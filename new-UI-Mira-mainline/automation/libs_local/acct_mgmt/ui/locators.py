class ChooseAccountSelectors:
    SEARCH_BOX = "[data-testid=\"accounts-search-box\"]"
    COMPANY_NAME_TEMPLATE = "[data-testid^=\"heading-company-name\"]:text-is(\"{}\")"
    GO_TO_ACCOUNT = "[data-testid=\"tile-action-btn\"]"
    GO_TO_ACCOUNT_TEMPLATE = "[data-testid^='tile-account']:has(h4:text-is('{}')) [data-testid='tile-action-btn']"
    CREATE_ACCT_BTN = "[data-testid=\"create-account-button\"]"
    BACK_TO_SIGN_IN_BTN = "[data-testid=\"back-to-sign-in-btn\"]"
    WELCOME_HEADER = "h1:text-is('Welcome to HPE GreenLake')"
    ACCOUNTS_COUNT = "[data-testid='text-customer-accounts-count']"
    ACCOUNT_TILES = "[data-testid='tile-action-btn']"
    PAGINATION_BAR = "[data-testid='pagination']"


class CreateUserSelectors:
    """
    Class holding user creation locators
    """
    SIGNUP_TXT = "id=custom-signup"
    INPUT_EMAIL = "input[name=\"email\"]"
    INPUT_PASSWORD = "input[name=\"password\"]"
    FIRST_NAME = "input[name=\"firstName\"]"
    LAST_NAME = "input[name=\"lastName\"]"
    BUSINESS_NAME = "input[name=\"businessName\"]"
    STREET_ADDRESS = "input[name=\"streetAddress\"]"
    STREET_ADDRESS2 = "input[name=\"streetAddress2\"]"
    INPUT_CITY = "input[name=\"city\"]"
    STATE_PROVINCE = "input[name=\"stateOrProvince\"]"
    POSTAL_CODE = "input[name=\"postalCode\"]"
    CREATE_ACCT_BTN = "[data-testid=\"create-account-button\"]"
    SETUP_ACCT_COMP_NAME = "[data-testid=\"set-up-account-company-name-input\"]"
    SETUP_ACCT_PAGE = "/onboarding/set-up-account"
    SELECT_COUNTRY = "[placeholder=\"Select Country or Region\"]"
    COUNTRY_MENY_ITEM_ROLE = "menuitem"
    SELECT_LANG_DROP = "text={}"
    SELECT_LANG = "input[name=\"selectLanguage\"]"
    SELECT_TZ = "input[name=\"selectTimezone\"]"
    SELECT_TZ1 = "text={}"
    INPUT_PHONE = "input[name=\"phoneNumber\"]"
    EMAIL_CTCT_PREF = "#emailContactPreference div"
    PHONE_CTCT_PREF = "#phoneContactPreference div"
    LEGAL_CHECK_BOX = ".StyledCheckBox__StyledCheckBoxContainer-sc-1dbk5ju-1 >" \
                      " div > .StyledBox-sc-13pk1d4-0"
    CREATE_ACCT_TXT = "text=Create Account"
    ACCT_STREET_ADDRESS = "[data-testid=\"set-up-account-street-address-input\"]"
    ACCT_CITY_INPUT = "[data-testid=\"set-up-account-city-input\"]"
    ACCT_STATE_INPUT = "[data-testid=\"set-up-account-state-input\"]"
    ACCT_LEGAL_TERMS = "[data-testid=\"set-up-account-legal-terms-form-field\"] div"
    ACCT_SUBMIT = "[data-testid=\"set-up-account-submit\"]"
    MANAGE_NAV_MENU = "[data-testid=\"manage-nav-menu\"]"
    VERIFICATION_EMAIL_SENT_TEXT = "text=Verification email sent"


class CreateAcctSelectors:
    """
    Class for account creation locators
    """
    CREATE_ACCT_BTN = "[data-testid=\"create-account-button\"]"
    SETUP_ACCT_COMP_NAME = "[data-testid=\"set-up-account-company-name-input\"]"
    SELECT_COUNTRY = "[placeholder=\"Select Country\"]"

    COUNTRY_OPTION = "button:text-is('{}')"
    COUNTRY_MENY_ITEM_ROLE = "option"
    ACCT_STREET_ADDRESS = "[data-testid=\"set-up-account-street-address-input\"]"
    ACCT_CITY_INPUT = "[data-testid=\"set-up-account-city-input\"]"
    ACCT_STATE_INPUT = "[data-testid=\"set-up-account-state-input\"]"
    POSTAL_CODE = "[data-testid=\"set-up-account-zip-code-input\"]"
    INPUT_PHONE = "[data-testid=\"set-up-account-phone-number-input\"]"
    INPUT_EMAIL = "[data-testid=\"set-up-account-email-input\"]"
    ACCT_LEGAL_TERMS = "[data-testid=\"set-up-account-legal-terms-form-field\"] div"
    ACCT_SUBMIT = "[data-testid=\"set-up-account-submit\"]"
    INPUT_COUNTRY_SEARCH = '[placeholder="Country"]'


