class TacHomePageSelectors:
    ACCT_NAME = "[data-testid=\"heading-heading-home\"]"
    SWITCH_ACCOUNT_BTN = "[data-testid=\"switch-account-btn\"]"
    WORKSPACE_ID = "[data-testid=\"account-id-val\"]"
    WORKSPACE_TYPE = "[data-testid=\"paragraph-account-type-val\"]"
    WORKSPACE_STATUS = "[data-testid=\"paragraph-account-status-val\"]"
    CARD_WORKSPACE_DETAILS = "[data-testid=\"card-account_details\"]"
    CARD_MANAGE_CCS = "[data-testid=\"manage-ccs-text-info\"]"


class TacNotificationsSelectors:
    MENU_LINK_TEMPLATE = "div[data-testid$=\"-link\"]:has-text(\"{}\")"


class TacCustomersSelectors:
    MENU_LINK_TEMPLATE = "div[data-testid$=\"-link\"]:has-text(\"{}\")"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"


class TacCustomerDetailsSelectors:
    TABS_TEMPLATE = "div[data-testid$=\"-tab\"]:has-text(\"{}\")"

    CREATE_FOLDER_BTN = "[data-testid=\"create-folder-btn\"]"
    FOLDER_NAME_INPUT = "[data-testid=\"folder-name-input\"]"
    PARENT_NAME_DROPDOWN = "button:has([data-testid=\"parent-name-input\"])"
    DESCRIPTION_INPUT = "[data-testid=\"description-input\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    POPUP_CREATE_BTN = "[data-testid=\"create-btn\"]"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"
