"""
Manage CCS Folder Details page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.activate_folder_details_page import ActivateFolderDetails

log = logging.getLogger(__name__)


class TacFolderDetails(ActivateFolderDetails):
    """
    Manage CCS Folder Devices page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Manage CCS Folder Details page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Manage CCS Folder Details page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-ccs/customers/customer-details/folders/folder-details"
