class TacHomePageSelectors:
    ACCT_NAME = "[data-testid=\"heading-heading-home\"]"
    SWITCH_ACCOUNT_BTN = "[data-testid=\"switch-account-btn\"]"
    WORKSPACE_ID = "[data-testid=\"account-id-val\"]"
    WORKSPACE_TYPE = "[data-testid=\"paragraph-account-type-val\"]"
    WORKSPACE_STATUS = "[data-testid=\"paragraph-account-status-val\"]"
    CARD_WORKSPACE_DETAILS = "[data-testid=\"card-account_details\"]"
    CARD_MANAGE_CCS = "[data-testid=\"manage-ccs-text-info\"]"


class TacSideMenuSelectors:
    NOTIFICATIONS_LINK = "[data-testid=\"desc-notifications-link\"]"
    CUSTOMERS_LINK = "[data-testid=\"desc-customers-link\"]"
    USERS_LINK = "[data-testid=\"desc-users-link\"]"
    DEVICES_LINK = "[data-testid=\"desc-devices-link\"]"
    ORDERS_LINK = "[data-testid=\"desc-orders-link\"]"
    SUBSCRIPTIONS_LINK = "[data-testid=\"desc-subscriptions-link\"]"
    FIRMWARE_LINK = "[data-testid=\"desc-firmware-link\"]"
    APPLICATIONS_LINK = "[data-testid=\"desc-applications-link\"]"
    WHATS_NEW_LINK = "[data-testid=\"desc-whats-new-link\"]"
    MENU_LINK_TEMPLATE = "div[data-testid$=\"-link\"]:has-text(\"{}\")"


class TacCustomersSelectors:
    SEARCH_FIELD = "[data-testid=\"search-field\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"


class TacCustomerDetailsSelectors:
    BACK_TO_CUSTOMERS_BUTTON = "[data-testid=\"back-btn\"]"
    TABS_TEMPLATE = "div[data-testid$=\"-tab\"]:has-text(\"{}\")"

    ADD_DEVICE_BTN = "[data-testid=\"add-device-btn\"]"
    EXPORT_DEVICES_BTN = "[data-testid=\"export-devices-btn\"]"
    MANAGE_AUTO_SUBSCRIBE_BTN = "[data-testid=\"manage-auto-subscription-btn\"]"
    ACTIONS_BTN = "[data-testid=\"bulk-actions\"]"
    MOVE_TO_FOLDER_BTN = "[data-testid=\"move-to-folder-btn\"]"
    EXPORT_SELECTED_BTN = "[data-testid=\"export-selected-btn\"]"
    MANAGE_LOCATION_BTN = "[data-testid=\"manage-location-btn\"]"
    SERVICE_DELIVERY_CONTACT_BTN = "[data-testid=\"service-delivery-contact-btn\"]"
    FOLDER_NAME_DROPDOWN = "[data-testid=\"folder-name-input\"]"
    MOVE_TO_FOLDER_ACTION_BTN = "[data-testid=\"move-to-folder-action-btn\"]"
    MOVE_CONFIRMATION_BTN = "[data-testid=\"move-confirmation-btn\"]"

    CREATE_FOLDER_BTN = "[data-testid=\"create-folder-btn\"]"
    FOLDER_NAME_INPUT = "[data-testid=\"folder-name-input\"]"
    PARENT_NAME_DROPDOWN = "button:has([data-testid=\"parent-name-input\"])"
    DESCRIPTION_INPUT = "[data-testid=\"description-input\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    POPUP_CREATE_BTN = "[data-testid=\"create-btn\"]"

    CREATE_ALIAS_BTN = "[data-testid=\"create-folder-btn\"]:has-text(\"Add Alias\")"
    ALIAS_NAME_INPUT_FIELD = "[data-testid=\"alias-input\"]"
    ALIAS_TYPE_DROPDOWN = "[data-testid=\"alias-type-input\"]"
    POPUP_ADD_BTN = "[data-testid=\"add-btn\"]"
    ITEM_MENU_BUTTON = "button[aria-label='Open Drop']"
    DELETE_ALIAS_MENU_ITEM = "button:has-text('Delete Alias')"
    EDIT_ALIAS_MENU_ITEM = "button:has-text('Delete Alias')"
    POPUP_DELETE_BTN = "[data-testid=\"delete-btn\"]"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"
    TABLE_ROW_CHECKBOX_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({}) div:has(>input[type=\"checkbox\"])"
    TABLE_ROW_COLUMN_TEMPLATE = \
        "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>td:nth-of-type({column_index})," \
        "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>th:nth-of-type({column_index})"


class TacDevicesSelectors:
    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    FILTER_SEARCH_BTN = "[data-testid=\"filter-search-btn\"]"
    ADD_EXCEPTION_DEVICE_BTN = "[data-testid=\"add-exception-device-btn\"]"
    MOVE_DEVICE_BTN = "[data-testid=\"move-device-btn\"]"

    SERIALS_OR_MACS_FIELD = "[data-testid=\"serial-numbers-or-macs-text-area-formfield-area\"]"
    PCID_INPUT_FIELD = "[data-testid=\"pcid-input-input\"]"
    CUST_ID_SEARCH_BTN = "[data-testid=\"search-btn\"]"
    FOLDER_SELECT_DROPDOWN = "button[aria-label=\"Select\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    MOVE_DEVICES_ACTION_BTN = "[data-testid=\"move-devices-action-btn\"]"
    MOVED_DEVICES_POPUP_TITLE = "[data-testid=\"heading-progress-modal-title\"]:has-text(\"Devices moved\")"
    ERROR_MESSAGE_AREA = "[data-testid=\"text-form-global-error-message\"]"
    CLOSE_BTN = "[data-testid=\"close-btn\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"
    TABLE_ROW_CHECKBOX_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({}) div:has(>input[type=\"checkbox\"])"
    TABLE_ROW_COLUMN_TEMPLATE = \
        "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>td:nth-of-type({column_index})," \
        "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>th:nth-of-type({column_index})"


class TacDeviceDetailsSelectors:
    DEVICES_BTN = "[data-testid=\"devices-btn\"]"
    CUSTOMER_ID_BTN = "[data-testid=\"customer_id_btn\"]"
    EDIT_DEVICE_DETAILS_BTN = "[data-testid=\"edit-device-details-btn\"]"

    MAC_ADDRESS_VALUE = "[data-testid=\"text-mac_address-value\"]"
    SERIAL_NUMBER_VALUE = "[data-testid=\"text-serial_number-value\"]"
    PART_NUMBER_VALUE = "[data-testid=\"text-part_number-value\"]"
    FOLDER_NAME_VALUE = "[data-testid=\"text-folder_name-value\"]"
    PCID_VALUE = "[data-testid=\"text-platform_customer_id-value\"]"