class CustomerAccountSelectors:
    """
    Class for customer account locators
    """
    PAGE_HEADER = "h1:text-is(\"Customer Accounts\")"
    ADD_CUSTOMER_BTN = "button:text(\"Add Customer\")"
    SEARCH_CUSTOMER = "[data-testid=\"search-field\"]"
    FILTER_BTN = "[data-testid=\"filter-btn\"]"
    ACTIONS_BTN = "[data-testid=\"oneaction-action-btn\"]"
    EXPORT_BTN = "[data-testid=\"export-btn\"]"
    CUSTOMER_TABLE_ROWS = "[data-testid=\"table\"] > tbody > tr"
    LOADER_SPINNER = "[data-testid*=\"loader-spinner\"]"
    CUSTOMER = "span:text-is(\"{}\")"
    CUSTOMER_ACTIONS = "[data-testid=\"table\"] > tbody > tr:has(span:text-is(\"{}\")) > td:has(button)"
    VIEW_DETAILS_BTN = "[data-testid=\"view-details-btn\"]"
    DELETE_CUSTOMER_BTN = "[data-testid=\"delete-btn\"]"


class AddCustomerSelectors:
    """
    Class for customer account creation locators
    """
    MODAL_DIALOG = "[data-testid=\"add-customer-modal-dialog\"]"
    COMPANY_NAME = "[data-testid=\"company-name-form-input\"]"
    COMPANY_DESCRIPTION = "[data-testid=\"description-input\"]"
    COUNTRY_INPUT = "[data-testid=\"country-input\"]"
    SEARCH_COUNTRY = "input[type='search']"
    COUNTRY_OPTION = "button:text-is('{}')"
    COUNTRY_ITEM_ROLE = "option"
    STREET_ADDRESS = "[data-testid=\"street-address-form-input\"]"
    STREET_ADDRESS2 = "[data-testid=\"street-address-2-form-input\"]"
    CITY_INPUT = "[data-testid=\"city-form-input\"]"
    REGION_INPUT = "[data-testid=\"state-or-region-form-input\"]"
    POSTAL_CODE = "[data-testid=\"zip-form-input\"]"
    CANCEL_BTN = "[data-testid=\"cancel-btn\"]"
    CREATE_BTN = "[data-testid=\"create-btn\"]"
    CREATION_MSG_POPUP = "[data-testid=\"notification-status-ok\"]"
    CREATION_MSG = "span:text-is(\"Customer Added Successfully\")"
    CREATION_MSG_CLOSE_BTN = "[data-testid=\"notification-status-ok\"] button"
    

class DeleteCustomerSelectors:
    """
    Class for holding Delete customer locators
    """
    TERMS_CHECKBOX = "[data-testid=\"customer-account-term-checkbox\"] + div"
    KEEP_ACCOUNT_BTN = "[data-testid=\"cancel-btn\"]"
    DELETE_ACCOUNT_BTN = "[data-testid=\"delete-account-btn\"]"
    ERROR_NOTIFICATION = "[data-testid=\"notification_error\"]"


class AccountTypeSelectors:
    """
    Class for Account Type locators
    """
    ELIGIBILITY_HEADER = "h3:text-is('Check Your Eligibility')"
    CHECK_ELIGIBILITY_BUTTON = "data-testid=check-eligibility-button"
    CONVERT_ACCT_BUTTON = "data-testid=convert-account-button"
    CONFIRM_CONVERT_BUTTON = "data-testid=submit-btn"
    FORBIDDEN_CONVERSION_MESSAGE = "data-testid=notification-message"


