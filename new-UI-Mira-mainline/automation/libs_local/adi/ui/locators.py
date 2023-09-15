class DevicesInventorySelectors:
    LOADER_SPINNER = "[data-testid=\"devices-loader\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"

    DEVICE_PAGE_TITLE = "[data-testid=\"device-page-title\"]"
    ADD_DEVICE_BUTTON = "[data-testid=\"add-device-btn\"]"

    CARD_REQUIRE_ASSIGNMENTS = "[data-testid=\"card-require-assignments-tab\"]"
    CARD_REQUIRE_LICENSES = "[data-testid=\"card-require-licenses-tab\"]"
    CARD_ASSIGNED_LICENSED = "[data-testid=\"card-assigned-licensed-tab\"]"
    CARD_ALL_DEVICES = "[data-testid=\"card-all-devices-tab\"]"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    FILTER_BUTTON = "[data-testid=\"filter-search-btn\"]"
    ACTIONS_BUTTON = "[data-testid=\"bulk-actions\"]"
    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"


class ActivateDevicesSelectors:
    LOADER_SPINNER = "[data-testid=\"devices-loader\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-devices-page-title\"]"

    DEVICES_TAB_BUTTON = "[data-testid=\"devices-tab\"]"
    FOLDERS_TAB_BUTTON = "[data-testid=\"folders-tab\"]"
    DOCUMENTATION_TAB_BUTTON = "[data-testid=\"desc-activate-documentation-tab\"]"
    BACK_TO_MANAGE_BUTTON = "[data-testid=\"manage-account-btn\"]"

    DEVICES_ACTION_BTN = "[data-testid=\"devices-action-btn\"]"
    EXPORT_ALL_DEVICES_BTN = "[data-testid=\"export-btn\"]"
    EXPORT_POPUP_BTN = "[data-testid=\"export-action-btn\"]"
    GENERATE_TOKEN_BTN = "[data-testid=\"generate-token-btn\"]"
    ADD_DEVICES_BTN = "[data-testid=\"add-device-btn\"]"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    FOLDER_NAME_FILTER = "[data-testid=\"folder-name-input\"]"
    DEVICE_TYPE_FILTER = "[data-testid=\"device-type-dropdown\"]"
    MODELS_FILTER = "[data-testid=\"all-models-dropdown\"]"
    ACTIONS_BUTTON = "[data-testid=\"bulk-actions\"]"
    MOVE_TO_FOLDER_BUTTON = "[data-testid=\"move-to-folder-btn\"]"
    EXPORT_SELECTED_BUTTON = "[data-testid=\"export-selected-btn\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"
    TABLE_SUMMARY_COUNT = "[data-testid=\"table-summary\"]>div>div:nth-child(1)"

    POPUP_CONTINUE_BTN = "[data-testid=\"continue-btn\"]"
    POPUP_CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    CLOUD_ACTIVATION_KEY_INPUT = "[data-testid=\"cloud-activation-key-input\"]"
    MAC_ADDRESS_INPUT = "[data-testid=\"mac-address-input\"]"
    ADD_BTN = "[data-testid=\"add-button\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"


