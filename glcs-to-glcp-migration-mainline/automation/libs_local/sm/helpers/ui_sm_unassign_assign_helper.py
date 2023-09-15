import logging

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.authn.ui.login_to_homepage import Login
from hpe_glcp_automation_lib.libs.sm.ui.sm_unassign_assign import SmUnassignAssignDevicePages
from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)

record_dir = '/tmp/results/'


class HlpUnassignAssignDeviceSubscription(object):

    def HlpUnassignAssignDeviceSubscription_fn(self, browser_launched, hostname, username, password, account_name,
                                               dm_pw_data, dm_pw_data_except, sm_pw_data, test_name):
        random_str = RandomGenUtils.random_string_of_chars(7)
        context = browser_launched.new_context(record_video_dir=record_dir)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        try:
            page.goto(hostname)
            tc_login = Login(username, password)
            login_successful = tc_login.login_acct(page, account_name)
            if not login_successful:
                raise Exception(f"Failed login by {username}.")
            # assign_license = FtUnassignAssignDevicePages()
            init_sm_device_page = SmUnassignAssignDevicePages()
            assign_unassign_result = init_sm_device_page.SmUnassignAssignDevicePages_fn(page,
                                                                                        record_dir, random_str,
                                                                                        dm_pw_data, dm_pw_data_except,
                                                                                        sm_pw_data, test_name)
            return assign_unassign_result

        except Exception as e:
            log.error(e)
            return False

        finally:
            page.screenshot(path=record_dir + random_str + test_name + ".png", full_page=True)
            allure.attach.file(source=record_dir + random_str + test_name + ".png")
            page.close()
            context.tracing.stop(path=record_dir + random_str + test_name + ".zip")
            allure.attach.file(source=record_dir + random_str + test_name + ".zip")
            context.close()
            path = page.video.path()
            allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
