"""
App Catalog UI API Library
"""
import json
import logging
import pprint
import requests
import time

from functools import wraps

LOG = logging.getLogger(__name__)


class AppCatalog(object):
    """
    App Catalog UI API Class
    """

    def __init__(self, session, **kwargs):
        """
        :param session: UI Session object
        """
        self.session = session
        self.base_path = "/app_api-catalog/ui/"
        self.api_version = "v1/"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}{path}"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            LOG.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Request"
            )
            res = func(*args, **kwargs)
            LOG.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response" \
                + "\n\n" + pprint.pformat(res) + "\n"
            )
            return res
        return decorated_func

    @_log_response
    def get_status(self):
        """
        Get status of the App Catalog service UI API
        :return: JSON object of the status
        """
        return self.session,get(self._get_path("status"))

    @_log_response
    def create_app(self, app_data):
        """
        Create an application in App Catalog
        :param app_data: Manifest data of the application to be created
        :return: JSON body containing App ID
        """
        return self.session.post(self._get_path("applications"), json=app_data)

    @_log_response
    def update_app(self, app_id, app_data):
        """
        Update an application in App Catalog
        :param app_id: App ID of the application to be updated
        :param app_data: Manifest data of the application to be created
        :return: JSON body containing App ID
        """
        return self.session.put(self._get_path(f"applications/{app_id}"),
                                json=app_data)

    @_log_response
    def get_apps(self, app="", **params):
        """
        Get applications from App Catalog
        :param app: App ID or Slug
        :param params: Keyword argument of the following:
            status : Status value like ONBOARDED, PUBLISHED etc
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing applications
        """
        if app:
            return self.session.get(self._get_path(f"applications/{app}"))
        else:
            return self.session.get(
                self._get_path(f"applications"), params=params
            )

    @_log_response
    def delete_app(self, app_id):
        """
        Delete an application from App Catalog
        :param app_id: App ID of the application to be deleted
        :return:
        """
        return self.session.delete(self._get_path(f"applications/{app_id}"))

    @_log_response
    def accept_review(self, app_id):
        """
        Accept the Review of the Application Manifest
        :param app_id: App ID of the application to be deleted
        :return:
        """
        return self.session.post(
            self._get_path("applications/{app_id}/review-accept")
        )

    @_log_response
    def get_reviews(self, app="", **params):
        """
        Get reviews from App Catalog
        :param app: App ID or Slug
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing reviews
        """
        if app:
            return self.session.get(
                self._get_path(f"applications/reviews/{app}")
            )
        else:
            return self.session.get(
                self._get_path("applications/reviews"), params=params
            )

    @_log_response
    def delete_review(self, app_id):
        """
        Delete the pending review for an app_api
        :param app_id: App ID of the application to be deleted
        :return:
        """
        return self.session.delete(
            self._get_path(f"applications/reviews/{app_id}")
        )

    @_log_response
    def get_algorithms(self, algorithm="", **params):
        """
        Get the configured algorithms
        :param algorithm: Algorithm name
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing algorithms
        """
        if algorithm:
            return self.session.get(self._get_path(f"algorithms/{algorithm}"))
        else:
            return self.session.get(
                self._get_path(f"algorithms"), params=params
            )

    @_log_response
    def add_algorithm(self, name, description):
        """
        Add an algorithm
        :param name: Name of the algorithm
        :param description: Description of the algorithm
        :return: JSON body
        """
        return self.session.post(
            self._get_path("algorithms"),
            json={"name" : name, "description" : description}
        )

    @_log_response
    def update_algorithm(self, name, description):
        """
        Update an algorithm
        :param name: Name of the algorithm to be updated
        :param description: Description of the algorithm
        :return: JSON body
        """
        return self.session.put(
            self._get_path(f"algorithms/{name}"),
            json={"name" : name, "description" : description}
        )

    @_log_response
    def delete_algorithm(self, name):
        """
        Delete an algorithm
        :param name: Name of the algorithm to be deleted
        :return:
        """
        return self.session.delete(self._get_path(f"algorithms/{name}"))

    @_log_response
    def add_instance(self, instance_data):
        """
        Add an application instance
        :param instance_data: JSON data of the instance info
        :return: JSON object containing instance ID and meta
        """
        return self.session.post(self._get_path("app_api-instances"),
                                 json=instance_data)

    @_log_response
    def update_instance(self, instance_id, instance_data):
        """
        Update an application instance
        :param instance_id: Instance ID
        :param instance_data: JSON data of the instance info
        :return: JSON object containing instance ID and meta
        """
        return self.session.put(self._get_path(f"app_api-instances/{instance_id}"),
                                json=instance_data)

    @_log_response
    def get_instances(self, instance_id="", **params):
        """
        Get the configured application instances
        :param instance_id: Instance ID
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
            status : Status value like ONBOARDED, ONBOARDING etc
            region : Region code
            appid_or_slug : App ID or App slug
        :return: JSON body containing app_api instances
        """
        if instance_id:
            return self.session.get(
                self._get_path(f"app_api-instances/{instance_id}")
            )
        else:
            return self.session.get(
                self._get_path(f"app_api-instances"), params=params
            )

    @_log_response
    def delete_instance(self, instance_id):
        """
        Delete an application instance
        :param instance_id: ID of the instance to be deleted
        :return:
        """
        return self.session.delete(
            self._get_path(f"app_api-instances/{instance_id}")
        )

    @_log_response
    def bootstrap_instance(self, instance_id):
        """
        Bootstrap an application instance
        :param instance_id: ID of the instance to be deleted
        :return:
        """
        return self.session.post(
            self._get_path(f"app_api-instances/{instance_id}/bootstrap")
        )

    @_log_response
    def publish_app(self, app_id):
        """
        Publish an App
        :param app_id: App ID of the application to be published
        :return:
        """
        return self.session.post(
            self._get_path(f"applications/{app_id}/publish")
        )

    @_log_response
    def add_app_rule(self, app_id, algorithm, rule_data):
        """
        Add an application rule
        :param app_id: App ID of the application
        :param algorithm: Algorithm name
        :param rule_data: Rule data dict
        :return:
        """
        data = {
            "app_id" : app_id, "algorithm" : algorithm,
            "customer_sticky" : rule_data.get("customer_sticky", False),
            "description" : rule_data.get("description", "Default App Rule")
        }
        return self.session.post(
            self._get_path("app_api-rules"), json=data
        )

    @_log_response
    def update_app_rule(self, rule_id, app_id, algorithm, rule_data):
        """
        Update an application rule
        :param rule_id: Ruld ID of the rule to be updated
        :param app_id: App ID of the application
        :param algorithm: Algorithm name
        :param rule_data: Rule data dict
        :return:
        """
        data = {
            "app_id" : app_id, "algorithm" : algorithm,
            "customer_sticky" : rule_data.get("customer_sticky", False),
            "description" : rule_data.get("description", "Default App Rule")
        }
        return self.session.put(self._get_path(f"app_api-rules/{rule_id}"),
                                json=data)

    @_log_response
    def get_app_rules(self, rule_id="", **params):
        """
        Get the configured application rules
        :param rule_id: Rule ID of the rule
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing app_api rules
        """
        if rule_id:
            return self.session.get(self._get_path(f"app_api-rules/{rule_id}"))
        else:
            return self.session.get(
                self._get_path(f"app_api-rules"), params=params
            )

    @_log_response
    def delete_app_rule(self, rule_id):
        """
        Delete an application rule
        :param rule_id: Rule ID of the rule to be deleted
        :return:
        """
        return self.session.delete(self._get_path(f"app_api-rules/{rule_id}"))

    @_log_response
    def add_instance_rule(self, instance_id, rule_data):
        """
        Add an application rule
        :param instance_id: ID of the application instance
        :param rule_data: Rule data dict
        :return:
        """
        data = { "instance_id" : instance_id, **rule_data }
        return self.session.post(self._get_path("app_api-instance-rules"),
                                 json=data)

    @_log_response
    def update_instance_rule(self, rule_id, instance_id, rule_data):
        """
        Update an application rule
        :param rule_id: Rule ID of the rule to be updated
        :param instance_id: ID of the application instance
        :param rule_data: Rule data dict
        :return:
        """
        data = { "instance_id" : instance_id, **rule_data }
        return self.session.put(self._get_path(f"app_api-instance-rules/{rule_id}"),
                                json=data)

    @_log_response
    def get_instance_rules(self, rule_id="", **params):
        """
        Get the configured application instance rules
        :param rule_id: Rule ID of the instance rule
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing instance rules
        """
        if rule_id:
            return self.session.get(
                self._get_path(f"app_api-instance-rules/{rule_id}")
            )
        else:
            return self.session.get(
                self._get_path(f"app_api-instance-rules"), params=params
            )

    @_log_response
    def delete_instance_rule(self, rule_id):
        """
        Delete an instance rule
        :param rule_id: Rule ID of the instance rule to be deleted
        :return:
        """
        return self.session.delete(
            self._get_path(f"app_api-instance-rules/{rule_id}")
        )

    @_log_response
    def get_countries(self, code="", auth=True, **params):
        """
        Get countries
        :param code: Country code
        :param params: Keyword argument of the following:
            status : Status value like AVAILABLE etc
            country_group_code : Country Group code
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing countries
        """
        if code:
            return self.session.get(self._get_path(f"countries/{code}"))
        else:
            if auth:
                return self.session.get(
                    self._get_path("countries"), params=params
                )
            else:
                r = requests.get(
                    f"{self.base_url}{self._get_path('countries')}",
                    allow_redirects=False
                )
                if r.status_code != 200:
                    raise Exception("Cannot invoke API without auth token")
                return r.json()

    @_log_response
    def get_country_groups(self, code="", **params):
        """
        Get country groups
        :param code: Country Group code
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing country groups
        """
        if code:
            return self.session.get(self._get_path(f"country-groups/{code}"))
        else:
            return self.session.get(
                self._get_path(f"country-groups"), params=params
            )

    @_log_response
    def get_regions(self, code="", **params):
        """
        Get regions
        :param code: Region code
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing regions
        """
        if code:
            return self.session.get(self._get_path(f"regions/{code}"))
        else:
            return self.session.get(self._get_path(f"regions"), params=params)

    @_log_response
    def get_apps_by_region(self, region="", **params):
        """
        Get applications by regions
        :param region: Region code
        :return JSON body of the list of applications
        """
        if region:
            return self.session.get(
                self._get_path(f"regions/{region}/applications")
            )
        else:
            return self.session.get(self._get_path(f"regions/applications"),
                                    params=params)

    @_log_response
    def get_per_region_apps(self, **params):
        """
        Get per region applications
        :param params: Query parameters
            offset: Pagination offset
            limit: Page length
            msp_supported: Boolean flag if MSP supported or not
        :return JSON body of the list of applications
        """
        return self.session.get(self._get_path("per-region-applications"),
                                params=params)

    @_log_response
    def get_languages(self, code="", **params):
        """
        Get languages
        :param code: Language code
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing languages
        """
        if code:
            return self.session.get(self._get_path(f"languages/{code}"))
        else:
            return self.session.get(self._get_path(f"languages"), params=params)

    @_log_response
    def get_timezones(self, **params):
        """
        Get timezones
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
        :return: JSON body containing timezones
        """
        return self.session.get(self._get_path(f"timezones"), params=params)

    @_log_response
    def get_cloud_info_region_map(self, **params):
        """
        Get cloud info region map
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
            provider : Cloud Provider
            region : Region code
        :return: JSON body containing cloud info region map
        """
        return self.session.get(self._get_path(f"cloud-regions"), params=params)

    def wait_for(self, instances, key, value, iterations=10, delay=6):
        """
        Wait for the Instance's key to reach the expected value
        :param instances: List of Instance IDs that need to be queries
        :param key: Key to be checked
        :param value: Value of the key to be checked for
        :param iteration: No of times to check
        :param delay: Delay between the iterations
        :return: (True/False)
        """
        for iteration in range(1, iterations + 1):
            tmp_instances = instances[:]
            for inst in tmp_instances:
                res = self.get_instances(inst)
                if res[key] == value:
                    instances.remove(inst)
            if not instances:
                LOG.info(f"The '{key}' for all instances reached '{value}'")
                return True
            time.sleep(delay)
            LOG.info(f"Waited for {iteration*delay} seconds for '{key}' change")
        else:
            LOG.error(f"Few instances did not reach '{value}' for '{key}'" + \
                      "\n\n" + pprint.pformat(instances) + "\n")
            return False
