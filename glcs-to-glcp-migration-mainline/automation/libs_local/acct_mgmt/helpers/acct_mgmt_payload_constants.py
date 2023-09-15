import logging
from logging import DEBUG

log = logging.getLogger(__name__)


class AmInputPayload(object):
    pod_namespace: str = ""
    log_level = DEBUG

    def create_msp_tenant(self):
        msp_create_tenant_data = {
            "tenant": {
                "customer_id": "string",
                "company_name": "string",
                "description": "string",
                "address": {
                    "street_address": "string",
                    "city": "string",
                    "state_or_region": "string",
                    "zip": "string",
                    "country_code": "AW",
                    "street_address_2": "string"
                },
                "created_at": "2019-08-24T14:15:22Z",
                "updated_at": "2019-08-24T14:15:22Z",
                "accessed_at": "string",
                "phone_number": "string",
                "email": "user@example.com",
                "customer_logo": {}
            },
            "created_by": "user@example.com",
            "platform_cid": "string"
        }
        return msp_create_tenant_data
