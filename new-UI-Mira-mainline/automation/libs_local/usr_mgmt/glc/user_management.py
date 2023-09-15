# Copyright 2023 - Hewlett Packard Enterprise Company
"""GLC user management page"""

import logging
import re
from playwright.sync_api import expect


LOG = logging.getLogger(__name__)


class UserMgmtPage(object):
    """GLC authn page"""

    def __init__(self) -> None:
        LOG.info(f"Initialize {__name__}")

    def navigate_to_glc_tennant(self, page, tennant):
        """
        Navigate to GLC tenant with page and tenant 
        page: param (required)
        tenant: param (required)
        """
        LOG.info(f"Navigate to {tennant} tennant.")
        try:
            expect(page).to_have_url(re.compile("choose"), timeout=30000)
            if "choose" in page.url:
                page.get_by_text(tennant).click()
        except:
            return
        
    def open(self, page) -> None:
        """
        Open User Management Page for page {page} 
        page: param (required)
        returns None
        """
        LOG.info("Open User Management Page.")
        page.get_by_role("button", name="Dashboard").click()
        page.wait_for_load_state("networkidle")
        page.get_by_role("button", name="Configure").click()
        page.wait_for_load_state("networkidle")
        page.get_by_role("menuitem", name="User Management").click()
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("button", name="Overview")).to_be_visible()
        expect(
            page.get_by_role("button", name="UserAdd Users")
        ).to_be_visible()
        expect(
            page.get_by_text(
                "UsersManage users, user status, and role assignment.Invite UserUser GroupsGroup "
            )
        ).to_be_visible()
        expect(
            page.get_by_role("button", name="Group User Groups")
        ).to_be_visible()
        expect(
            page.get_by_role("button", name="ContactInfo Roles")
        ).to_be_visible()
        expect(
            page.get_by_text(
                "UsersManage users, user status, and role assignment.Invite UserUser GroupsGroup "
            )
        ).to_be_visible()

    def _search_user(self, page, email_address):
        """
        Search user with page {page} and with email {email_address} 
        email_address: param (required)
        returns None
        """
        LOG.info(f"Searching user {email_address}")
        page.get_by_role("button", name="Users", exact=True).click()
        page.wait_for_load_state("networkidle")
        page.get_by_placeholder(
            "Enter a name, id or email address to search for users."
        ).fill(email_address.split("@")[0])
        page.wait_for_load_state("networkidle")
        page.get_by_text(email_address).click()

    def invite_user(
        self, page, firstname, lastname, email_address, country="United States - US"
    ) -> None:
        """
        Invite User with page {page} and firstname, {lastname}, {emailaddress} and with {country}
        returns None
        """
        
        LOG.info(f"Invite user {firstname} {lastname}  Email address: {email_address}")
        self.open(page)
        page.get_by_role("button", name="Invite User").click()
        expect(
            page.get_by_text("Invite a user to this tenant.")
        ).to_be_visible()
        page.get_by_label("First Name*").fill(firstname)
        page.get_by_label("Last Name*").fill(lastname)
        page.get_by_label("Primary Email*").fill(email_address)
        page.get_by_placeholder("Select Country").click()
        page.get_by_role("searchbox").fill(country)
        page.get_by_role("option", name=country).click()
        page.get_by_role("button", name="Invite User").click()
        page.get_by_role("button", name="Invite User").is_enabled()
        expect(page.get_by_text("Form Submission Error")).not_to_be_visible()
        expect(
            page.get_by_text("Internal Error - An internal error has occurred.")
        ).not_to_be_visible()
        LOG.info("Done inviting user.")

    def uninvite_user(self, page, email_address) -> None:
        """
        Uninvite User for page {page} and {emailaddress} 
        page: required
        email_address: required 
        returns None
        """
        LOG.info(f"Uninvite user {email_address}")
        self.open(page)
        self._search_user(page, email_address)
        page.get_by_role("button", name="Open Menu").click()
        page.get_by_role("menuitem", name="Uninvite").click()
        page.locator("label div").nth(1).click()
        page.get_by_role("button", name="Yes, Uninvite").click()
        LOG.info("Done uninviting user.")
        return True

    def create_assignment(
        self, page, email_address: str, role: str, space: str = "Default"
    ) -> None:
        """
        Create assignment for page {page} and {emailaddress} and with {space}
        page: required
        email_address: required
        role: required
        space: Optional
        returns None
        """
        LOG.info(f"Create assignment {role} for user {email_address}")
        self.open(page)
        self._search_user(page, email_address)
        page.get_by_role("button", name="Open Menu").click()
        page.get_by_role("menuitem", name="Create Assignment").click()
        page.locator("label").filter(has_text=f"{role}").locator("div").nth(
            1
        ).click()
        page.get_by_role("button", name="Space").click()
        page.get_by_role("option", name=f"{space}").click()
        page.locator("label").filter(
            has_text="I confirm that I want to create the assignments listed above."
        ).locator("div").nth(1).click()
        page.get_by_role("button", name="Create Assignment").click()
        page.wait_for_load_state("networkidle")
        page.get_by_role("tab", name="Assignments").click()
        page.get_by_role("button", name="IAM Owner").click()
        page.get_by_role("button", name="Close").click()

    def delete_assignment(self, page, email_address: str, role: str) -> None:
        """
        Delete assignment  {page} and {emailaddress} and {tenant} 
        page: required
        tenant: required
        email_address: required 
        returns None
        """
        LOG.info(f"Delete assignment {role} from user {email_address}")
        self.open(page)
        self._search_user(page, email_address)
        page.get_by_role("tab", name="Assignments").click()
        page.get_by_role("button", name=f"{role}").click()
        page.get_by_role("button", name="Close").click()
        page.get_by_role("button", name="Trash").click()
        page.get_by_role("button", name="Yes, Remove").click()

    def tenant_should_not_be_visible(self, page, tenant):
        """
        check Tenant visible for {page} and with {tenant} 
        page: required
        tenant: required 
        returns None
        """
        page.get_by_role("button", name="User").click()
        expect(page.get_by_text(f"Tenant: {tenant}")).not_to_be_visible()

    def verify_useremail_and_tenant_in_glc(self, page, useremail, tenant):
        """
        Verify email in tenant in GLC {page} and {emailaddress} and {tenant} 
        page: required
        tenant: required
        email_address: required 
        returns None
        """
        page.wait_for_load_state()
        page.get_by_role("button", name="User", exact = True).click()
        page.wait_for_load_state()
        return page.get_by_text(useremail).is_visible() and page.get_by_text(tenant).is_visible()

    def check_user(self, page, email_address: str) -> bool:
        """
        check  User for page {page} and {emailaddress}  
        page: required
        email_address: required 
        returns None
        """
        LOG.info(f"Searching for user {email_address}")
        page.get_by_role("button", name="Users", exact=True).click()
        page.wait_for_load_state("networkidle")
        page.get_by_placeholder(
            "Enter a name, id or email address to search for users."
        ).fill(email_address.split("@")[0])
        page.wait_for_load_state("networkidle")
        try:
            return page.get_by_text(email_address).is_enabled()  
        except:
            return False

    def suspend_user(self, page, email_address: str) -> None:
        """
        Suspend User for page {page} and {emailaddress}  
        page: required
        email_address: required 
        returns None
        """
        LOG.info(f"Supending {email_address} user")
        self.open(page)
        self._search_user(page, email_address)
        page.get_by_role("button", name="Open Menu").click()
        if page.get_by_role("menuitem", name="Suspend").is_visible():
            page.get_by_role("menuitem", name="Suspend").click()
            page.get_by_role("button", name="Yes, Suspend").click()
            return True
        else:
            LOG.info(f"User {email_address} is already suspended.")
            return False
    
    def check_assignment(self, page, email_address: str, assignment: str) -> bool:
        """
        check assignment User for page {page} and {emailaddress} and {assignment} 
        page: required
        email_address: required 
        returns None
        """
        LOG.info(f"Check {assignment} for {email_address}")
        self._search_user(page, email_address)
        page.get_by_role("tab", name="Assignments").click()
        page.get_by_placeholder(re.compile("Assignments")).fill(assignment)
        return page.get_by_role("button", name=assignment).is_visible()

    def signout(self, page):
        """
        Signout User for page {page} 
        page: required
        returns None
        """
        page.get_by_role("button", name="User", exact = True).click()
        try:
            expect(page.get_by_role("menuitem", name="Log Out")).to_be_visible()
        except AssertionError:
            page.get_by_role("button", name="User", exact = True).click()

        LOG.info("Signing out ...")
        page.get_by_role("menuitem", name="Log Out").click()
