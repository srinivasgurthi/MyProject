class RolesSelectors:
    BACK_BUTTON = "[data-testid=\"identity-title\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"
    CREATE_ROLE_BUTTON = "[data-testid=\"roles-create-btn\"]"
    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    TABLE_HEAD_COLUMNS = "[data-testid=\"table\"]>thead>tr>th"
    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"


class UsersSelectors:
    BACK_BUTTON = "[data-testid=\"identity-back-btn\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"
    INVITE_USERS_BUTTON = "[data-testid=\"invite-users-btn\"]"
    CARD_TOTAL_USERS = "[data-testid=\"card-total-users-tab\"]"
    CARD_ACTIVE_USERS = "[data-testid=\"card-active-users-tab\"]"
    CARD_INACTIVE_USERS = "[data-testid=\"card-inactive-users-tab\"]"
    CARD_UNVERIFIED_USERS = "[data-testid=\"card-unverified-users-tab\"]"
    SEARCH_FIELD = "[data-testid=\"search-field\"]"
    TABLE_HEAD_COLUMNS = "[data-testid=\"table\"]>thead>tr>th"
    TABLE_ROWS = "[data-testid=\"table\"]>tbody>tr"
    TABLE_ROW_TEMPLATE = "[data-testid=\"table\"]>tbody>tr:nth-child({})"
    INVITE_USERS_EMAIL_FIELD = "[data-testid=\"email-form-field-input\"]"
    INVITE_USERS_ROLES_DROPDOWN = "[data-testid=\"roles-dropdown\"]"
    INVITE_USERS_ROLE_TEMPLATE = "button:has(span:text-is('{}'))"
    INVITE_USERS_SEND_INVITE_BTN = "[data-testid=\"send-invite-btn\"]"
    USER_STATUS_TEMPLATE = "//span[normalize-space()='{}']/ancestor::tr[contains(.,'{}')]"
    TABLE_ACTION_BTN_TEMPLATE = "[data-testid=\"table\"] > tbody > tr:has(span:text-is('{}')) > td:last-child:has(button)"
    DELETE_BTN = "button:text-is(\"Delete\")"
    DELETE_CHECK_BTN = "[data-testid=\"delete-user-btn\"]"
    DELETE_CONFIRM_BTN = "[data-testid=\"confirm-delete-user-btn\"]"