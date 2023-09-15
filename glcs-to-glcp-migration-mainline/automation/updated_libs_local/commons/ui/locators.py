from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings
settings = Settings()


class NavBarSelectors:
    is_glcp_wc_header_enabled = settings.get_ld_flags("glcp-wc-header")
    DASHBOARD_NAV_MENU = "[data-testid=\"dashboard-nav-menu\"]"
    APPLICATION_NAV_MENU = "[data-testid=\"application-nav-menu\"]"
    DEVICES_NAV_MENU = "[data-testid=\"devices-nav-menu\"]"
    MANAGE_NAV_MENU = "[data-testid=\"manage-nav-menu\"]"
    CUSTOMERS_NAV_MENU = "[data-testid=\"desc-customers-nav-menu\"]"
    MENU_ITEM_USER_BUTTON = "button[data-testid=\"drop-btn-glcp-header-brand-n-profile-menu-item-user\"]," \
                            "button[data-testid=\"drop-btn-glcp-header-all-menu-item-user\"]"
    USER_MENU_POPUP = "div[data-testid=\"drop-content-glcp-header-brand-n-profile-menu-item-user\"]," \
                      "div[data-testid=\"drop-content-glcp-header-all-menu-item-user\"]"
    SIGNOUT_MENU = "data-testid=sign-out-hpe-nav-menu"
    ACCOUNT_DETAILS_NAV_MENU = "[data-testid=\"desc-hpe-acc-det-nav-menu\"]"
    PREFERENCES_NAV_MENU = "[data-testid=\"desc-hpe-gl-pref-nav-menu\"]"
    if is_glcp_wc_header_enabled:
        DASHBOARD_NAV_MENU = "[part=nav-header-nav-dashboard]"
        APPLICATION_NAV_MENU = "[part=nav-header-nav-applications]"
        DEVICES_NAV_MENU = "[part=nav-header-nav-devices]"
        MANAGE_NAV_MENU = "[part=nav-header-nav-manage]"
        MENU_ITEM_USER_BUTTON = "[part=user-menu-button] > x-avatar"
        USER_MENU_POPUP = "[part=user-menu-button] fast-menu.shown"
        SIGNOUT_MENU = "[part=user-user-profile-dropdown-sign-out]"
        PREFERENCES_NAV_MENU = "[part=user-user-profile-dropdown-hpe-greenlake-preferences]"
        ACCOUNT_DETAILS_NAV_MENU = "[part=user-user-profile-dropdown-hpe-account-details]"
        CUSTOMERS_NAV_MENU = "[part=nav-header-nav-customers]"


class BasePageSelectors:
    APP_LOADER = "[data-testid=\"app-loader\"]"
    LOADER_SPINNER = "[data-testid$=\"spinner-with-text\"]"


class HomePageSelectors:
    LOADER_SPINNER = "[data-testid=\"loader-spinner\"]"
    ACCT_NAME = "[data-testid=\"heading-heading-home\"]"
    INVITE_USER_BUTTON = "[data-testid=\"invite-user-card-btn\"]"
    ASSIGN_ROLES_BUTTON = "[data-testid=\"assign-user-access-card-btn\"]"
    RELEASE_NOTES_BUTTON = "[data-testid=\"release-notes-card-btn\"]"
    SWITCH_ACCOUNT_BUTTON = "[data-testid=\"switch-account-btn\"]"
    RETURN_TO_MSP_ACCT_BTN = "[data-testid=\"return-to-msp-account-btn\"]"


class ManageAccountSelectors:
    CARD_WORKSPACE_DETAILS = "[data-testid=\"card-account_details\"]"
    CARD_AUDIT_LOGS = "[data-testid=\"card-audit-logs\"]"
    CARD_IDENTITY_AND_ACCESS = "[data-testid=\"card-identity\"]"
    CARD_SUBSCRIPTIONS = "[data-testid=\"card-subscriptions\"]"
    CARD_ACTIVATE = "[data-testid=\"card-activate\"]"
    PCID_VALUE_SELECTOR = "[data-testid=\"paragraph-account-id-val\"]"
    MANAGE_ACCOUNT_TYPE_BUTTON = "[data-testid='manage-account-type-btn']"


class IdentitySelectors:
    CARD_USERS = "[data-testid=\"card-users\"]"
    CARD_ROLES = "[data-testid=\"card-roles\"]"
