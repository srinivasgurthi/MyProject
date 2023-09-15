import logging
from logging import DEBUG

log = logging.getLogger(__name__)

class AcDataPayload:
    @staticmethod
    def aob_data():
        aob_data_default = {
            "app_data" : {
                "name": "HokuTest2 App1",
                "description": "HokuTest2 for testing",
                "company_name": "HokuTest2 Networks",
                "logo": "HOKUTST1",
                "msp_supported": True,
                "email_addresses": [
                    "hcloud203+WLVU@gmail.com"
                ],
                "slug": "HOKUTST"
            },
            "instance_data" : {
                "short_name": "HOKUTST1",
                "version": "1.0.0",
                "description": "HOKU app Instance 1 for NMS in AWS US-West region",
                "content": "Main ST Long content for application in App instance 1",
                "languages": [],
                "docs": "https://st-long-term-triton1.triton.sample-app.ccs.arubathena.com/docs",
                "cloud_provider": {
                    "name": "AWS",
                    "region": "us-west-1",
                    "location": "Oregon",
                    "zone": "a"
                },
                "event_endpoint": "https://st-long-term-triton1.triton.sample-app.ccs.arubathena.com/events",
                "ccs_region": "us-west"
            },
            "algorithm_data" : {
                "name" : "round-robin",
                "description" : "Round-Robin Algorithm"
            },
            "app_rule_data" : {
                "customer_sticky" : False,
                "description" : "App Rule"
            },
            "instance_rule_data" : {
                "description" : "App Instance Rule",
                "countries_groups_included": [
                    "AME",
                    "NAM"
                ],
                "countries_groups_excluded": [
                    "EUR"
                ],
                "customers_included": [
                    "ATT",
                    "Sprint"
                ],
                "customers_excluded": [
                    "Costco"
                ]
            }
        }

        return aob_data_default
