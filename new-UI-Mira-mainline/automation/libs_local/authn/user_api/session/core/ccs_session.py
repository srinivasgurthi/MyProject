"""
CCS Session Library
"""
import logging

from .session import Session


LOG = logging.getLogger(__name__)


class CCSSession(Session):
    """
    CCS Session Class
    """
    
    def __init__(self, **kwargs):
        """
        :param kwargs: Keyword arguments
        """
        super(CCSSession, self).__init__(**kwargs)

    def validate_retriable_response(self, response):
        """
        Additional validation of retriable errors before going for retries
        :param response: Response object
        :return: True/False
        """
        if not response.headers.get("server") == "HPE":
            LOG.error("Server Header not found")
            return False
        return True
