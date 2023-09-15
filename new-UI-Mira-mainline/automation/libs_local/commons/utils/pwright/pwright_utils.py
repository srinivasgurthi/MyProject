import logging
import os
import time

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

RECORD_DIR = os.path.join('tmp', 'results')

log = logging.getLogger(__name__)
pic_location = "/tmp/results/"
log_file = "/tmp/results/log1.log"


class PwrightUtils:
    def __init__(self, page):
        self.page = page

    def save_screenshot(self, test_name):
        """
        Save screenshot with testname to logs folder and attach to allure report
        :param test_name: test case name
        """
        random_str = RandomGenUtils.random_string_of_chars(7)
        scr_path = f"{pic_location}{random_str}{test_name}.png"
        self.page.screenshot(path=scr_path, full_page=True)
        allure.attach.file(
            source=scr_path, attachment_type=allure.attachment_type.PNG)

    def wait_for_selector(self, selector, state="visible", timeout_ignore=False, timeout=20000):
        """Wait for expected element appeared on the page.

        Args:
            selector: str - element selector
            state: Literal["attached", "detached", "hidden", "visible"] - element's state to wait for
            timeout_ignore: bool - bypass (True) or not (False) timeout without raising exception
            timeout: int - waiting timeout, milliseconds

        Returns:
            bool - is element present (True) or not (False)
        """
        try:
            self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return True
        except Exception as ex:
            log.warning(
                f"Element with expected selector '{selector}' did not appear within {timeout} milliseconds.")
            if not timeout_ignore:
                raise ex
            return False

    def click_selector(self, selector, timeout=20000):
        """Click on element once it appeared on the page.

        Args:
            selector: str - element selector
            timeout: int - waiting timeout for element to appear at the page, milliseconds
        """
        self.wait_for_selector(selector, timeout=timeout)
        self.page.locator(selector).click()

    def wait_for_url(self, url_pattern, timeout_ignore=False, timeout=20000):
        """Wait for actual URL matched to expected pattern.

        Args:
            url_pattern: Pattern[str] - expected URL pattern to be matched with page's actual URL
            timeout_ignore: bool - bypass (True) or not (False) timeout without raising exception
            timeout: int - waiting timeout, milliseconds

        Returns:
            bool - is URL matched (True) or not (False)
        """
        try:
            self.page.wait_for_url(url=url_pattern, wait_until="domcontentloaded", timeout=timeout)
            return True
        except Exception as ex:
            current_url = self.page.url
            log.warning(
                f"Expected URL did not appear within {timeout} milliseconds.")
            log.warning(
                f"Expected URL pattern '{url_pattern}'; actual URL: '{current_url}'.")
            if not timeout_ignore:
                raise ex
            return False

    def enter_text_into_element(self, selector, text):
        """Populate element with specified text and press "Enter".

        Args:
            selector: str - element selector
            text: str - text to be entered
        """
        element = self.page.locator(selector)
        element.click()
        element.clear()
        element.fill(text)
        element.press("Enter")

    def select_drop_down_element_by_index(self, dropdown_selector, list_items_selector, item_index,
                                          tries=3, items_timeout=2000):
        """Choose element from dropdown items list by item index (starting from 1).

        :param dropdown_selector: selector of dropdown element.
        :param list_items_selector: common selector for all items in this dropdown list.
        :param item_index: index (starting from 1) of item to select.
        :param tries: count of attempts to get displayed list of items in expanded dropdown (required for some pages).
        :param items_timeout: timeout for list items to be displayed after expending dropdown list (used by retries).
        """
        while tries > 0:
            self.page.locator(dropdown_selector).click()
            list_items_displayed = self.wait_for_selector(list_items_selector, "visible", True, items_timeout)
            if list_items_displayed:
                break
            tries -= 1
            if tries > 0:
                log.warning(f"List items were missed in dropdown. Retrying (remained retries: {tries})...")
        else:
            raise Exception(f"Items list with expected selector '{list_items_selector}' is missed in dropdown.")
        self.page.locator(list_items_selector).nth(item_index-1).click()  # index of nth() method starts from 0.

    def select_drop_down_element(self, drop_menu_selector, element, element_role="menuitem", exact_match=False):
        """ Method used to pick element from the dropdown menu

        Args:
            drop_menu_selector: Selector of dropdown menu
            element: Element's name, which needs to be picked up
            element_role: Role attribute of DOM list element
            exact_match: Pick element that matched exactly/partially to given name
        """
        self.page.locator(drop_menu_selector).click()
        self._scroll_to_drop_list_element(element_role, element, exact_match)
        self.page.get_by_role(element_role, name=element,
                              exact=exact_match).click()

    def _scroll_to_drop_list_element(self, role, selector, exact, horizontally=0, vertically=200, timeout=30):
        """Scroll the mouse wheel in selected direction till element became visible

        Args:
            selector: str - element selector
            role: str - role of the element. Several examples: "button", "checkbox", "link", "menuitem" etc.
            horizontally: int - pixels value to scroll X axis - positive value to the right direction,
                                                                negative - to the left
            vertically: int - pixels value to scroll Y axis - positive value to the bottom direction,
                                                                negative - to the top
            timeout: int - timeout to break the loop, seconds
            exact: Whether `name` is matched exactly: case-sensitive and whole-string.
        """
        time_start = time.time()
        while self.page.get_by_role(role, name=selector, exact=exact).is_hidden() \
                and time.time() < time_start + timeout:
            self.page.mouse.wheel(horizontally, vertically)


