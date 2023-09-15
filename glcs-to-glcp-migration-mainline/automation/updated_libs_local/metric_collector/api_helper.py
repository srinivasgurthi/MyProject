import functools
import logging
import time

import requests
from requests.exceptions import HTTPError

log = logging.getLogger(__name__)

DEFAULT_RETRY_STATUS_CODES = [
    # 500,
    501,
    503,
    412,
    401,
]  # CCS-5667:Retry 401 error code till unauthorised issue is resolved


class MetricCollectorFTException(Exception):
    """Exception raised for errors in the account management api request.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Exception from metric collector api"):
        self.message = message
        super().__init__(self.message)


def retry_on_server_error(delay=10, times=6):
    """
    A decorator for retrying a function call with a specified delay in case of a set of exceptions

    Parameter List
    -------------

    :param delay: Amount of delay (seconds) needed between successive retries.
    :param times: no of times the function should be retried

    """

    def outer_wrapper(my_func):
        @functools.wraps(my_func)
        def inner_wrapper(*args, **kwargs):
            skip_retry = False
            if "skip_retry" in kwargs:
                skip_retry = kwargs.pop("skip_retry")
            for counter in range(1, times + 1):
                try:
                    response = my_func(*args, **kwargs)
                    if skip_retry:
                        log.info("retry has been skipped")
                        return response
                    if response.status_code not in DEFAULT_RETRY_STATUS_CODES:
                        return response
                    log.info(
                        f"******* NOTE ******* \n STATUS_CODE is {response.status_code} \n"
                        f"which is part of DEFAULT_RETRY_STATUS_CODES, so going for RETRY."
                    )
                    log.info("Waiting for {} seconds, before retry".format(delay))
                    time.sleep(delay)
                    if counter == times:
                        return response
                except HTTPError as http_error:
                    if (
                        http_error.response.status_code
                        not in DEFAULT_RETRY_STATUS_CODES
                    ):
                        log.warning(
                            f"Request is not success, status code {http_error.response.status_code}"
                        )
                        return http_error

                    log.info(
                        "Exception from server {}, retying count {}".format(
                            str(http_error), counter
                        )
                    )
                    log.info("Waiting for {} seconds, before retry".format(delay))
                    time.sleep(delay)

                except TimeoutError as t_e:
                    raise MetricCollectorFTException(
                        "Timeout Error, details {}".format(str(t_e))
                    )

                except (
                    ConnectionAbortedError,
                    ConnectionAbortedError,
                    ConnectionRefusedError,
                ) as c_e:
                    raise MetricCollectorFTException(
                        "Connection Error, details {}".format(str(c_e))
                    )

                except Exception as e:
                    raise MetricCollectorFTException(
                        "Unknown Error, details {}".format(str(e))
                    )

        return inner_wrapper

    return outer_wrapper


class LocalApiHelper(object):
    def __init__(self, protocol, api_hostname, base_url, port=None, ui_hostname=None):
        self.BASE_PROTOCOL = protocol
        self.BASE_API_HOSTNAME = api_hostname
        self.BASE_PORT = port
        self.BASE_UI_HOSTNAME = ui_hostname
        self.BASE_url = base_url
        self.req_url = None

    @retry_on_server_error()
    def api_request(self, method, api_path=None, full_path=None, **kwargs):
        """Generic API method for REST call, this handled with retry decorator to
        retry on the specific defaulted error codes.

        :param method REST method name as string, example - GET, PUT, POST, DELETE
        :param api_path End point for the API
        :param full_path full api path like healthz as it doesn't have /internal/v1
        :param **kwargs all the keyword arguments accepted by requests.request method.

        :return api response"""
        if not full_path:
            full_api_path = self.BASE_url + api_path
        else:
            full_api_path = full_path

        self.req_url = self.__construct_req_url(full_api_path)
        log.info(f"API CALL: URL - {self.req_url}, Method Request - {method}")
        if kwargs.get("headers"):
            log.info(f"headers for the call : {kwargs['headers']}")
        response = requests.request(method, self.req_url, **kwargs)
        if response is None:
            raise MetricCollectorFTException(
                f"Response from {api_path} is {method} request is None"
            )
        log.info(
            f"******* RESPONSE CODE FROM {self.req_url} *******\t {response.status_code}"
        )
        if response.status_code != 204:
            log.info(
                f"******* RESPONSE FROM {self.req_url} ******* \n {response.json()}"
            )

        return response

    def __construct_req_url(self, api_path):
        """Private method to construct the full url from the given end point."""
        if not self.BASE_PORT:
            req_url = "{}://{}/{}".format(
                self.BASE_PROTOCOL, self.BASE_API_HOSTNAME, api_path,
            )
        else:
            req_url = "{}://{}:{}/{}".format(
                self.BASE_PROTOCOL, self.BASE_API_HOSTNAME, self.BASE_PORT, api_path,
            )
        return req_url
