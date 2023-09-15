import logging
import allure
from allure_commons.types import AttachmentType
import json
import random,string

#from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils
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






def load_json_from_file(file_path: str):
    with open(file_path, "r") as openfile:
        json_object = json.load(openfile)
    return json_object



def dump_json_to_file(file_path: str, dictionary: dict):
    with open(file_path, "w") as outfile:
        json.dump(dictionary, outfile)
    


def generate_random_string(length: int) -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))