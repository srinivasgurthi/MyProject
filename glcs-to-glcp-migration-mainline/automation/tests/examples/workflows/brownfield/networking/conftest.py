import pytest
from automation.tests.examples.\
    workflows.brownfield.networking.user_login_load_acct_audit_logs import WfUserLoginLoadAcctAudit

@pytest.fixture(scope="session")
def logged_in_storage_state(browser_instance):
    create_test = WfUserLoginLoadAcctAudit()
    yield create_test.wf_webui_login(browser_instance)