class ActivateFoldersSelectors:
    HEADING_PAGE_TITLE = "[data-testid=\"heading-folders-page-title\"]"

    DEVICES_TAB_BUTTON = "[data-testid=\"devices-tab\"]"
    FOLDERS_TAB_BUTTON = "[data-testid=\"folders-tab\"]"
    DOCUMENTATION_TAB_BUTTON = "[data-testid=\"desc-activate-documentation-tab\"]"
    BACK_TO_MANAGE_BUTTON = "[data-testid=\"manage-account-btn\"]"

    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    CREATE_FOLDER_BTN = "[data-testid=\"create-folder-btn\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"

    FOLDER_NAME_INPUT = "[data-testid=\"folder-name-input\"]"
    PARENT_NAME_DROPDOWN = "button:has([data-testid=\"parent-name-input\"])"
    DESCRIPTION_INPUT = "[data-testid=\"description-input\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    POPUP_CREATE_BTN = "[data-testid=\"create-btn\"]"


class DevicesHistorySelectors:
    LOADER_SPINNER = "[data-testid=\"devices-loader\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"

    DEVICE_HISTORY_TITLE = "[data-testid=\"heading-device-history\"]"
    EDIT_DEVICE_BUTTON = "[data-testid=\"edit-device-details-btn\"]"
    MOVE_TO_FOLDER_BUTTON = "[data-testid=\"move-to-folder-btn\"]"
    BACK_TO_DEVICES_BUTTON = "[data-testid=\"devices-btn\"]"
    PAGINATION_BAR = "[data-testid=\"pagination-device-history-table\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"


class AddDevicesSelectors:
    DEVICE_TYPE_DROPDOWN = "[data-testid=\"device-type-dropdown-wizard\"]"
    NEXT_BUTTON = "[data-testid=\"button-next\"]"
    ENTER_BUTTON = "[data-testid=\"enter-btn\"]"
    FINISH_BUTTON = "[data-testid=\"button-finish\"]"

    CSV_FILE_RADIO = "div[class*=\"Radio\"]:has(input[value=\"csv_file\"])"

    CLOUD_AND_MAC_RADIO = "div[class*=\"Radio\"]:has(input[value=\"cloud_activation_and_mac_address\"])"
    ACTIVATION_KEY_INPUT = "[data-testid=\"cloud-activation-key-input-wizard\"]"
    MAC_ADDRESS_INPUT_CLOUD = "[data-testid=\"mac-address-input-wizard\"]"

    SERIAL_AND_MAC_RADIO = "div[class*=\"Radio\"]:has(input[value=\"serial_number_and_mac_address\"])"
    SERIAL_NUMBER_INPUT = "[data-testid=\"serial-number-input\"]"
    MAC_ADDRESS_INPUT_SERIAL = "[data-testid=\"input-data-input\"]"

    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"

    DELIVERY_CONTACT_DROPDOWN = "[data-testid=\"service-delivery-contact-input\"]"
    DELIVERY_CONTACT_LIST_ITEM = "button[role=\"option\"]"

    VIEW_AUDIT_LOG_BTN = "[data-testid=\"view-audit-log-btn\"]"
    CLOSE_BTN = "[data-testid=\"close-btn\"]"


class ActivateFolderDetailsSelectors:
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"
    EDIT_FOLDER_BTN = "[data-testid=\"edit-folder-btn\"]"
    ADD_NEW_RULE_BTN = "[data-testid=\"add-new-rule-btn\"]"
    SEARCH_DEVICE_INPUT_FIELD = "[data-testid=\"search-field\"]"
    ACTIONS_MENU = "[data-testid=\"multipleactions-action-btn\"]"
    DELETE_FOLDER_MENU_ITEM = "[data-testid=\"action-0\"]"
    ACTIVATE_DEVICES_LINK = "[data-testid=\"devices-anchor-btn\"]"
    BACK_TO_FOLDERS_BUTTON = "[data-testid=\"folders-back-btn\"]"

    RULE_LIST_ROW_TEMPLATE = "[data-testid=\"rules-list\"]>div:has-text(\"{}\")>div"
    DELETE_RULE_BTN = "[data-testid=\"rule-delete-btn\"]"
    EDIT_RULE_BTN = "[data-testid=\"rule-edit-btn\"]"

    CONFIRM_POPUP_BUTTON = "[data-testid=\"create-btn\"]"
    CANCEL_POPUP_BUTTON = "[data-testid=\"cancel-btn\"]"
    OK_POPUP_BUTTON = "[data-testid=\"ok-btn\"]"

    SAVE_CHANGES_BTN = "[data-testid=\"save-changes-btn\"]"
    DISCARD_CHANGES_BTN = "[data-testid=\"discard-changes-btn\"]"
    FOLDER_NAME_INPUT_FIELD = "[data-testid=\"folder-input\"]"
    PARENT_FOLDER_MENU = "[data-testid=\"parent-folder-input\"]"
    DESCRIPTION_INPUT_FIELD = "[data-testid=\"description-input\"]"

    RULE_NAME_INPUT_FIELD = "[data-testid=\"rule-name-input\"]"
    RULE_TYPE_DROP_DOWN = "[data-testid=\"rule-type-input\"]"
    PARENT_FOLDER_DROP_DOWN = "[data-testid=\"folder-name-input\"]"
    EMAIL_ON_DROP_DOWN = "[data-testid=\"email-on-input\"]"
    EMAIL_TO_INPUT_FIELD = "[data-testid=\"email-to-input\"]"
    PROVISIONING_TYPE_DROP_DOWN = "[data-testid=\"provisioning-type-input\"]"
    FOR_RULE_DROP_DOWN = "[data-testid=\"for-rule-input\"]"
    AMP_IP_INPUT_FIELD = "[data-testid=\"amp-ip-input\"]"
    SHARED_SECRET_INPUT_FIELD = "[data-testid=\"shared-secret-input\"]"
    ORGANIZATION_INPUT_FIELD = "[data-testid=\"organization-input\"]"
    AP_GROUP_INPUT_FIELD = "[data-testid=\"ap-group-input\"]"
    CONTROLLER_INPUT_FIELD = "[data-testid=\"controller-input\"]"
    CONDUCTOR_MAC_DROP_DOWN = "[data-testid=\"controller-mac-input\"]"
    BACKUP_CONTROLLER_IP_INPUT_FIELD = "[data-testid=\"backup-controller-ip-input\"]"
    BACKUP_CTRL_IP_INPUT_FIELD = "[data-testid=\"backup-ctrl-ip-input\"]"
    BACKUP_CONDUCTOR_DROP_DOWN = "[data-testid=\"backup-controller-input\"]"
    BACKUP_MASTER_CONDUCTOR_DROP_DOWN = "[data-testid=\"backup-master-controller-input\"]"
    BACKUP_VPN_CONDUCTOR_MAC_DROP_DOWN = "[data-testid=\"backup-vpn-concentrator-mac-input\"]"
    VPN_CONCENTRATOR_MAC_DROP_DOWN = "[data-testid=\"vpn-concentrator-mac-input\"]"
    VPN_CONCENTRATOR_IP_INPUT_FIELD = "[data-testid=\"vpn-concentrator-ip-input\"]"
    PRIMARY_CONTROLLER_DROP_DOWN = "[data-testid=\"primary-controller-input\"]"
    COUNTRY_CODE_DROP_DOWN = "[data-testid=\"country-code-form-input\"]"
    REDUNDANCY_LEVEL_DROP_DOWN = "[data-testid=\"redundancy-level-input\"]"
    MASTER_CONTROLLER_DROP_DOWN = "[data-testid=\"master-controller-input\"]"
    MASTER_CONTROLLER_IP_INPUT_FIELD = "[data-testid=\"master-controller-ip-input\"]"
    PRIMARY_CONTROLLER_IP_INPUT_FIELD = "[data-testid=\"primary-ctrl-ip-input\"]"
    BRANCH_CONFIG_GROUP_INPUT_FIELD = "[data-testid=\"branch-config-group-input\"]"
    CONFIG_NODE_PATH_INPUT_FIELD = "[data-testid=\"config-node-path-input\"]"
