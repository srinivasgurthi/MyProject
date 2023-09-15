"""
#TODO:
Start using file under utils/pwright/pwright_utils.py for new test cases. Remove this file after check in the test case if this is not used.

"""
import logging

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)
pic_location = "/tmp/results/"
log_file = "/tmp/results/log1.log"


class SaveVideo(object):
    def save_video(self, page):
        page.video.save_as(pic_location)
        allure.attach.file(source=pic_location, name="video", attachment_type=AttachmentType.WEBM)


class VerifyTestSteps(object):
    def verify_test_step(self, tc_step):
        return bool(tc_step)


class SaveScreenshot(object):
    def save_screenshot(self, page, test_name):
        random_str = RandomGenUtils.random_string_of_chars(7)
        page.screenshot(path=pic_location + random_str + test_name + ".png", full_page=True)
        allure.attach.file(source=pic_location + random_str + test_name + ".png",
                           attachment_type=allure.attachment_type.PNG)
