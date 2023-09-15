class MyApplicationsSelectors:
    LOADER_SPINNER = "[data-testid=\"loader-spinner\"]"
    HEADING_PAGE_TITLE = "[data-testid=\"heading-page-title\"]"
    REGION_DROPDOWN = "[data-testid=\"region-dropdown\"]"
    APPLICATION_TILE = "[data-testid^=\"application-tile-\"]"
    APPLICATION_CARD_TEMPLATE = "[data-testid='application-tile-{}']"


class AppNavigationSelectors:
    MY_APPS_BTN = "[data-testid='menu-item-installed-apps']"
    AVAILABLE_APPS_BTN = "[data-testid='menu-item-available-apps']"


class AvailableAppsSelectors:
    LOADER_SPINNER = "[data-testid=\"loader-spinner\"]"
    AVAILABLE_APPS_MSG = "[data-testid=\"no-data-title\"]"
    APPLICATION_CARDS = "[data-testid^='card-application-card-']"
    APPLICATION_CARD_TEMPLATE = "[data-testid='card-application-card-{}']"
    VIEW_DETAILS_BTN_TEMPLATE = "[data-testid=\"view-details-action-btn-{}\"]"


class AppsDetailsSelectors:
    AVAILABLE_APPS = "data-testid='back-to-available-app'"
    SETUP_APPLICATION_BTN = "[data-testid=\"set-up-application-btn\"]"
    ADD_APPLICATION_MODAL = "[data-testid=\"add-application-modal\"]"
    DEPLOYMENT_REGION = "[data-testid=\"deployment-region-dropdown\"]"
    REGION_OPTION_TEMPLATE = "button:text-is('{}')"
    REGION_ELEMENT_ROLE = "option"
    TERMS_CHECKBOX = "[data-testid=\"app-term-form\"]"
    DEPLOY_BTN = "[data-testid=\"add-region-btn\"]"
    CANCEL_BTN = "data-testid='cancel-modal-btn'"


class InstalledAppsSelectors:
    MY_APPS = "[data-testid='my-apps-back-btn']"
    INSTALLED_APP_TEMPLATE = "[data-testid=\"installed-app-{}\"]"
    APP_ACTION_BTN_TEMPLATE = "[data-testid=\"installed-app-{}\"] [data-testid=\"installed-app-list-action-btn\"]"
    LAUNCH_APPS_BTN_TEMPLATE = "[data-testid=\"installed-app-{}\"] [data-testid=\"launch-action-btn\"]"
    ACTION_REMOVE_REGION = "[data-testid=\"action-2\"]"
    REMOVE_APPS_MODAL = "[data-testid=\"remove-apps-modal\"]"
    TERM_CHECKBOX = "[data-testid=\"app-term-form\"]"
    REMOVE_REGION_BTN = "[data-testid=\"remove-region-btn\"]"
    KEEP_REGION_BTN = "[data-testid=\"cancel-btn\"]"
