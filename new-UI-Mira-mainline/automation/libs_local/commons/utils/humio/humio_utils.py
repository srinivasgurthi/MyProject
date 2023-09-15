import logging
from humiolib.HumioClient import HumioClient

log = logging.getLogger(__name__)
class HumioClass:
    """
    class for querying logs in humio for Glcp environments
    :param base_url: example: "https://mira-us-east-2.cloudops.ccs.arubathena.com/logs"
    :param repository: example "ccsportal"
    :param user_token: user_token for the humio env
    :return: list of results
    https://python-humio.readthedocs.io/en/latest/reference/humioclient.html
    example:
        InitHumioQueryJob = HumioClass(base_url=base_url, repository=repository, user_token=user_token)
        result = InitHumioQueryJob.create_queryjob('"CCS_DEVICE_HISTORY_EVENT" AND "serialNumber=BE0246695"',
                                       start=1680612132222,
                                       end=1680632432222)
    """
    def __init__(self, **kwargs):
        self.base_url = kwargs['base_url']
        self.repository = kwargs['repository']
        self.user_token = kwargs['user_token']
        self.client = HumioClient(base_url=self.base_url,
                                  repository=self.repository,
                                  user_token=self.user_token)
    def create_queryjob(self,
                       query_string,
                       start=None,
                       end=None,
                       is_live=None,
                       timezone_offset_minutes=None,
                       arguments=None,
                       raw_data=None,
                       **kwargs):
        """
        :param: query_string (str) – Humio query
        :param: start (Union[int, str], optional) – Starting time of query (epoch time)
        :param: end (Union[int, str], optional) – Ending time of query (epoch time)
        :param: is_live (int, optional) – Ending time of query
        :param: timezone_offset_minutes – Timezone offset in minutes
        :param: argument (dict(string->string), optional) – Arguments specified in query
        :param: raw_data (dict(string->string), optional) – Additional arguments to add to POST body under other keys
        :return: list of results
        """
        try:
            queryjob = self.client.create_queryjob(query_string,
                                                   start,
                                                   end,
                                                   is_live,
                                                   timezone_offset_minutes,
                                                   arguments,
                                                   raw_data
                                                   )
            res = []
            for poll_result in queryjob.poll_until_done():
                for event in poll_result.events:
                    res.append(event)
            return res
        except Exception as e:
            log.error(f"not able to get the query result: {e}")