class CheckEligibilitySelectors:
    """
    Class for Check Eligibility Selectors
    """
    NM_SERVICE_OPTION = "span:text-is('{}')"
    DEVICE_DROP_DOWN = "data-testid=input-select-nw-as-a-svs"
    DEVICE_OPTION_ROLE = "option"
    SELECT_COUNTRY_DROP_DOWN = "input[placeholder='Select Country']"
    COUNTRY_OPTION_ROLE = "option"
    CUSTOMER_LOCATION_DROP_DOWN = "data-testid=input-select-customer-located"
    CUSTOMER_LOCATION_OPTION_ROLE = "option"
    NETWORK_COUNT_INPUT = "data-testid=input-text-num-of-nw"
    MAIL_ID = "#input-text-email"
    SALES_REP_MAIL_ID = "#input-text-sales-rep-email"
    SUBMIT_BUTTON = "data-testid=button-next"
    CONTINUE_BUTTON = "button:text-is('Continue')"


class UserProfileSelectors:
    """
    Class for holding the user profile locators
    """
    PERSONAL_EDIT_INFO_BTN = "h4:text-is(\"Personal Information\") + button:text-is(\"Edit\")"
    PASSWORD_EDIT_BTN = "h4:text-is(\"Password\") + button:text-is(\"Edit\")"
    INPUT_EMAIL = "input[id=\"email\"]"
    FIRST_NAME = "input[id=\"firstName\"]"
    LAST_NAME = "input[id=\"lastName\"]"
    ORGANISATION_NAME = "input[id=\"hpeCompanyName\"]"
    STREET_ADDRESS = "input[id=\"streetAddress\"]"
    STREET_ADDRESS2 = "input[id=\"hpeStreetAddress2\"]"
    INPUT_CITY = "input[id=\"city\"]"
    STATE_PROVINCE = "input[id=\"state\"]"
    POSTAL_CODE = "input[id=\"zipCode\"]"
    COUNTRY_BTN = "input[id=\"hpeCountryCode__input\"]"
    COUNTRY_ELEMENT_ROLE = "option"
    TIME_ZONE = "input[id=\"hpeTimezone__input\"]"
    TIME_ELEMENT_ROLE = "option"
    SELECT_LANG = "input[id=\"preferredLanguage__input\"]"
    SELECT_LANG_ROLE = "option"
    PRIMARY_PHONE = "input[id=\"primaryPhone\"]"
    MOBILE_PHONE = "input[id=\"mobilePhone\"]"
    EMBARGO_COUNTRY_WARNING_TEXT = "span:text(\"This country code is not allowed.\")"
    EMBARGO_COUNTRY_NAME = "//button[normalize-space()='North Korea']"
    SAVE_INFO_BTN = "button:text-is(\"Save\")"
    CURRENT_PASSWORD = "input[id=\"currentPassword\"]"
    NEW_PASSWORD = "input[id=\"newPassword\"]"
    CONFIRM_NEW_PASSWORD = "input[id=\"confirmPassword\"]"
    CHANGE_PASSWORD_BTN = "button:text-is(\"Change Password\")"
    INFO_SUCCESS_TXT = "span:text(\"Your profile has been updated successfully.\")"
    ERROR_MSG_TXT = "span:text(\"The password does not meet the password requirements.\")"


class UserPreferencesSelectors:
    ACCT_SELECTION_BTN = "data-testid=account-selection-btn"
    LANGUAGE_DROPDOWN = "input[name=language]"
    LANGUAGE_DROP_ROLE = "option"
    SESSION_TIMEOUT = "data-testid=timeout-number-form-field-input"
    SAVE_CHANGES_BTN = "data-testid=profile-button-submit"
    SUCCESS_MSG_TXT = "data-testid=success-info-box"
    ERROR_MSG_TXT = "span:text-is('Bad Request')"
    INVALID_TXT_MSG = "span:has-text('Invalid session timeout value')"
    DISCARD_BTN = "data-testid=profile-button-discard"
    SIGN_IN_INFO = ".okta-form-title.o-form-head"


class SwitchAccountSelectors:
    CREATE_NEW_ACCOUNT_BTN = "data-testid=create-new-account-button"
    SEARCH_ACCOUNT_FIELD = "data-testid=search-field"
    ACCOUNT_TYPE_DROPDOWN = "data-testid=account-type-input"
    SORT_BY_DROPDOWN = "data-testid=sort-by-input"
    DROPDOWN_OPTS_TEMPLATE = "button:text-is('{}')"
    RECENT_ACCOUNT_NAME = "[data-testid^='card']:first-of-type span[data-testid^='text-account-title']"
    RECENT_ACCOUNT_LAUNCH = "[data-testid^='card']:first-of-type button"
    PAGINATION_BAR = "data-testid=pagination-switch-account"
    GO_TO_PAGE = "button[aria-label='Go to page {}']"
