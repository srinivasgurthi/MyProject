"""
Report Engine Internal API Library
"""
import logging
import pprint
from functools import wraps
from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class ReportEngine(Session):
    """
    Report Engine Internal API Class
    """

    def __init__(self, max_retries=3, retry_timeout=5, debug=True, **kwargs):
        log.info("Initializing report_engine for internal api calls")
        super().__init__(max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs)
        self.host = "http://report-engine-svc.ccs-system.svc.cluster.local:80"
        self.base_path = "/report-engine/internal"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.host}{self.base_path}{self.api_version}/{path}"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Request"
            )
            res = func(*args, **kwargs)
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response" \
                + "\n\n" + pprint.pformat(res) + "\n"
            )
            return res

        return decorated_func

    @_log_response
    def health_check_status(self):
        """
        Get status of the Report Engine service health check status
        :return: JSON object of the status
        """
        # http://report-engine-svc.ccs-system.svc.cluster.local:80/report-engine/internal/v1/healthcheck
        return self.get(
            url=self._get_path("healthcheck"), ignore_handle_response=True
        )


if __name__ == "__main__":
    re = ReportEngine()
    re.health_check_status()