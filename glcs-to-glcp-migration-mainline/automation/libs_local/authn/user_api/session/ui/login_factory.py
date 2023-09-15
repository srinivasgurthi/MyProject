"""
CCS Login Factory to handle different login types
"""
import importlib
import logging

from .login_types import LOGIN_TYPES

LOG = logging.getLogger(__name__)

class CCSLoginFactory(object):
    """
    CCS Login Factory class for handling different login types
    """

    def __new__(cls, *args, **kwargs):
        """
        :param args: Argument tuple
            First argument is the cluster config obtained from settins.json API
        :param kwargs: Keyword arguments
            Keyword arguments to be passed on to the actual login type class i.e.
            user and password
        """
        cluster_config = args[0]
        login_type = kwargs.get("login_type", None)

        if cluster_config.get("isOkta", False):
            if login_type == "okta_mfa":
                return LOGIN_TYPES["okta_mfa"](*args, **kwargs)
            elif login_type == "okta_sso":
                return LOGIN_TYPES["okta_sso"](*args, **kwargs)
            else:
                return LOGIN_TYPES["okta"](*args, **kwargs)
        else:
            return LOGIN_TYPES["pf"](*args, **kwargs)
