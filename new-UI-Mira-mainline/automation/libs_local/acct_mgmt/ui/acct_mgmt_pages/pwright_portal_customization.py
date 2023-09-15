import logging

from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class PortalCustomizationPagePaths:
    apps_btn_xpath: str = 'data-testid=apps-btn'
    mng_acct_btn_xpath: str = 'data-testid=desc-header-apps-manage-account'
    portal_customization_tile_xpath: str = 'data-testid=text-portal-customization-title'
    customize_portal_title_xpath: str = 'data-testid=heading-page-title'
    portal_edit_button_xpath: str = 'data-testid=portal-edit-btn'
    company_information_title_xpath: str = 'data-testid=heading-company-information-title'
    company_name_input_xpath: str = 'data-testid=edit-company-name-input'
    product_name_input_xpath: str = 'data-testid=edit-product-name-input'
    mailing_addr_input_xpath: str = 'data-testid=edit-mailing-address-input'
    copyright_input_xpath: str = 'data-testid=edit-copyright-input'
    save_changes_button_xpath: str = "//button[contains(text(),'Save Changes')]"
    company_name_value_text_xpath: str = \
        'data-testid=text-portal-details-display-company-name-value'
    required_error_xpath: str = "//*[contains(text(), 'required')]"
    logo_upload_input_xpath: str = 'data-testid=branding_logo'
    logo_name_text_xpath: str = 'data-testid=text-branding-logo-icon-name'
    sample_email_button_xpath: str = 'data-testid=portal-send-email-btn'
    send_email_input_xpath: str = 'data-testid=send-email-input'
    send_email_button_xpath: str = 'data-testid=send-email-btn'
    sample_email_sent_text_xpath: str = 'data-testid=text-sample-email-sent-text'


class PortalCustomizationPage(object):
    def __init__(self, edit_portal_data=None):
        self.pw_utils = PwrightUtils()
        self.selectors = PortalCustomizationPagePaths()
        self.edit_portal_data = edit_portal_data or {}
        log.info(f"Initialize {__name__}")

    def check_portal_customization_homepage(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            portal_edit = page.locator(self.selectors.customize_portal_title_xpath)

            if 'Portal Customization' in portal_edit.inner_text():
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the details of "
                      "the portal customization page {}".format(e))
            return False

    def check_portal_customization_edit_text(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            page.click(self.selectors.portal_edit_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            portal_edit = page.locator(self.selectors.company_information_title_xpath)

            if 'Company Information' in portal_edit.inner_text():
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the edit section of customization page {}".format(e))
            return False

    def check_portal_customization_edit_flow(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            page.click(self.selectors.portal_edit_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.fill(self.selectors.company_name_input_xpath, '')
            page.fill(self.selectors.company_name_input_xpath, self.edit_portal_data['company_name'])
            page.fill(self.selectors.product_name_input_xpath, '')
            page.fill(self.selectors.product_name_input_xpath, self.edit_portal_data['product_name'])
            page.fill(self.selectors.mailing_addr_input_xpath, '')
            page.fill(self.selectors.mailing_addr_input_xpath, self.edit_portal_data['mailing_addr'])
            page.fill(self.selectors.copyright_input_xpath, '')
            page.fill(self.selectors.copyright_input_xpath, self.edit_portal_data['copyright'])
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.save_changes_button_xpath)
            company_name = page.locator(self.selectors.company_name_value_text_xpath)

            if self.edit_portal_data['company_name'] in company_name.inner_text():
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the edit section of customization page {}".format(e))
            return False

    def check_portal_customization_edit_error_fields(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            page.click(self.selectors.portal_edit_button_xpath)
            page.fill(self.selectors.company_name_input_xpath, '')
            page.fill(self.selectors.product_name_input_xpath, '')
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.save_changes_button_xpath)
            required_error = page.locator(self.selectors.required_error_xpath)

            if required_error:
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the edit section of customization page {}".format(e))
            return False

    def check_portal_customization_edit_logo_upload(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            page.click(self.selectors.portal_edit_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.fill(self.selectors.company_name_input_xpath, '')
            page.fill(self.selectors.company_name_input_xpath, self.edit_portal_data['company_name'])
            page.fill(self.selectors.product_name_input_xpath, '')
            page.fill(self.selectors.product_name_input_xpath, self.edit_portal_data['product_name'])
            page.set_input_files(self.selectors.logo_upload_input_xpath,
                                 self.edit_portal_data['logo_img_path'])
            page.click(self.selectors.save_changes_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            logo_name = page.locator(self.selectors.logo_name_text_xpath)

            if self.edit_portal_data['logo_img_name'] in logo_name.inner_text():
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the edit section of customization page {}".format(e))
            return False

    def check_portal_customization_edit_sample_email(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.portal_customization_tile_xpath)
            page.click(self.selectors.portal_edit_button_xpath)
            page.fill(self.selectors.company_name_input_xpath, '')
            page.fill(self.selectors.company_name_input_xpath, self.edit_portal_data['company_name'])
            page.fill(self.selectors.product_name_input_xpath, '')
            page.fill(self.selectors.product_name_input_xpath, self.edit_portal_data['product_name'])
            page.click(self.selectors.sample_email_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.fill(self.selectors.send_email_input_xpath, self.edit_portal_data['sample_email'])
            page.click(self.selectors.send_email_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            email_sent = page.locator(self.selectors.sample_email_sent_text_xpath)
            # TBD when sample email reaching inbox delay is resolved
            # time.sleep(5)
            # gmail_session = Email(login=edit_portal_data['sample_email'],
            # password=edit_portal_data['sample_password'])
            # time.sleep(5)
            # sample_email_subject =
            # gmail_session.get_subject_from_mail(_mail=edit_portal_data['sample_email'])
            if 'Sample Email Sent.' in email_sent.inner_text():
                self.pw_utils.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("element not present")
        except Exception as e:
            log.error("not able to locate the edit section of customization page {}".format(e))
            return False
