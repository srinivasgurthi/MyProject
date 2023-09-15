"""
Activate Folder Details page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateFolderDetailsSelectors
from hpe_glcp_automation_lib.libs.adi.ui.rule_data import RuleData
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class ActivateFolderDetails(HeaderedPage):
    """
    Activate Folder Details page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Activate Folder Details page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Activate Folder Details page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/activate/folders/folder-details"

    def edit_folder(self, **kwargs):
        """
        Edit current folder details
        :param kwargs: a set of key-values to be applied to a folder. E.g.: name="some new name", parent="self",
        description="some description"
        :return: current instance of Activate Folder Details page object.
        """
        log.info("Playwright: Edit folder.")
        self.page.locator(ActivateFolderDetailsSelectors.EDIT_FOLDER_BTN).click()
        for key in kwargs.keys():
            if "name" in key:
                self.page.locator(ActivateFolderDetailsSelectors.FOLDER_NAME_INPUT_FIELD).fill(kwargs[key])
            elif "parent" in key:
                self.page.locator(ActivateFolderDetailsSelectors.PARENT_FOLDER_MENU).click()
                self._search_drop_down("searchbox", kwargs[key], "option")
            elif "description" in key:
                self.page.locator(ActivateFolderDetailsSelectors.DESCRIPTION_INPUT_FIELD).fill(kwargs[key])
            else:
                raise KeyError("Name of the new parameter does not fit the expected. Expected fields to change in a "
                               f"folder: 'name', 'parent_folder', 'description'. Actual key name: {key}")
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(ActivateFolderDetailsSelectors.SAVE_CHANGES_BTN).click()
        self.wait_for_loaded_state()
        return self

    def wait_for_loaded_table(self):
        """Wait for table rows are not empty and loader spinner is not present on the page.

        :return: current instance of Activate Folder Details page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(ActivateFolderDetailsSelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def delete_folder(self):
        """
        Delete current active folder.
        """
        log.info("Playwright: Delete folder.")
        self.page.locator(ActivateFolderDetailsSelectors.ACTIONS_MENU).click()
        self.page.locator(ActivateFolderDetailsSelectors.DELETE_FOLDER_MENU_ITEM).click()
        self.page.locator(ActivateFolderDetailsSelectors.OK_POPUP_BUTTON).click()
        self.page.locator(ActivateFolderDetailsSelectors.OK_POPUP_BUTTON).wait_for(state="hidden")
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def add_new_rule(self, rule_info: RuleData = RuleData()):
        """
        Add new rule to current folder
        :param rule_info: RuleData class object with data for a new rule
        :return: current instance of Activate Folder Details page object.
        """
        log.info("Playwright: Create new rule for the folder.")
        self.page.locator(ActivateFolderDetailsSelectors.ADD_NEW_RULE_BTN).click()
        self.page.locator(ActivateFolderDetailsSelectors.RULE_NAME_INPUT_FIELD).fill(rule_info.name)
        self.page.locator(ActivateFolderDetailsSelectors.RULE_TYPE_DROP_DOWN).click()
        self.page.get_by_role("option", name=rule_info.type).click()
        if rule_info.email_on:
            self.page.locator(ActivateFolderDetailsSelectors.EMAIL_ON_DROP_DOWN).click()
            self.page.get_by_role("option", name=rule_info.email_on).click()
        if rule_info.folder:
            self.page.locator(ActivateFolderDetailsSelectors.PARENT_FOLDER_DROP_DOWN).click()
            self.page.get_by_role("option", name=rule_info.folder).click()
        if rule_info.for_rule:
            self.page.locator(ActivateFolderDetailsSelectors.FOR_RULE_DROP_DOWN).click()
            self.page.get_by_placeholder("Search By Rule...").fill(rule_info.for_rule)
            self.page.get_by_role("option", name=rule_info.for_rule)
        if rule_info.email_to:
            self.page.locator(ActivateFolderDetailsSelectors.EMAIL_TO_INPUT_FIELD).fill(rule_info.email_to)
        if rule_info.prov_type:
            self.pw_utils.select_drop_down_element(ActivateFolderDetailsSelectors.PROVISIONING_TYPE_DROP_DOWN,
                                                   rule_info.prov_type,
                                                   "option")
        if rule_info.amp_ip:
            self.page.locator(ActivateFolderDetailsSelectors.AMP_IP_INPUT_FIELD).fill(rule_info.amp_ip)
        if rule_info.shared_secret:
            self.page.locator(ActivateFolderDetailsSelectors.SHARED_SECRET_INPUT_FIELD).fill(rule_info.shared_secret)
        if rule_info.organization:
            self.page.locator(ActivateFolderDetailsSelectors.ORGANIZATION_INPUT_FIELD).fill(rule_info.organization)
        if rule_info.ap_group:
            self.page.locator(ActivateFolderDetailsSelectors.AP_GROUP_INPUT_FIELD).fill(rule_info.ap_group)
        if rule_info.controller:
            self.page.locator(ActivateFolderDetailsSelectors.CONTROLLER_INPUT_FIELD).fill(rule_info.controller)
        if rule_info.backup_contrlr_ip:
            self.page.locator(ActivateFolderDetailsSelectors.BACKUP_CONTROLLER_IP_INPUT_FIELD).fill(rule_info.backup_contrlr_ip)
        if rule_info.conductor_mac:
            self.page.locator(ActivateFolderDetailsSelectors.CONDUCTOR_MAC_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.conductor_mac, "menuitem")
        if rule_info.primary_conductor:
            self.page.locator(ActivateFolderDetailsSelectors.PRIMARY_CONTROLLER_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.primary_conductor, "menuitem")
        if rule_info.backup_conductor:
            self.page.locator(ActivateFolderDetailsSelectors.BACKUP_CONDUCTOR_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.backup_conductor, "menuitem")
        if rule_info.primary_ctrl_ip:
            self.page.locator(ActivateFolderDetailsSelectors.PRIMARY_CONTROLLER_IP_INPUT_FIELD).fill(rule_info.primary_ctrl_ip)
        if rule_info.backup_ctrl_ip:
            self.page.locator(ActivateFolderDetailsSelectors.BACKUP_CTRL_IP_INPUT_FIELD).fill(rule_info.backup_ctrl_ip)
        if rule_info.branch_ctrl_group:
            self.page.locator(ActivateFolderDetailsSelectors.BRANCH_CONFIG_GROUP_INPUT_FIELD).fill(rule_info.branch_ctrl_group)
        if rule_info.redundancy_level:
            self.page.locator(ActivateFolderDetailsSelectors.REDUNDANCY_LEVEL_DROP_DOWN).click()
            self.page.get_by_role("option", name=rule_info.redundancy_level)
        if rule_info.config_node_path:
            self.page.locator(ActivateFolderDetailsSelectors.CONFIG_NODE_PATH_INPUT_FIELD).fill(rule_info.config_node_path)
        if rule_info.mobility_conductor:
            self.page.locator(ActivateFolderDetailsSelectors.MASTER_CONTROLLER_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.mobility_conductor, "menuitem", exact=True)
        if rule_info.mobility_conductor_ip:
            self.page.locator(ActivateFolderDetailsSelectors.MASTER_CONTROLLER_IP_INPUT_FIELD).fill(rule_info.mobility_conductor_ip)
        if rule_info.backup_mobility_conductor:
            self.page.locator(ActivateFolderDetailsSelectors.BACKUP_CONDUCTOR_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.backup_mobility_conductor, "menuitem", exact=True)
        if rule_info.vpn_concentrator_mac:
            self.page.locator(ActivateFolderDetailsSelectors.VPN_CONCENTRATOR_MAC_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.vpn_concentrator_mac, "menuitem")
        if rule_info.vpn_concentrator_ip:
            self.page.locator(ActivateFolderDetailsSelectors.VPN_CONCENTRATOR_IP_INPUT_FIELD).fill(rule_info.vpn_concentrator_ip)
        if rule_info.backup_vpn_concentrator_mac:
            self.page.locator(ActivateFolderDetailsSelectors.BACKUP_VPN_CONDUCTOR_MAC_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.backup_vpn_concentrator_mac, "menuitem", exact=True)
        if rule_info.country:
            self.page.locator(ActivateFolderDetailsSelectors.COUNTRY_CODE_DROP_DOWN).click()
            self._search_drop_down("searchbox", rule_info.country, "option", exact=True)
        if rule_info.persist_ip:
            self.page.locator("label").filter(has_text="Persist Conductor IP").check()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(ActivateFolderDetailsSelectors.CONFIRM_POPUP_BUTTON).click()
        return self

    def delete_rule(self, rule_name):
        """
        Delete rule by its name
        :param rule_name: Name of the rule, that need to be deleted
        :return: current instance of Activate Folder Details page object.
        """
        log.info("Playwright: Delete rule for the folder.")
        self.page.locator(ActivateFolderDetailsSelectors.RULE_LIST_ROW_TEMPLATE.format(rule_name))\
            .locator(ActivateFolderDetailsSelectors.DELETE_RULE_BTN).click()
        self.page.locator(ActivateFolderDetailsSelectors.OK_POPUP_BUTTON).click()
        self.page.locator(ActivateFolderDetailsSelectors.OK_POPUP_BUTTON).wait_for(state="hidden")
        return self

    def edit_rule(self, rule_name, rule_info):
        """
        Edit rule by its name
        :param rule_name: Name of the rule, that need to be edited.
        :param rule_info: New values, to update rule info
        :return: current instance of Activate Folder Details page object.
        """
        log.info("Playwright: Edit rule for the folder.")
        self.page.locator(ActivateFolderDetailsSelectors.RULE_LIST_ROW_TEMPLATE.format(rule_name))\
            .locator(ActivateFolderDetailsSelectors.EDIT_RULE_BTN).click()
        # Note: This is just a placeholder. Need to implement rule editing functionality.
        return self

    def go_back_to_folders(self):
        self.page.locator(ActivateFolderDetailsSelectors.BACK_TO_FOLDERS_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def search_for_text(self, search_text, ensure_not_empty=True):
        """Enter text to search field.

        :param search_text: search_text.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return:current instance of Activate Folder Details page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at folders page.")
        self.pw_utils.enter_text_into_element(ActivateFolderDetailsSelectors.SEARCH_DEVICE_INPUT_FIELD, search_text)
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def should_have_device_in_the_folder(self, device_info):
        """
        Verify that the device is able to show successfully for the folder
        IMPORTANT: verification applied to first table row, so need to perform search before assertion
        :param device_info: Device serial or mac or name
        :return:current instance of Activate Folder Details page object.
        """
        table_row_selector = ActivateFolderDetailsSelectors.TABLE_ROWS
        expect(self.page.locator(table_row_selector).first).to_contain_text(device_info)
        return self

    def should_have_rule_in_the_list(self, rule_name):
        """
        Check that rule is in the list of rules on the page.
        :param rule_name: Rule's name
        :return: current instance of Activate Folder Details page object.
        """
        rule_selector = ActivateFolderDetailsSelectors.RULE_LIST_ROW_TEMPLATE.format(rule_name)
        expect(self.page.locator(rule_selector).first).to_be_visible()
        return self

    def _search_drop_down(self, search_field, item_name, item_option, exact=False):
        """
        Search from drop down menu elements
        :param search_field: search input field role name
        :param item_name: item to search for
        :param item_option: list item role name
        :param exact: use exact (True) or partial (False) matching.
        :return: current instance of Activate Folder Details page object.
        """
        self.page.get_by_role(search_field).fill(item_name)
        self.page.get_by_role(item_option, name=item_name, exact=exact).click()
