import logging

class SimpleMiddleware:

	def process_exception(self, request, exception):
		logging.error(str(exception))
