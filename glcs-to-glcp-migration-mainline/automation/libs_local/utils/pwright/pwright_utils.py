import logging
import os
import time

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

RECORD_DIR = os.path.join('tmp', 'results')

log = logging.getLogger(__name__)
pic_location = "/tmp/results/"
log_file = "/tmp/results/log1.log"


class PwrightUtils:
    def save_video(self, page):
        page.video.save_as(pic_location)
        allure.attach.file(source=pic_location, name="video", attachment_type=AttachmentType.WEBM)

    def verify_test_step(self, tc_step):
        return bool(tc_step)

    def save_screenshot(self, page, test_name):
        random_str = RandomGenUtils.random_string_of_chars(7)
        scr_path = f"{pic_location}{random_str}{test_name}.png"
        page.screenshot(path=scr_path, full_page=True)
        allure.attach.file(source=scr_path, attachment_type=allure.attachment_type.PNG)

    @staticmethod
    def wait_after_selector(page, selector, state="visible", timeout_ignore=False, timeout=20000, delay=2):
        """Wait for specified delay after expected element appeared on the page.

        Args:
            page: Page - Playwright page instance
            selector: str - element selector
            state: Literal["attached", "detached", "hidden", "visible"] - element's state to wait for
            timeout_ignore: bool - bypass (True) or not (False) timeout without raising exception
            timeout: int - waiting timeout, milliseconds
            delay: int - delay after expected element appeared, seconds

        Returns:
            bool - is element present (True) or not (False)
        """
        try:
            page.wait_for_selector(selector, timeout=timeout, state=state)
            time.sleep(delay)
            return True
        except Exception as ex:
            log.warning(f"Element with expected selector '{selector}' did not appear within {timeout} milliseconds.")
            if not timeout_ignore:
                raise ex
            return False

    @staticmethod
    def wait_after_url(page, url_pattern, timeout_ignore=False, timeout=20000, delay=2):
        """Wait for specified delay after page URL matched to expected pattern.

        Args:
            page: Page - Playwright page instance
            url_pattern: Pattern[str] - expected URL pattern to be matched with page's actual URL
            timeout_ignore: bool - bypass (True) or not (False) timeout without raising exception
            timeout: int - waiting timeout, milliseconds
            delay: int - delay after URL matched to expected pattern, seconds

        Returns:
            bool - is URL matched (True) or not (False)
        """
        try:
            page.wait_for_url(url=url_pattern, wait_until="domcontentloaded", timeout=timeout)
            time.sleep(delay)
            return True
        except Exception as ex:
            current_url = page.url
            log.warning(f"Expected URL did not appear within {timeout} milliseconds.")
            log.warning(f"Expected URL pattern '{url_pattern}'; actual URL: '{current_url}'.")
            if not timeout_ignore:
                raise ex
            return False


def browser_stop(context, page, test_name):
    """
    Closes the page

    :param context: context object
    :param page: page object
    :param test_name: name of the test case
    :return: None
    """
    context.tracing.stop(path=RECORD_DIR + test_name + ".zip")
    allure.attach.file(source=RECORD_DIR + test_name + ".zip")
    page.close()


def browser_page(browser_launched):
    """
    Launches browser; creates new page

    :param browser_launched: browser instance
    :return: context, page
    """
    context = browser_launched.new_context(record_video_dir=RECORD_DIR)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    return context, page