class TableUtils:
    """
    Playwright utilities to work with tables
    """

    def __init__(self, page):
        """Specify selectors for the tables to work with.
        Currently verified with Users, Roles, Audit Logs, DevicesInventory and DeviceSubscriptions tables.
        Since table selectors are consistent between all pages - they are stored locally in this utility class.
        Should be here until table selectors became diverse between pages. If diversed - needs to be reworked.

        :param page: current playwright page
        """
        self.page = page
        self.head_columns = "[data-testid=\"table\"]>thead>tr>th"
        self.table_rows = "[data-testid=\"table\"]>tbody>tr"
        self.row_columns_template = "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>td," \
                                    "[data-testid=\"table\"]>tbody>tr:nth-child({row_index})>th"

    def get_column_index_by_name(self, column_name):
        """Return index (starting from 1) of the column with matched text.

        :param column_name: text to be matched in header's column of the table.
        :return: index (int) of matched column. None, if matches not found.
        """
        columns_count = self.page.locator(self.head_columns).count()
        for column_index in range(columns_count):
            if self.page.locator(self.head_columns).nth(column_index).text_content() == column_name:
                column_css_index = column_index + 1  # CSS-locator index starts from 1
                return column_css_index
        return None

    def get_rows_indices_by_text(self, row_text):
        """Return list of indices (starting from 1) of the rows, containing expected text.

        :param row_text: text to be present in table's row.
        :return: list (int) of the rows indices, containing specified text. Empty list, if text not found in rows.
        """
        rows_count = self.page.locator(self.table_rows).count()
        rows_indices = []
        for row_index in range(rows_count):
            if row_text in self.page.locator(self.table_rows).nth(row_index).text_content():
                # CSS-locator index starts from 1
                rows_indices.append(row_index + 1)
        return rows_indices

    def get_row_columns_indices_by_text(self, row_index, column_text):
        """Analyze row with specified index and return list of columns indices (starting from 1),
        matching to expected text.

        :param row_index: index of the row to look at (starting from 1).
        :param column_text: text to be matched.
        :return: list (int) of the columns indices, matching specified text. Empty list, if text not matched in columns.
        """
        columns_count = self.page.locator(self.head_columns).count()
        column_indices = []
        for column_index in range(columns_count):
            if self.page.locator(self.row_columns_template.format(row_index=row_index)).nth(
                    column_index).text_content() == column_text:
                # CSS-locator index starts from 1
                column_indices.append(column_index + 1)
        return column_indices

    def get_rows_indices_by_text_in_column(self, column_name, column_text):
        """Return list of rows indices (starting from 1), matching to expected text at specified column.

        :param column_name: column name where matching text should be looked at.
        :param column_text: text to be matched.
        :return: list (int) with indices of the rows, matching expected text at specified column.
        Empty list, if text not matched in columns.
        """
        column_index = self.get_column_index_by_name(column_name)
        rows_indices = self.get_rows_indices_by_text(column_text)
        if not all((column_index, rows_indices)):
            log.warning(
                f"Column or rows with expected value was not found at the page.")

        matched_rows_indices = []
        for index in rows_indices:
            row_columns_indices = self.get_row_columns_indices_by_text(
                index, column_text)
            if column_index in row_columns_indices:
                matched_rows_indices.append(index)
        return matched_rows_indices

    def get_rows_indices_by_values_in_columns(self, column_to_text_dict):
        """Return list of rows indices (starting from 1), matching to expected text at specified column.

        :param column_to_text_dict: dict with expected values in format {"Column name": "Expected text"}.
        :return: list (int) with indices of the rows, matching expected text at specified column.
        Empty list, if text not matched in columns.
        """

        matched_rows_indices = set()
        for column_name, column_text in column_to_text_dict.items():
            column_index = self.get_column_index_by_name(column_name)
            rows_indices = self.get_rows_indices_by_text(column_text)
            if not all((column_index, rows_indices)):
                log.warning(f"Column or rows with expected value was not found in table.")
                matched_rows_indices.clear()
                break
            if not matched_rows_indices:
                matched_rows_indices.update(set(rows_indices))
            matched_rows_indices.intersection_update(set(rows_indices))

            for index in matched_rows_indices:
                row_columns_indices = self.get_row_columns_indices_by_text(index, column_text)
                if column_index not in row_columns_indices:
                    matched_rows_indices.remove(index)
        return sorted(matched_rows_indices)


def browser_stop(context, page, test_name):
    """
    Closes the page

    :param context: context object
    :param page: page object
    :param test_name: name of the test case
    :return: None
    """
    page.close()
    context.tracing.stop(path=RECORD_DIR + test_name + ".zip")
    allure.attach.file(source=RECORD_DIR + test_name + ".zip")
    context.close()
    path = page.video.path()
    allure.attach.file(source=path, name="video",
                       attachment_type=AttachmentType.WEBM)


def browser_page(browser_launched, storage_state=None):
    """
    Launches browser; creates new page

    :param browser_launched: browser instance
    :param storage_state: filename with stored context state to be used in new instantiated browser context.
    :return: context, page
    """
    context = browser_launched.new_context(
        storage_state=storage_state, record_video_dir=RECORD_DIR)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    return context, page
