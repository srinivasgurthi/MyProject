import logging
from logging import DEBUG

log = logging.getLogger(__name__)


class SmInputPayload(object):
    pod_namespace: str = ""
    log_level = DEBUG

    def subs_data_default(self):
        subs_data_payload_default = {
            "reason": "Creation",
            "quote": "string",
            "contract": "string",
            "entitlements": [
                {
                    "lineItem": "string",
                    "quote": "string",
                    "contract": "string",
                    "licenses": [
                        {
                            "id": "string",
                            "customer": {
                                "id": "string",
                                "phone": "string",
                                "postal_code": "string",
                                "address": "string",
                                "city": "string",
                                "state": "str",
                                "country": "str",
                                "company_name": "string",
                                "email": "string"
                            },
                            "qty": "string",
                            "available_qty": "string",
                            "appointments": {
                                "subscriptionStart": "string",
                                "subscriptionEnd": "string",
                                "executionDate": "string",
                                "suspensionDate": "string",
                                "cancellationDate": "string",
                                "reactivationDate": "string",
                                "duration": "string",
                                "activationDate": "string",
                                "delayedActivation": "string",
                                "autoRenewalDate": "string"
                            },
                            "devices": [
                                {
                                    "serial": "string",
                                    "material": "string"
                                }
                            ]
                        }
                    ],
                    "product": {
                        "sku": "string",
                        "legacy": "string",
                        "description": "string",
                        "attributes": [
                            {
                                "name": "string",
                                "value": "string",
                                "nameDisplay": "string",
                                "valueDisplay": "string"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "string",
                            "value": "string"
                        }
                    ]
                }
            ],
            "activate": {
                "soldTo": "string",
                "soldToName": "string",
                "soldToEmail": "string",
                "shipTo": "string",
                "shipToName": "string",
                "shipToEmail": "string",
                "endUser": "string",
                "endUserName": "string",
                "endUserEmail": "string",
                "reseller": "string",
                "resellerName": "string",
                "resellerEmail": "string",
                "po": "string",
                "resellerPo": "string",
                "endUserPo": "string",
                "orderClass": "string",
                "party": {
                    "id": "string",
                    "function": "AG",
                    "country_id": "string",
                    "global_id": "string"
                },
                "parties": [
                    {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string"
                    }
                ],
                "contacts": [
                    {
                        "id": "string",
                        "function": "SM"
                    }
                ]
            },
            "customer": {
                "phone": "string",
                "postal_code": "string",
                "address": "string",
                "city": "string",
                "state": "str",
                "country": "str",
                "company_name": "string",
                "email": "string",
                "mdm": "string",
                "MDM": "string"
            },
            "smcCode": "string",
            "aasType": "IAAS"
        }
        return subs_data_payload_default

    def subs_data_AP(self):
        subs_data_AP_payload = {
            "reason": "Creation",
            "quote": "3100000453",
            "contract": "5100000111",
            "smcCode": "E",
            "customer": {
                "MDM": "1000937777",
                "phone": "50179505",
                "postal_code": "164 40",
                "address": "Torshamnsgatan 21-23",
                "city": "Kista",
                "country": "SE",
                "state": "",
                "company_name": "ERICSSON AB EAB",
                "email": "goran.matovic@ericsson.com"
            },
            "activate": {
                "soldTo": "Kronborgsgränd 7 Kista SE",
                "soldToName": "ARROW ECS SWEDEN AB",
                "soldToEmail": "ap.ecs.dk@arrow.com",
                "shipTo": "Torshamnsgatan 21-23 Kista SE",
                "shipToName": "ERICSSON AB EAB",
                "shipToEmail": "ptp.incident.management@ericsson.com",
                "endUser": "txpsojc",
                "endUserName": "txpsojc",
                "endUserEmail": "goran.matovic@ericsson.com",
                "reseller": "Kronborgsgränd 1 Kista SE",
                "resellerName": "ATEA SVERIGE AB",
                "resellerEmail": "levresk@atea.se",
                "po": "ARSW_TST4",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000937777",
                    "countryId": "120771848",
                    "globalId": "120771846"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994"
                    },
                    {
                        "function": "WE",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846"
                    },
                    {
                        "function": "RE",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994"
                    },
                    {
                        "function": "RG",
                        "id": "1000831628",
                        "countryId": "121140995",
                        "globalId": "121140994"
                    },
                    {
                        "function": "Z1",
                        "id": "1001063567",
                        "countryId": "121148324",
                        "globalId": "121148323"
                    },
                    {
                        "function": "ZC",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846"
                    },
                    {
                        "function": "ZE",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846"
                    },
                    {
                        "function": "ZL",
                        "id": "1000937777",
                        "countryId": "120771848",
                        "globalId": "120771846"
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000202677",
                        "countryId": None,
                        "globalId": None
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000030",
                    "quote": "3100000453",
                    "contract": "5100000111",
                    "total_qty": "100.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "Q9Y59AAS",
                        "legacy": "",
                        "description": "Aruba Central AP Fnd 3yr Sub SaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PREPAID_AMT|PRICING_MODEL",
                                "nameDisplay": "Characteristic Name"
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term"
                            },
                            {
                                "name": "TIER_AP",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Access Point Tier"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Contract Type"
                        },
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier"
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Technical Support"
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "General Technical Guidance"
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure"
                        },
                        {
                            "name": "CS_TCS_RESPONSE_TIME",
                            "value": "2HR",
                            "valueDisplay": "2 Hours",
                            "nameDisplay": "Response Time"
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure"
                        },
                        {
                            "name": "CS_TCS_COV_WINDOW7",
                            "value": "24",
                            "valueDisplay": "24 Hours",
                            "nameDisplay": "Coverage Window 24x7"
                        },
                        {
                            "name": "TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term"
                        },
                        {
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Collaborative Supp and Assist"
                        },
                        {
                            "name": "CS_TCS_SERVICE_LEVEL",
                            "value": "ESS",
                            "valueDisplay": "Essential",
                            "nameDisplay": "Service Level"
                        },
                        {
                            "name": "CS_TERM",
                            "value": "3",
                            "valueDisplay": "3",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHCUECD6U66",
                            "qty": "100.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "04.01.2023 00:00:00",
                                "subscriptionEnd": "04.01.2026 00:00:00",
                                "suspensionDate": None,
                                "cancellationDate": None,
                                "reactivationDate": None,
                                "activationDate": "04.01.2023 14:26:59",
                                "duration": "3",
                                "delayedActivation": None,
                                "autoRenewalDate": None
                            }
                        }
                    ]
                }
            ]
        }
        return subs_data_AP_payload
