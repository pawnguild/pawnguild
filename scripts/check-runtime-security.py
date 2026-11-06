"""Isolated loopback checks: no production settings, accounts, or external traffic."""
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
from threading import Thread
import time
import unittest

import certifi
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID
from OpenSSL import SSL, crypto
import requests


class GunicornChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = tempfile.TemporaryDirectory(prefix="pawnguild-gunicorn-check-")
        cls.addClassCleanup(folder.cleanup)
        Path(folder.name, "probe.py").write_text(
            "import os\n"
            "def application(environ, start_response):\n"
            "    body = ('OK:' + str(os.getpid())).encode()\n"
            "    start_response('200 OK', [('Content-Length', str(len(body)))])\n"
            "    return [body]\n"
        )
        listener = socket.socket()
        listener.bind(("127.0.0.1", 0))
        listener.listen(16)
        cls.port = listener.getsockname()[1]
        cls.log = tempfile.TemporaryFile()
        cls.addClassCleanup(cls.log.close)
        env = os.environ.copy()
        env.pop("GUNICORN_CMD_ARGS", None)
        cls.process = subprocess.Popen(
            [sys.executable, "-m", "gunicorn", "probe:application", "--workers", "1",
             "--bind", "fd://" + str(listener.fileno()), "--no-control-socket"],
            cwd=folder.name, env=env, pass_fds=(listener.fileno(),),
            stdout=cls.log, stderr=subprocess.STDOUT,
        )
        listener.close()
        cls.addClassCleanup(cls.stop_server)
        cls.session = requests.Session()
        cls.session.trust_env = False
        cls.addClassCleanup(cls.session.close)
        cls.wait_for_worker()

    @classmethod
    def stop_server(cls):
        cls.process.terminate()
        try:
            cls.process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            cls.process.kill()
            cls.process.wait(timeout=5)

    @classmethod
    def wait_for_worker(cls, previous=None):
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if cls.process.poll() is not None:
                break
            try:
                response = cls.session.get(
                    "http://127.0.0.1:" + str(cls.port), timeout=1
                )
                if response.status_code == 200 and response.text != previous:
                    return response.text
            except requests.RequestException:
                pass
            time.sleep(0.05)
        cls.log.seek(0)
        raise AssertionError(
            "Gunicorn failed to become ready: " + cls.log.read().decode()
        )

    def test_normal_http_request(self):
        self.assertTrue(self.wait_for_worker().startswith("OK:"))

    def test_ambiguous_request_framing_is_rejected(self):
        request = (
            b"POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\n"
            b"Transfer-Encoding: chunked\r\nConnection: close\r\n\r\n0\r\n\r\n"
        )
        with socket.create_connection(("127.0.0.1", self.port), timeout=3) as stream:
            stream.sendall(request)
            response = stream.recv(4096)
        self.assertIn(b"400", response.split(b"\r\n", 1)[0])
        self.assertNotIn(b"OK:", response)

    def test_hup_reload_replaces_worker_and_keeps_serving(self):
        previous = self.wait_for_worker()
        self.process.send_signal(signal.SIGHUP)
        self.assertNotEqual(self.wait_for_worker(previous), previous)


class TLSChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = tempfile.TemporaryDirectory(prefix="pawnguild-tls-check-")
        cls.addClassCleanup(folder.cleanup)
        root = Path(folder.name)
        now = datetime.now(timezone.utc)
        ca_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        name = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, "Synthetic test CA")
        ])
        ca = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
              .public_key(ca_key.public_key())
              .serial_number(x509.random_serial_number())
              .not_valid_before(now - timedelta(minutes=1))
              .not_valid_after(now + timedelta(days=1))
              .add_extension(
                  x509.BasicConstraints(ca=True, path_length=0), critical=True
              )
              .sign(ca_key, hashes.SHA256()))
        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
        leaf = (x509.CertificateBuilder()
                .subject_name(leaf_name)
                .issuer_name(name).public_key(key.public_key())
                .serial_number(x509.random_serial_number())
                .not_valid_before(now - timedelta(minutes=1))
                .not_valid_after(now + timedelta(days=1))
                .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]),
                               critical=False)
                .add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
                               critical=False)
                .sign(ca_key, hashes.SHA256()))
        cls.ca_path = root / "ca.pem"
        cls.ca_path.write_bytes(ca.public_bytes(serialization.Encoding.PEM))
        cert_path, key_path = root / "server.pem", root / "server-key.pem"
        cls.leaf_pem = leaf.public_bytes(serialization.Encoding.PEM)
        cert_path.write_bytes(cls.leaf_pem)
        key_path.write_bytes(key.private_bytes(
            serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ))

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"TLS OK")

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)
        server.socket = context.wrap_socket(server.socket, server_side=True)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        cls.addClassCleanup(server.server_close)
        cls.addClassCleanup(thread.join, 5)
        cls.addClassCleanup(server.shutdown)
        cls.url = "https://localhost:" + str(server.server_port)
        cls.session = requests.Session()
        cls.session.trust_env = False
        cls.addClassCleanup(cls.session.close)

    def test_trusted_certificate_succeeds_and_untrusted_certificate_fails(self):
        response = self.session.get(self.url, verify=str(self.ca_path), timeout=3)
        self.assertEqual(response.text, "TLS OK")
        with self.assertRaises(requests.exceptions.SSLError):
            self.session.get(self.url, timeout=3)

    def test_patched_certificate_bundle_and_native_crypto_load(self):
        context = ssl.create_default_context(cafile=certifi.where())
        self.assertGreater(context.cert_store_stats()["x509_ca"], 0)
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        context.load_verify_locations(str(self.ca_path))
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, self.leaf_pem)
        names = cert.to_cryptography().subject.get_attributes_for_oid(
            NameOID.COMMON_NAME
        )
        self.assertEqual(names[0].value, "localhost")


if __name__ == "__main__":
    unittest.main(verbosity=2)
