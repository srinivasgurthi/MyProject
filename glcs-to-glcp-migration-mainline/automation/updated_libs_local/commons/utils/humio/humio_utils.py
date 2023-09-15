import json
import logging
import re
import time

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


class HumioHelper:
    @staticmethod
    def get_last_event_transaction_id(humio_session,
                                      search_query,
                                      search_duration_in_ms=3600000,
                                      timeout=10000):
        """
        search humio logs for event name and returns transactionId, message example:
        {"@timestamp":"2023-04-18T05:27:25.084Z","service_name":"activate-inventory","level":"INFO",
        "logger":"c.a.c.c.k.p.k.KafkaPublisherImpl","thread":"kafka-producer-network-thread | producer-1",
        "message":"Sent message=[topic:ACTIVATE-device-ccs-system, msg_key:STIAP4KOBP.JW242AR.IAP,
        event_type:DEVICE_PROVISION_INTERNAL_EVENT, offset:9286, partition:3,
        transactionId:b82444f7-de8b-4978-a56d-18ec60dafbc0]"}
        :param: humio_session
        :param: search_query (example: serial_number AND kafka-producer-network-thread AND DEVICE_PROVISION_INTERNAL_EVENT)
        :param: search_duration_in_ms
        :param: timeout for the method
        :return: transaction_id
        """
        epoch_time = int(time.time() * 1000.0)
        current_time = int(time.time() * 1000.0)
        timeout_time = current_time + timeout
        while current_time < timeout_time:
            result = humio_session.create_queryjob(
                search_query,
                start=epoch_time - search_duration_in_ms,
                end=epoch_time,
                is_live=False)
            json_log = json.loads(result[0]['log'])
            msg = json_log['message']
            match_id = re.search('(?<=transactionId:)(.*)', msg)
            transaction_id = match_id.group(1)[:-1]
            if transaction_id:
                log.info(f"Found logs in humio with transaction_id: '{transaction_id}'")
                return transaction_id
            time.sleep(1)
            current_time = int(time.time() * 1000.0)

    @staticmethod
    def event_with_transaction_id_exists(humio_session,
                                         transaction_id,
                                         service_name,
                                         result_search_str,
                                         search_duration_in_ms=3600000,
                                         timeout=10000):
        """
        search humio logs for event by transaction id for a service and search for string in message
        {"log":"{"@timestamp":"2023-04-18T05:28:25.084Z","service_name":"subscription-management",
        "level":"DEBUG","logger":"c.a.c.c.k.KafkaConsumerAutoConfiguration",
        "thread":"providesMessageListenerContainer-0-C-1",
        "message":"Received kafka record: after consume: key=STIAP4KOBP.JW242AR.IAP, 
        topic=ACTIVATE-device-ccs-system offset=435786 part=2, transactionId=b82444f7-de8b-4978-a56d-18ec60dafbc0"}
        :param: humio_session
        :param: transaction_id
        :service_name: name of service such as activate-inventory or subscription-management
        :param: result_search_str, such as "Received kafka record: after consume: key=STIAP4KOBP.JW242AR.IAP"
        :param: search_duration_in_ms
        :param: timeout for the method
        :return: boolean
        """
        log.info(f"Searching for logs in humio for transaction_id: '{transaction_id}'.")
        epoch_time = int(time.time() * 1000.0)
        current_time = int(time.time() * 1000.0)
        timeout_time = current_time + timeout
        while current_time < timeout_time:
            result = humio_session.create_queryjob(transaction_id,
                                                   start=epoch_time - search_duration_in_ms,
                                                   end=current_time,
                                                   is_live=False)
            for event in result:
                json_obj = json.loads(event["log"])
                log.info(event["log"])
                log.info(f"Searching for log string: '{result_search_str}'.")
                if json_obj["service_name"] == service_name:
                    if result_search_str in json_obj["message"]:
                        return True
            time.sleep(1)
            current_time = int(time.time() * 1000.0)
        return False
