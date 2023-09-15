import logging
from logging import DEBUG

log = logging.getLogger(__name__)


class SmInputPayload:

    @staticmethod
    def subs_data_default():
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

    @staticmethod
    def subs_data_ap():
        subs_data_ap_payload = {
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
        return subs_data_ap_payload

    @staticmethod
    def subs_data_sw_6200():
        null = None
        subs_data_sw_6200_payload = {
            "reason": "Creation",
            "quote": "6000210273",
            "contract": "2000043261",
            "smcCode": "E",
            "customer": {
                "MDM": "1000023264",
                "phone": "",
                "postal_code": "33760-3155",
                "address": "5350 Tech Data Dr",
                "city": "Clearwater",
                "country": "US",
                "state": "",
                "company_name": "TECH DATA CORPORATION",
                "email": "Simha@gmail.com"
            },
            "activate": {
                "soldTo": "44201 Nobel Drive FREMONT US",
                "soldToName": "TD SYNNEX CORPORATION",
                "soldToEmail": "narahari.n@hpe.com",
                "shipTo": "5350 Tech Data Dr Clearwater US",
                "shipToName": "TECH DATA CORPORATION",
                "shipToEmail": "",
                "endUser": "5350 Tech Data Dr Clearwater US",
                "endUserName": "TECH DATA CORPORATION",
                "endUserEmail": "Simha@gmail.com",
                "reseller": "300 Spectrum Center Dr Ste 100 Irvine US",
                "resellerName": "ENTERPRISE COMPUTING SOLUTIONS, INC.",
                "resellerEmail": "kollisetti@hpe.com",
                "po": "TEST-341RAMP",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000023264",
                    "countryId": "121482897",
                    "globalId": "121105452"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    },
                    {
                        "function": "WE",
                        "id": "2002082346",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RE",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    },
                    {
                        "function": "RG",
                        "id": "1000939629",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    },
                    {
                        "function": "Z1",
                        "id": "1000023046",
                        "countryId": "120424886",
                        "globalId": "120424885"
                    },
                    {
                        "function": "ZC",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    },
                    {
                        "function": "ZE",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    },
                    {
                        "function": "ZL",
                        "id": "1000023264",
                        "countryId": "121482897",
                        "globalId": "121105452"
                    }
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "9000975555",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RT",
                        "id": "9001139386",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZG",
                        "id": "9000125290",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000210273",
                    "contract": "2000043261",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "Q9Y76AAS",
                        "legacy": "",
                        "description": "Aruba Central 62/29xx F 7y SaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "BILLING FREQUENCY"
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "84",
                                "valueDisplay": "84",
                                "nameDisplay": "Term In Months"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "84",
                                "valueDisplay": "84",
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
                                "value": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|FIXED_COMMITMENT|PRICING_MODEL",
                                "nameDisplay": "HIDE CHARACTERISTICS"
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Paid Upfront",
                                "nameDisplay": "INVOICING MODEL"
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_SW",
                                "valueDisplay": "Central_SW",
                                "nameDisplay": "Product ID for CC"
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "TERM",
                                "value": "7",
                                "valueDisplay": "7",
                                "nameDisplay": "Term"
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN002AAS",
                                "valueDisplay": "JN002AAS",
                                "nameDisplay": "Product ID"
                            },
                            {
                                "name": "SW_FAMILY",
                                "value": "62XX",
                                "valueDisplay": "62XX",
                                "nameDisplay": "Switch Family"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier"
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure"
                        },
                        {
                            "name": "TERM",
                            "value": "7",
                            "valueDisplay": "7",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHUYHH5AHC6",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "21.03.2023 00:00:00",
                                "subscriptionEnd": "21.03.2030 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "07.03.2023 08:25:40",
                                "duration": "7",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return subs_data_sw_6200_payload

    @staticmethod
    def subs_data_sw_6300():
        null = None
        subs_data_sw_6300_payload = {
            "reason": "Creation",
            "quote": "6000212238",
            "contract": "2000043706",
            "smcCode": "E",
            "aasType": "IAAS",
            "customer": {
                "MDM": "1013199818",
                "phone": "",
                "postal_code": "70124",
                "address": "8000 Lakeshore Dr",
                "city": "New Orleans",
                "country": "US",
                "state": "LA",
                "company_name": "LANDRYS",
                "email": "kevin.balmaceda@hpe.com"
            },
            "activate": {
                "soldTo": "8000 Lakeshore Dr New Orleans US",
                "soldToName": "LANDRYS",
                "soldToEmail": "",
                "shipTo": "8000 Lakeshore Dr New Orleans US",
                "shipToName": "LANDRYS",
                "shipToEmail": "alma.ber.garcia-soto@hpe.com",
                "endUser": "8000 Lakeshore Dr New Orleans US",
                "endUserName": "LANDRYS",
                "endUserEmail": "kevin.balmaceda@hpe.com",
                "po": "end2end27_03",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1013199818",
                    "countryId": null,
                    "globalId": null
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "WE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZC",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZL",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000990693",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000070",
                    "quote": "6000212238",
                    "contract": "2000043706",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "FSB_ARUBA_AGG",
                        "legacy": "",
                        "description": "FSB ARUBA AGG",
                        "attributes": [
                            {
                                "name": "CS_AGG_CORE_HW",
                                "value": "JL662A",
                                "valueDisplay": "JL662A 24G CL4 PoE 4SFP56",
                                "nameDisplay": "Aruba Agg Switch HW"
                            },
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_NET_TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Aruba Tier Values"
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term In Months"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "BILL_FREQ|CS_PRODUCT_ID|EVERGREEN|HP_BASIC_CHOICES|HP_STD_COMPONENT|INVOICING_MODEL|NO_OF_SW|SDCOM_VKOND|TIER",
                                "valueDisplay": "BILL_FREQ|CS_PRODUCT_ID|EVERGREEN|HP_BASIC_CHOICES|HP_STD_COMPONENT|INVOICING_MODEL|NO_OF_SW|SDCOM_VKOND|TIER",
                                "nameDisplay": "HIDE CHARACTERISTICS"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "SW_FAMILY",
                                "value": "63XX",
                                "valueDisplay": "63XX",
                                "nameDisplay": "Switch Family"
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "BILLING FREQUENCY"
                            },
                            {
                                "name": "CS_NET_HW_VAR",
                                "value": "JL086A-1#ABA",
                                "valueDisplay": "JL086A-1#ABA",
                                "nameDisplay": "Concatenate of Loc./Reg. Opt."
                            },
                            {
                                "name": "CS_WIRE_POWER_SUPPLY",
                                "value": "JL086A-1",
                                "valueDisplay": "680W AC",
                                "nameDisplay": "Power Supply Options"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "CS_TERM_ALPHANUM",
                                "value": "_36",
                                "valueDisplay": "_36",
                                "nameDisplay": "Alphanumeric Value for Term"
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "INVOICING MODEL"
                            },
                            {
                                "name": "CS_NET_PWR_CORD",
                                "value": "#ABA",
                                "valueDisplay": "US",
                                "nameDisplay": "Aruba Localizations"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "HP_STD_COMPONENT",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "STD COMP FOR PLANNING"
                            },
                            {
                                "name": "CS_FOUND_CARE_SUPPORT",
                                "value": "NBDEXHW",
                                "valueDisplay": "Next Business Day HW Exchange",
                                "nameDisplay": "Foundation Care Support"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "IAASYGHUUU43UU66",
                            "qty": "1.000",
                            "devices": [
                                {
                                    "serial": "AB7812009668",
                                    "material": "R3V49A"
                                }
                            ],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "16.03.2023 00:00:00",
                                "subscriptionEnd": "16.03.2026 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "15.03.2023 12:58:11",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return subs_data_sw_6300_payload

    @staticmethod
    def subs_data_gw_70xx():
        null = None
        subs_data_gw_70xx_payload = {
            "reason": "Creation",
            "quote": "3100004030",
            "contract": "5100001114",
            "smcCode": "E",
            "customer": {
                "MDM": "1000439523",
                "phone": "671893450",
                "postal_code": "55543",
                "address": "Schwabenheimer Weg 8",
                "city": "Bad Kreuznach",
                "country": "DE",
                "state": "RP",
                "company_name": "TULLIUS SANITÄR - HEIZUNG GMBH",
                "email": "Florian.Loeffler@sz-group.de"
            },
            "activate": {
                "soldTo": "Kistlerhofstr. 75 Muenchen DE",
                "soldToName": "TECH DATA GMBH & CO. OHG",
                "soldToEmail": "",
                "shipTo": "Schwabenheimer Weg 8 Bad Kreuznach DE",
                "shipToName": "TULLIUS SANITÄR - HEIZUNG GMBH",
                "shipToEmail": "",
                "endUser": "Schwabenheimer Weg 8 Bad Kreuznach DE",
                "endUserName": "TULLIUS SANITÄR - HEIZUNG GMBH",
                "endUserEmail": "Florian.Loeffler@sz-group.de",
                "reseller": "Peutestr 53 Hamburg DE",
                "resellerName": "DATAGROUP HAMBURG GMBH",
                "resellerEmail": "",
                "po": "3100000978",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000439523",
                    "countryId": "121461853",
                    "globalId": "121461852"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1001065036",
                        "countryId": "121148353",
                        "globalId": "121148352"
                    },
                    {
                        "function": "WE",
                        "id": "1000439523",
                        "countryId": "121461853",
                        "globalId": "121461852"
                    },
                    {
                        "function": "RE",
                        "id": "1001065036",
                        "countryId": "121148353",
                        "globalId": "121148352"
                    },
                    {
                        "function": "RG",
                        "id": "1001065036",
                        "countryId": "121148353",
                        "globalId": "121148352"
                    },
                    {
                        "function": "Z1",
                        "id": "1000004052",
                        "countryId": "121493294",
                        "globalId": "121493293"
                    },
                    {
                        "function": "ZC",
                        "id": "1000439523",
                        "countryId": "121461853",
                        "globalId": "121461852"
                    },
                    {
                        "function": "ZE",
                        "id": "1000439523",
                        "countryId": "121461853",
                        "globalId": "121461852"
                    },
                    {
                        "function": "ZL",
                        "id": "1000439523",
                        "countryId": "121461853",
                        "globalId": "121461852"
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000247678",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100004030",
                    "contract": "5100001114",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JZ120AAS",
                        "legacy": "",
                        "description": "Aruba7/90xxGtwyFnd5yrSubSaaS",
                        "attributes": [
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "BILLING FREQUENCY"
                            },
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term In Months"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "TIER",
                                "value": "FO",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "INVOICING MODEL"
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type"
                            },
                            {
                                "name": "TERM",
                                "value": "5",
                                "valueDisplay": "5",
                                "nameDisplay": "Term"
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID"
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "7005",
                                "valueDisplay": "7005",
                                "nameDisplay": "Gateway Family"
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
                            "value": "5",
                            "valueDisplay": "5",
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
                            "value": "5",
                            "valueDisplay": "5",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHH2CG23DYG",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "24.02.2023 00:00:00",
                                "subscriptionEnd": "24.02.2028 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "24.02.2023 08:11:01",
                                "duration": "5",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return subs_data_gw_70xx_payload

    @staticmethod
    def subs_data_gw_72xx():
        null = None
        subs_data_gw_72xx_payload = {
            "reason": "Creation",
            "quote": "6000216574",
            "contract": "2000044016",
            "smcCode": "E",
            "customer": {
                "MDM": "1013199818",
                "phone": "",
                "postal_code": "70124",
                "address": "8000 Lakeshore Dr",
                "city": "New Orleans",
                "country": "US",
                "state": "LA",
                "company_name": "LANDRYS",
                "email": "kevin.balmaceda@hpe.com"
            },
            "activate": {
                "soldTo": "8000 Lakeshore Dr New Orleans US",
                "soldToName": "LANDRYS",
                "soldToEmail": "",
                "shipTo": "8000 Lakeshore Dr New Orleans US",
                "shipToName": "LANDRYS",
                "shipToEmail": "alma.ber.garcia-soto@hpe.com",
                "endUser": "8000 Lakeshore Dr New Orleans US",
                "endUserName": "LANDRYS",
                "endUserEmail": "kevin.balmaceda@hpe.com",
                "po": "6000216574",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1013199818",
                    "countryId": null,
                    "globalId": null
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "WE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RG",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZC",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZE",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZL",
                        "id": "1013199818",
                        "countryId": null,
                        "globalId": null
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000990693",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6000216574",
                    "contract": "2000044016",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "JZ198AAS",
                        "legacy": "",
                        "description": "Aruba72xxGatewayAdv1yrSubSaaS",
                        "attributes": [
                            {
                                "name": "TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term In Months"
                            },
                            {
                                "name": "TIER",
                                "value": "AD",
                                "valueDisplay": "Advanced",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "HIDE_CHAR",
                                "value": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "valueDisplay": "COMMITMENT_VALUE1|EVERGREEN|FIXED_COMMITMENT|PRICING_MODEL",
                                "nameDisplay": "HIDE CHARACTERISTICS"
                            },
                            {
                                "name": "TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit of Measure"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term"
                            },
                            {
                                "name": "PRODUCT_ID",
                                "value": "JN003AAS",
                                "valueDisplay": "JN003AAS",
                                "nameDisplay": "Product ID"
                            },
                            {
                                "name": "GW_FAMILY",
                                "value": "7200",
                                "valueDisplay": "7200",
                                "nameDisplay": "Gateway Family"
                            },
                            {
                                "name": "BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "BILLING FREQUENCY"
                            },
                            {
                                "name": "SP_HIDE_CHAR1",
                                "value": "TERM",
                                "valueDisplay": "TERM",
                                "nameDisplay": "Characteristic Name"
                            },
                            {
                                "name": "SP_HIDE_CHAR2",
                                "value": "TERM_UOM",
                                "valueDisplay": "TERM_UOM",
                                "nameDisplay": "Characteristic Name"
                            },
                            {
                                "name": "TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "INVOICING MODEL"
                            },
                            {
                                "name": "PRODUCT_CC",
                                "value": "CENTRAL_GW",
                                "valueDisplay": "Central_GW",
                                "nameDisplay": "Product ID for CC"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "GW_TYPE",
                                "value": "SDWAN",
                                "valueDisplay": "SDWAN",
                                "nameDisplay": "Gateway Type"
                            },
                            {
                                "name": "TIER_GW",
                                "value": "AD",
                                "valueDisplay": "Advanced",
                                "nameDisplay": "Gateway Tier"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care",
                            "nameDisplay": "Support Tier"
                        },
                        {
                            "name": "TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit of Measure"
                        },
                        {
                            "name": "CS_TERM_UOM",
                            "value": "Y",
                            "valueDisplay": "Year(s)",
                            "nameDisplay": "Term Unit Of Measure"
                        },
                        {
                            "name": "TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term"
                        },
                        {
                            "name": "CS_TERM",
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "PAYGHJ3U3E4HTE",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "21.03.2023 00:00:00",
                                "subscriptionEnd": "21.03.2024 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "21.03.2023 07:24:52",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return subs_data_gw_72xx_payload

    @staticmethod
    def vm_bakcup():
        null = None
        vm_backup_order = {
            "reason": "Creation",
            "quote": "SERTEST007",
            "contract": "SERTEST007",
            "trial": True,
            "smcCode": "code",
            "customer": {
                "MDM": "SERTEST007",
                "phone": "3747702",
                "postal_code": "109841",
                "address": "1 Depot Close",
                "city": "Singapore",
                "country": "SG",
                "state": 'ca',
                "company_name": "HEWLETT-PACKARD ASIA PACIFIC PTE.",
                "email": "jeremy.lee@hpe.com"
            },
            "activate": {
                "soldTo": "51 Tai Seng Avenue #05-01 Pixe Singapore SG",
                "soldToName": "HEWLETT-PACKARD SINGAPORE(SALES)PTE",
                "soldToEmail": "default@gmail.com",
                "shipTo": "1 Depot Close Singapore SG",
                "shipToName": "HEWLETT-PACKARD ASIA PACIFIC PTE. LTD.",
                "shipToEmail": "default@gmail.com",
                "endUser": "1 Depot Close Singapore SG",
                "endUserName": "FLORENCE SPRINT6 SM TEST1",
                "endUserEmail": "jeremy.lee@hpe.com",
                "po": "PONUMCCS_09_170120_SERTEST007",
                "resellerPo": "SERTEST007",
                "endUserPo": "SERTEST007",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "SERTEST007",
                    "countryId": "122394339",
                    "globalId": "122394308"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "WE",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308"
                    },
                    {
                        "function": "RE",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZC",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308"
                    },
                    {
                        "function": "ZE",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308"
                    },
                    {
                        "function": "ZL",
                        "id": "SERTEST007",
                        "countryId": "122394339",
                        "globalId": "122394308"
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "SERTEST007",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "SERTEST007",
                    "contract": "SERTEST007",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R7A23AAE",
                        "legacy": null,
                        "description": "HPE GreenLake for Backup and Recovery 90 Day(s) Evaluation SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "EVAL",
                                "valueDisplay": "Evaluation",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "EBS,0|EC2,0|GB,0|VM,0",
                                "valueDisplay": "EBS,0|EC2,0|GB,0|VM,0",
                                "nameDisplay": "Concatenate UOM with Commit"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "EVERGREEN",
                                "value": "NO",
                                "valueDisplay": "NO",
                                "nameDisplay": "EVERGREEN"
                            },
                            {
                                "name": "CS_READ_ITM_TYPE",
                                "value": "ZQPV",
                                "valueDisplay": "ZQPV",
                                "nameDisplay": "Item Category"
                            },
                            {
                                "name": "CS_FIXED_COMMITMENT",
                                "value": "N",
                                "valueDisplay": "No",
                                "nameDisplay": "Fixed Commitment"
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "EBS|EC2|GB|VM",
                                "valueDisplay": "EBS|EC2|GB|VM",
                                "nameDisplay": "List of product unit of measur"
                            },
                            {
                                "name": "CS_USAGE_UOM1",
                                "value": "VM",
                                "valueDisplay": "VM",
                                "nameDisplay": "Unit Of Measure 1"
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R7A23AAE",
                                "valueDisplay": "R7A23AAE",
                                "nameDisplay": "Base Product ID"
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_EBS|CS_CCM_EC2|CS_CCM_GB|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_VM|CS_CLASSIC_PREPAID|CS_COMMITMENT_VALUE1|CS_COMMITMENT_VALUE2|CS_HW_LED_MANDATORY_SAAS|CS_PLATFORM|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER|CS_USAGE_UOM1|CS_USAGE_UOM2|EVERGREEN",
                                "valueDisplay": "CS_CCM_EBS|CS_CCM_EC2|CS_CCM_GB|CS_CCM_MULTIV_UOM|CS_CCM_MULTIV_UOM_CONC|CS_CCM_VM|CS_CLASSIC_PREPAID|CS_COMMITMENT_VALUE1|CS_COMMITMENT_VALUE2|CS_HW_LED_MANDATORY_SAAS|CS_PLATFORM|CS_PRICING_MODEL|CS_PRODUCT_CC|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2|CS_TIER|CS_USAGE_UOM1|CS_USAGE_UOM2|EVERGREEN",
                                "nameDisplay": "Characteristic Name"
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FN",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "CS_PRODUCT_CC",
                                "value": "VM_BACKUP",
                                "valueDisplay": "VM Backup",
                                "nameDisplay": "Product ID for CC"
                            },
                            {
                                "name": "CS_USAGE_UOM2",
                                "value": "GB",
                                "valueDisplay": "GB",
                                "nameDisplay": "Unit Of Measure 2"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "D",
                                "valueDisplay": "Day(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "Software SupChain aaS Handling"
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range"
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "001",
                                "valueDisplay": "EVAL Configuration",
                                "nameDisplay": "Configuration Type"
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "90",
                                "valueDisplay": "90",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "SERTEST007GUAGY",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "10.03.2023 00:00:00",
                                "subscriptionEnd": "08.06.2023 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "10.03.2023 20:39:06",
                                "duration": "90",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return vm_backup_order

    @staticmethod
    def svc_dis_recovery_zerto():
        null = None
        dis_recovery_order = {
            "reason": "Creation",
            "quote": "6001998187",
            "contract": "6001998187",
            "smcCode": "E",
            "customer": {
                "MDM": "1010858407",
                "phone": "3054366718",
                "postal_code": "33172-2525",
                "address": "2100 NW 102ND Pl",
                "city": "DORAL",
                "country": "US",
                "state": "FL",
                "company_name": "WESTHAM TRADE COMPANY LIMITED",
                "email": "kvazquez@hpe.com"
            },
            "activate": {
                "soldTo": "2100 NW 102ND Pl DORAL US",
                "soldToName": "WESTHAM TRADE COMPANY LIMITED",
                "soldToEmail": "lkategaru@deloitte.com",
                "shipTo": "2100 NW 102ND Pl DORAL US",
                "shipToName": "WESTHAM TRADE COMPANY LIMITED",
                "shipToEmail": "lkategaru@deloitte.com",
                "endUser": "2100 NW 102ND Pl DORAL US",
                "endUserName": "Zerto ABC LIMITED",
                "endUserEmail": "kvazquez@hpe.com",
                "po": "zerto_test_01",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "6001998187",
                    "countryId": "6001998187",
                    "globalId": "6001998187"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "WE",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "RE",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "RG",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "ZC",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "ZE",
                        "id": "6001998187",
                        "countryId": "6001998187",
                        "globalId": "6001998187"
                    },
                    {
                        "function": "ZL",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    },
                    {
                        "function": "ZW",
                        "id": "1010858407",
                        "countryId": "120703851",
                        "globalId": "120703323"
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000166419",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "6001998187",
                    "contract": "6001998187",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "S1S62AAE",
                        "legacy": "",
                        "description": "HPE GreenLake Disaster Recovery Sub Foundation 3 Year(s) Monthly SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM_CONC",
                                "value": "VM,00",
                                "valueDisplay": "VM,00",
                                "nameDisplay": "Concatenate UOM with Commit"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_CCM_MULTIV_UOM",
                                "value": "VM",
                                "valueDisplay": "VM",
                                "nameDisplay": "List of product unit of measur"
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "S1S62AAE",
                                "valueDisplay": "S1S62AAE",
                                "nameDisplay": "Base Product ID"
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_CCM_MULTIV_UOM_CONC|CS_HW_LED_MANDATORY_SAAS|CS_PRICING_MODEL|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER",
                                "valueDisplay": "CS_CCM_MULTIV_UOM_CONC|CS_HW_LED_MANDATORY_SAAS|CS_PRICING_MODEL|CS_PRODUCT_ID|CS_RANGE|CS_SCREEN_DEP_INVISIBLE|CS_SDCOM_VKOND|CS_SWSC_AAS_HANDLING|CS_TIER",
                                "nameDisplay": "Screen Dep Invisible"
                            },
                            {
                                "name": "CS_TIER",
                                "value": "FN",
                                "valueDisplay": "Foundation",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "CS_CCM_VM",
                                "value": "UP TO 100",
                                "valueDisplay": "UP TO 100",
                                "nameDisplay": "Commit Value VM"
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "SVC",
                                "valueDisplay": "Service",
                                "nameDisplay": "Software SupChain aaS Handling"
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "STO",
                                "valueDisplay": "Storage",
                                "nameDisplay": "Range"
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type"
                            },
                            {
                                "name": "CS_PRICING_MODEL",
                                "value": "TIER",
                                "valueDisplay": "Tier",
                                "nameDisplay": "Pricing Model"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [],
                    "licenses": [
                        {
                            "id": "YGGZERTO6UTT",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "20.10.2022 00:00:00",
                                "subscriptionEnd": "20.10.2025 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "20.10.2022 20:48:19",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return dis_recovery_order

    @staticmethod
    def subs_compute_iaas():
        null = None
        sub_compute_iaas = {
            "reason": "Creation",
            "quote": "COMPRO0001",
            "contract": "COMPRO0001",
            "smcCode": "E",
            "customer": {
                "MDM": "COMPRO0001",
                "phone": "2078430200",
                "postal_code": "LS12 6EH",
                "address": "7 Brown Lane West",
                "city": "LEEDS",
                "country": "GB",
                "state": "",
                "company_name": "NG BAILEY IT SERVICES LIMITED",
                "email": "shreyast@gmail.com"
            },
            "activate": {
                "soldTo": "REDWOOD 2, CROCKFORD LANE CHIN BASINGSTOKE GB",
                "soldToName": "TECH DATA LIMITED",
                "soldToEmail": "suresh.bhojani@cibc.co.uk",
                "shipTo": "7 Brown Lane West LEEDS GB",
                "shipToName": "NG BAILEY IT SERVICES LIMITED",
                "shipToEmail": "",
                "endUser": "7 Brown Lane West LEEDS GB",
                "endUserName": "FLORENCE SPRINT6 SM TEST1",
                "endUserEmail": "shreyast@gmail.com",
                "reseller": "ADMINISTRATION CENTRE HATFIELD HATFIELD GB",
                "resellerName": "COMPUTACENTER (UK) LIMITED",
                "resellerEmail": "Ashokkumar.Thangavelu@telefonica.com",
                "po": "16152_PO_COMPRO0001",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "COMPRO0001",
                    "countryId": "120243194",
                    "globalId": "120243012"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "WE",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RE",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "RG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "Z1",
                        "id": "COMPRO0001",
                        "countryId": "120762923",
                        "globalId": "120762922"
                    },
                    {
                        "function": "ZC",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    },
                    {
                        "function": "ZE",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    },
                    {
                        "function": "ZL",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    }
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RT",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZG",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "COMPRO0001",
                    "contract": "COMPRO0001",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R6Z88AAE",
                        "legacy": "",
                        "description": "HPE GreenLake COM St 1y Up ProLiant aaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "CS_HW_LED_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months"
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "PROLIANT",
                                "valueDisplay": "ProLiant",
                                "nameDisplay": "Platform"
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R6Z73AAE",
                                "valueDisplay": "R6Z73AAE",
                                "nameDisplay": "Base Product ID"
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible"
                            },
                            {
                                "name": "CS_TIER",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling"
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range"
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type"
                            },
                            {
                                "name": "CS_TIER_POSITANO",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier for Positano"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type"
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Technical Support"
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "General Technical Guidance"
                        },
                        {
                            "name": "CS_SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care 24x7",
                            "nameDisplay": "Support Tier"
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
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
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
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "COMPRO0001J73UC26",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "16.03.2023 00:00:00",
                                "subscriptionEnd": "16.03.2024 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "16.03.2023 00:00:00",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return vm_backup_order

    @staticmethod
    def subs_compute_iaas():
        null = None
        sub_compute_iaas = {
            "reason": "Creation",
            "quote": "COMPRO0001",
            "contract": "COMPRO0001",
            "smcCode": "E",
            "customer": {
                "MDM": "COMPRO0001",
                "phone": "2078430200",
                "postal_code": "LS12 6EH",
                "address": "7 Brown Lane West",
                "city": "LEEDS",
                "country": "GB",
                "state": "",
                "company_name": "NG BAILEY IT SERVICES LIMITED",
                "email": "shreyast@gmail.com"
            },
            "activate": {
                "soldTo": "REDWOOD 2, CROCKFORD LANE CHIN BASINGSTOKE GB",
                "soldToName": "TECH DATA LIMITED",
                "soldToEmail": "suresh.bhojani@cibc.co.uk",
                "shipTo": "7 Brown Lane West LEEDS GB",
                "shipToName": "NG BAILEY IT SERVICES LIMITED",
                "shipToEmail": "",
                "endUser": "7 Brown Lane West LEEDS GB",
                "endUserName": "FLORENCE SPRINT6 SM TEST1",
                "endUserEmail": "shreyast@gmail.com",
                "reseller": "ADMINISTRATION CENTRE HATFIELD HATFIELD GB",
                "resellerName": "COMPUTACENTER (UK) LIMITED",
                "resellerEmail": "Ashokkumar.Thangavelu@telefonica.com",
                "po": "16152_PO_COMPRO0001",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "COMPRO0001",
                    "countryId": "120243194",
                    "globalId": "120243012"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "WE",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RE",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "RG",
                        "id": "COMPRO0001",
                        "countryId": "121109504",
                        "globalId": "121109503"
                    },
                    {
                        "function": "Z1",
                        "id": "COMPRO0001",
                        "countryId": "120762923",
                        "globalId": "120762922"
                    },
                    {
                        "function": "ZC",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    },
                    {
                        "function": "ZE",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    },
                    {
                        "function": "ZL",
                        "id": "COMPRO0001",
                        "countryId": "120243194",
                        "globalId": "120243012"
                    }
                ],
                "contacts": [
                    {
                        "function": "CS",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "RT",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    },
                    {
                        "function": "ZG",
                        "id": "COMPRO0001",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "COMPRO0001",
                    "contract": "COMPRO0001",
                    "total_qty": "1.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R6Z88AAE",
                        "legacy": "",
                        "description": "HPE GreenLake COM St 1y Up ProLiant aaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "UP",
                                "valueDisplay": "Upfront",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "CS_HW_LED_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "0",
                                "valueDisplay": "0",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "12",
                                "valueDisplay": "12",
                                "nameDisplay": "Term in months"
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "PROLIANT",
                                "valueDisplay": "ProLiant",
                                "nameDisplay": "Platform"
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R6Z73AAE",
                                "valueDisplay": "R6Z73AAE",
                                "nameDisplay": "Base Product ID"
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible"
                            },
                            {
                                "name": "CS_TIER",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling"
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range"
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type"
                            },
                            {
                                "name": "CS_TIER_POSITANO",
                                "value": "ST",
                                "valueDisplay": "Standard",
                                "nameDisplay": "Tier for Positano"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "1",
                                "valueDisplay": "1",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type"
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "Technical Support"
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "Yes",
                            "nameDisplay": "General Technical Guidance"
                        },
                        {
                            "name": "CS_SUPPORT_TIER",
                            "value": "FC",
                            "valueDisplay": "Foundation Care 24x7",
                            "nameDisplay": "Support Tier"
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
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "Yes",
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
                            "value": "1",
                            "valueDisplay": "1",
                            "nameDisplay": "Term"
                        }
                    ],
                    "licenses": [
                        {
                            "id": "COMPRO0001J73UC26",
                            "qty": "1.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "16.03.2023 00:00:00",
                                "subscriptionEnd": "16.03.2024 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "16.03.2023 00:00:00",
                                "duration": "1",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }


        return sub_compute_iaas

    @staticmethod
    def subs_compute_alletra_4k():
        null = None
        sub_compute_alletra_4k = {
            "reason": "Creation",
            "quote": "3100005591",
            "contract": "5100001420",
            "smcCode": "E",
            "customer": {
                "MDM": "1000791811",
                "phone": "2124107500",
                "postal_code": "34418",
                "address": "NO:65 YESILCE MAHALLESI ESKI",
                "city": "Istanbul (Europe)",
                "country": "TR",
                "state": "",
                "company_name": "MEDIA MARKT TURKEY TICARET LIMITED",
                "email": "mozdemir@mediamarkt.com.tr"
            },
            "activate": {
                "soldTo": "ANEL IS MERKEZI NO:5 KAT:8 SAR Istanbul TR",
                "soldToName": "TECH DATA BILGISAYAR SISTEMLERI ANONIM SIRKETI",
                "soldToEmail": "",
                "shipTo": "NO:65 YESILCE MAHALLESI ESKI Istanbul (Europe) TR",
                "shipToName": "MEDIA MARKT TURKEY TICARET LIMITED SIRKETI",
                "shipToEmail": "rohit.reddy@hpe.com",
                "endUser": "NO:65 YESILCE MAHALLESI ESKI Istanbul (Europe) TR",
                "endUserName": "MEDIA MARKT TURKEY TICARET LIMITED SIRKETI",
                "endUserEmail": "mozdemir@mediamarkt.com.tr",
                "reseller": "Nil Tic Merkezi, Yesilce Mah., Istanbul (Europe) TR",
                "resellerName": "DESTEK BILG ILET OTOM SIST VE DAN HIZLERI YAZ SAN VE TIC LTD STI",
                "resellerEmail": "",
                "po": "123_TR",
                "resellerPo": "",
                "endUserPo": "",
                "orderClass": "ZBRIM",
                "party": {
                    "id": "1000791811",
                    "countryId": "121414137",
                    "globalId": "121414120"
                },
                "parties": [
                    {
                        "function": "AG",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498"
                    },
                    {
                        "function": "WE",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120"
                    },
                    {
                        "function": "RE",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498"
                    },
                    {
                        "function": "RG",
                        "id": "1000823619",
                        "countryId": "121414147",
                        "globalId": "120774498"
                    },
                    {
                        "function": "Z1",
                        "id": "1001698582",
                        "countryId": "120773664",
                        "globalId": "120773663"
                    },
                    {
                        "function": "ZC",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120"
                    },
                    {
                        "function": "ZE",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120"
                    },
                    {
                        "function": "ZL",
                        "id": "1000791811",
                        "countryId": "121414137",
                        "globalId": "121414120"
                    }
                ],
                "contacts": [
                    {
                        "function": "ZG",
                        "id": "9000642413",
                        "countryId": null,
                        "globalId": null
                    }
                ]
            },
            "entitlements": [
                {
                    "lineItem": "0000000010",
                    "quote": "3100005591",
                    "contract": "5100001420",
                    "total_qty": "100.000",
                    "available_qty": "0.00",
                    "product": {
                        "sku": "R6Z73AAE",
                        "legacy": "",
                        "description": "HPE GreenLake Cmp Ops Mgm Enhanced 3 Year(s) Monthly Alletra 4000 SaaS",
                        "attributes": [
                            {
                                "name": "CS_INVOICING_MODEL",
                                "value": "SU",
                                "valueDisplay": "Subscription",
                                "nameDisplay": "Invoicing Model"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MAX_2",
                                "value": "60",
                                "valueDisplay": "60",
                                "nameDisplay": "Term in months maximum"
                            },
                            {
                                "name": "CS_BILL_FREQ",
                                "value": "M",
                                "valueDisplay": "Monthly",
                                "nameDisplay": "Billing Frequency"
                            },
                            {
                                "name": "CS_HW_LED_MANDATORY_SAAS",
                                "value": "N",
                                "valueDisplay": "NO",
                                "nameDisplay": "HW Led Mandatory SaaS Flag"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS_MIN_2",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months minimum"
                            },
                            {
                                "name": "CS_TERM_IN_MONTHS",
                                "value": "36",
                                "valueDisplay": "36",
                                "nameDisplay": "Term in months"
                            },
                            {
                                "name": "CS_PLATFORM",
                                "value": "ALLETRA_4K",
                                "valueDisplay": "Alletra 4000",
                                "nameDisplay": "Platform"
                            },
                            {
                                "name": "CS_PRODUCT_ID",
                                "value": "R6Z73AAE",
                                "valueDisplay": "R6Z73AAE",
                                "nameDisplay": "Base Product ID"
                            },
                            {
                                "name": "CS_SCREEN_DEP_INVISIBLE",
                                "value": "CS_ERROR_LOG|CS_ERROR_TRGR|CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "valueDisplay": "CS_ERROR_LOG|CS_ERROR_TRGR|CS_HW_LED_MANDATORY_SAAS|CS_PRODUCT_ID|CS_RANGE|CS_SWSC_AAS_HANDLING|CS_TERM_IN_MONTHS|CS_TERM_IN_MONTHS_MAX_2|CS_TERM_IN_MONTHS_MIN_2",
                                "nameDisplay": "Screen Dep Invisible"
                            },
                            {
                                "name": "CS_TIER",
                                "value": "EN",
                                "valueDisplay": "Enhanced",
                                "nameDisplay": "Tier"
                            },
                            {
                                "name": "CS_TERM_UOM",
                                "value": "Y",
                                "valueDisplay": "Year(s)",
                                "nameDisplay": "Term Unit Of Measure"
                            },
                            {
                                "name": "CS_SWSC_AAS_HANDLING",
                                "value": "DEV",
                                "valueDisplay": "Device",
                                "nameDisplay": "Software SupChain aaS Handling"
                            },
                            {
                                "name": "CS_RANGE",
                                "value": "COM",
                                "valueDisplay": "Compute",
                                "nameDisplay": "Range"
                            },
                            {
                                "name": "CS_CONFIG_TYPE",
                                "value": "002",
                                "valueDisplay": "NON EVAL Configuration",
                                "nameDisplay": "Configuration Type"
                            },
                            {
                                "name": "CS_TERM",
                                "value": "3",
                                "valueDisplay": "3",
                                "nameDisplay": "Term"
                            }
                        ]
                    },
                    "support": [
                        {
                            "name": "CS_TCS_CONTRACT_TYPE",
                            "value": "TC",
                            "valueDisplay": "TechCare",
                            "nameDisplay": "Contract Type"
                        },
                        {
                            "name": "CS_TCS_TECH_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "Technical Support"
                        },
                        {
                            "name": "CS_TCS_TECH_GUIDANCE",
                            "value": "Y",
                            "valueDisplay": "年",
                            "nameDisplay": "General Technical Guidance"
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
                            "name": "CS_TCS_COLLAB_SUPPORT",
                            "value": "Y",
                            "valueDisplay": "年",
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
                            "id": "YGUAYAY3U7H6",
                            "qty": "100.000",
                            "devices": [],
                            "customer": {},
                            "appointments": {
                                "subscriptionStart": "29.03.2023 00:00:00",
                                "subscriptionEnd": "29.03.2026 00:00:00",
                                "suspensionDate": null,
                                "cancellationDate": null,
                                "reactivationDate": null,
                                "activationDate": "29.03.2023 14:50:00",
                                "duration": "3",
                                "delayedActivation": null,
                                "autoRenewalDate": null
                            }
                        }
                    ]
                }
            ]
        }
        return sub_compute_alletra_4k
