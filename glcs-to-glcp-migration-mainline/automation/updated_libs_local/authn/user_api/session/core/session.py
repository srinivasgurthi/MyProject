"""
Core REST Session Library
"""
try:
    import simplejson as json
except ImportError:
    import json
import logging
import pprint
import time
import urllib.parse as urlparse
from functools import wraps

import requests
from requests.exceptions import HTTPError, Timeout

from .exceptions import SessionException

LOG = logging.getLogger(__name__)
DEFAULT_RETRIABLE_ERRORS = [500, 501, 502, 503]


def exception_handler(func):
    """
    HTTP Requests Exception handler
    """

    @wraps(func)
    def decorator(obj, *args, **kwargs):
        retries = obj.max_retries
        while retries:
            try:
                if obj.debug:
                    obj._log_request(func, *args, **kwargs)
                return func(obj, *args, **kwargs)
            except HTTPError as e:
                retriable_errors = getattr(obj, "retriable_errors",
                                           DEFAULT_RETRIABLE_ERRORS)
                if e.response.status_code in retriable_errors:
                    obj._log_error_response(e.response)
                    LOG.warning(f"Response code : {e.response.status_code}")
                    if (
                            hasattr(obj, "validate_retriable_response") and
                            not obj.validate_retriable_response(e.response)
                    ):
                        raise SessionException(
                            "Response validation failed for API "
                            f"'{e.response.request.method} "
                            f"{e.response.request.url}' : "
                            f"'{e.response.status_code}'",
                            e.response
                        )
                    else:
                        retries -= 1
                        if retries:
                            LOG.error(f"Waiting for {obj.retry_timeout} "
                                      "seconds before retrying...")
                            time.sleep(obj.retry_timeout)
                            continue
                        LOG.error("Retries exhausted")
                        raise SessionException(
                            f"Retries exhausted for API "
                            f"'{e.response.request.method} "
                            f"{e.response.request.url}' : "
                            f"'{e.response.status_code}'",
                            e.response
                        )
                elif e.response.status_code == 401:
                    obj._log_request_headers(e.response.request)
                    obj._log_error_response(e.response)
                    if hasattr(obj, "refresh_token") and obj.refresh_token():
                        LOG.debug("Retrying the API after token refresh")
                        continue
                    raise SessionException(
                        f"Non Retryable error '{e.response.status_code}' for "
                        f"API '{e.response.request.method} "
                        f"{e.response.request.url}'", e.response
                    )
                else:
                    obj._log_error_response(e.response)
                    LOG.warning(
                        f"Non Retryable error '{e.response.status_code}' for "
                        f"API '{e.response.request.method} "
                        f"{e.response.request.url}'"
                    )
                    raise SessionException(
                        f"Non Retryable error '{e.response.status_code}' for "
                        f"API '{e.response.request.method} "
                        f"{e.response.request.url}'", e.response
                    )
            except (ConnectionError, Timeout):
                raise SessionException("Connection Error or Timeout")
            except Exception as ex:
                raise SessionException(f"Exception occurred:\n{ex}")

    return decorator


class Session:
    """
    REST Session Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=False, **kwargs):
        """
        :param max_retries: Max number of retries for retriable errors
        :param retry_timeout: Timeout between the retries (in seconds)
        :param debug: Enable/Disable Debug logging of HTTP Requests/Responses
        :param kwargs: Additional Keyword arguments
            :override: Override the session object (Default: requests.Session)
        """
        if kwargs.get("override"):
            self.session = kwargs["override"]
        else:
            self.session = requests.Session()
        self.max_retries = max_retries
        self.retry_timeout = retry_timeout
        self.debug = debug

    def _get_url(self, url):
        parsed = urlparse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            return url
        elif hasattr(self, "base_url"):
            return self.base_url + url
        return None

    def _get_url_secondary(self, url):
        parsed = urlparse.urlparse(url)
        if parsed.scheme and parsed.netloc:
            return url
        elif hasattr(self, "secondary_base_url"):
            return self.secondary_base_url + url
        return None

    def _get_domain(self):
        if hasattr(self, "domain_name") and hasattr(self, "base_url"):
            return self.base_url.split('https://')[-1]

    def _log_request(self, func, *args, **kwargs):
        if func.__name__ in ["put", "post", "patch"]:
            data = kwargs.get("data") or kwargs.get("json")
            try:
                LOG.debug("Request " + "\n\n" +
                          pprint.pformat(json.loads(data)) + "\n")
            except TypeError:
                LOG.debug("Request " + "\n\n" +
                          pprint.pformat(data) + "\n")

    def _log_error_response(self, response):
        LOG.debug("Response Headers " + "\n\n" +
                  pprint.pformat(dict(response.headers)) + "\n")
        try:
            LOG.debug("Response" + "\n\n" + pprint.pformat(response.json())
                      + "\n")
        except json.JSONDecodeError:
            LOG.debug("Response" + "\n\n" + response.text + "\n")
        self._log_elapsed_time(response)

    def _log_elapsed_time(self, response):
        LOG.debug(f"Elapsed time : {response.elapsed.total_seconds()} seconds")

    def _log_request_headers(self, request):
        LOG.debug("Request Headers " + "\n\n" +
                  pprint.pformat(dict(request.headers)) + "\n")

    def _handle_response(self, response):
        self._log_elapsed_time(response)
        LOG.debug(f"Response content : {response.content}")
        try:
            return response.json()
        except json.JSONDecodeError:
            return response

    @exception_handler
    def get(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP GET method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        r = self.session.get(self._get_url(url), **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def get_secondary(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP GET method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        get_cookies = self.session.cookies.get_dict(domain=self._get_domain())
        r = self.session.get(self._get_url_secondary(url), cookies=get_cookies, **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def post(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP POST method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        r = self.session.post(self._get_url(url), **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def post_secondary(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP POST method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        get_cookies = self.session.cookies.get_dict(domain=self._get_domain())
        r = self.session.post(self._get_url_secondary(url), cookies=get_cookies, **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def put(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP PUT method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        r = self.session.put(self._get_url(url), **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def patch(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP PATCH method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        r = self.session.patch(self._get_url(url), **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)

    @exception_handler
    def delete(self, url, tuple_response=False, ignore_handle_response=False, **kwargs):
        """
        HTTP DELETE method
        :param url:
        :param tuple_response: Boolean for tuple response (Default: False)
        :param ignore_handle_response: Boolean to ignore response handling (Default: False)
        :param kwargs:
        :return:
            When ignore_handle_response is True, return Response object (requests.Response)
            Otherwise,
                Response json or response obect if tuple_response is False
                Tuple of status_code and response json/response object if tuple_response is True
        """
        r = self.session.delete(self._get_url(url), **kwargs)
        if ignore_handle_response:
            return r
        r.raise_for_status()
        if tuple_response:
            return r.status_code, self._handle_response(r)
        return self._handle_response(r)
