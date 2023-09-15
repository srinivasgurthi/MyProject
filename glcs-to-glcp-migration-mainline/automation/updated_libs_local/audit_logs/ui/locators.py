class AuditLogsSelectors:
    LOADER_SPINNER = "[data-testid*=\"loader-spinner\"]"
    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    NO_AUDIT_LOG_DATA = "[data-testid='no-audit-log-data']"
    TABLE_ROWS_COUNT = "[data-testid=\"table-summary\"]>div>div:first-of-type>span"
    AUDIT_LOGS_TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    AUDIT_LOG_DESCRIPTION = "[data-testid=\"heading-audit-log-details\"] div"
    DETAIL_CLOSE_BUTTON = "[data-testid=\"close-button\"]"
    AUDIT_LOG_SM_ITEM_TEMPLATE = "tr:has-text(\"Subscription Management\") td:has-text(\"{}\")"
    AUDIT_LOG_ADDED_DEV_ITEM_TEMPLATE = "tr:has-text(\"Device Management\") td:has-text(\"{}\")"
    LOG_ENTRY_CHECK = "(//span[contains(., '{category}')]/ancestor::tr[contains(.,'{description}') and \
    contains(., '{user_name}') and contains(., '{account_name}')])[1]"
