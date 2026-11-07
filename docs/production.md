# Production deployment after the shared Nginx migration

Production uses **only** `docker-compose.prod.yml`, a standalone configuration.
The base `docker-compose.yml` remains for development/test use; combining it with
production would reintroduce the old Nginx service and its public port bindings.

The shared Nginx deployment is managed separately at
`/home/david/shared-web-infrastructure`. PawnGuild must not stop, recreate, or
configure it. The external `shared_web_frontend` network connects the app using
alias `pawnguild-app`; PostgreSQL remains on `pawnguild_default` only.

`./scripts/deploy-production.sh` validates existing infrastructure and updates only
`web`. It reuses the installed runtime image, collects static assets, and reloads
Gunicorn. PostgreSQL and its existing data volume are left running. The production
command runs Gunicorn directly: it does not call the development `start.sh` or run
`makemigrations`, `migrate`, or `createsuperuser`. Intentional schema changes require
a separately prepared migration and a fresh verified backup. This release has none.

All existing production data volumes are declared external. Never run volume
pruning, `down -v`, restore tests, or destructive historical debugging recipes on
this host. Protect `/var/backups/db_backups` and the migration recovery directory
`/home/david/pawnguild-migration-20260913`.

The production GitHub workflow no longer builds on the droplet or runs Compose
`down`. Dependency/Dockerfile changes cause it to stop before updating the checkout,
so a compatible image can be prepared separately. App/template changes use the
existing bind-mounted source and runtime. A production push still deploys the app;
do not push a change until it is ready for production.

## Image-upload security runtime (November 2026)

The image-upload security patch uses Python 3.11 and Pillow 13, installed from a
binary wheel so its patched image libraries are included. Django remains at its
existing version. Psycopg2 and PyYAML are updated only for Python 3.11 compatibility.
CI builds the full production image and runs synthetic tests without network or
production data, including picture creation/replacement and a libwebp version check.

Prepare and validate the new image before deployment, retain the old image under
a rollback tag, and take a fresh private database dump with an archive-directory
check. The workflow's dependency guard intentionally blocks an unprepared runtime
change. After an operator verifies the image and fast-forwards the production
checkout, rerunning the workflow uses the usual app-only deployment script. This
release needs no migrations, database restart, or changes to shared Nginx.

## Django 5.2 LTS runtime (November 2026)

This runtime uses Django 5.2.19 with compatible asgiref, sqlparse, and Django
REST framework pins. The Python/Pillow image base is unchanged. Existing account,
pawn, and media models have no changes; a synthetic Django 3.2 database was checked
under 5.2, including existing sessions, password hashes, email-verification tokens,
and pawn updates. Check the live migration plan read-only before release; do not
run migrations automatically.

The obsolete password-reset add-on is replaced with Django's built-in reset flow.
Username-or-email recovery, the site's templates, and `/recover/` remain. Newly
issued links are single-use and expire after 48 hours. Reset emails issued before
this release need a fresh recovery request; existing accounts and passwords are
unchanged. Logout uses a CSRF-protected POST as required by current Django.

Use the same prepared-image, fresh-backup, rollback-tag, and app-only deployment
procedure described above. No database or shared Nginx restart is required.

## Gunicorn and outbound TLS runtime (November 2026)

The runtime uses Gunicorn 26.2.0, the current published PyPI release, and updated
certifi, cryptography, pyOpenSSL, requests, urllib3, IDNA, and related support
packages. Pillow, cryptography, and CFFI are installed from binary wheels so the
validated native libraries are included. The unused legacy ndg-httpsclient,
pyasn1, and chardet pins are removed; requests uses charset-normalizer.

Gunicorn's optional management socket is disabled. Deployment still uses the
existing sync WSGI worker and HUP reload. CI runs isolated loopback checks for
normal requests, rejection of ambiguous HTTP framing, worker reload, and trusted
versus untrusted TLS certificates using temporary test certificates only.
Application code and database models are unchanged. Use the same prepared-image,
fresh-backup, rollback-image, and app-only deployment procedure above.

## Unused Python dependencies and deployment actions (November 2026)

The runtime removes the unused CoreAPI/coreschema/Jinja stack, nose test runner,
unused-media management add-on, and their obsolete support packages. Django REST
framework's current schema endpoint keeps its explicit uritemplate dependency.
Setuptools is pinned to 84.2.1 to replace the older build tool inherited from the
base image. No application behavior, templates, models, or schema changes are
included. Browser libraries remain a separate update requiring visual validation.

GitHub Actions use reviewed immutable commit pins and read-only repository-token
permissions. The SSH action's helper version is explicit. Keep these pins under
review when updating actions; the production dependency guard remains enabled.
Use the prepared-image, verified-backup, rollback-image, and app-only deployment
procedure above for this runtime change.

## Browser-library security update (November 2026)

The shared template pins jQuery 3.7.1 slim, Bootstrap 4.6.2 CSS/JavaScript, and
Popper 1.16.1 with verified SHA-384 integrity hashes. These compatible updates
remove the seven previously identified browser-library advisories. Bootstrap 4
remains end-of-life; moving to a supported major version is a separate migration.
Small CSS overrides retain the original table colours, small-text size, and
activity-star alignment. The base stylesheet URL is versioned to refresh caches.

Compare the original and updated templates using synthetic local data in Chromium
and WebKit at desktop, tablet, and phone widths. Check navigation collapse and
dropdowns, filters, pagination, and account/pawn forms alongside screenshots.
This template/static-only release uses the existing runtime image and the usual
app-only deployment script. It requires no database writes or migrations.

## Pawn activity filter

Individual platform pages offer Currently active (the existing default), Updated
within the last year (365 days by last update), and All time. The activity selector
appears before the level fields in the same row, wrapping on smaller screens.
The All Pawns page does not display the selector. This changes reads/display only;
older pawns are neither modified nor deleted. Both the combined page and each
platform page have bounded pagination (50 per platform) and preserve filter values.
The API and account-management behavior are unchanged.
