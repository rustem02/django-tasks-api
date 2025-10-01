import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status as drf_status

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        logger.error("Unhandled exception", exc_info=exc)
        return Response({'error': str(exc)}, status=drf_status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        logger.error("API exception: %s", response.data)
    except Exception:
        logger.error("API exception without data")
    return response
