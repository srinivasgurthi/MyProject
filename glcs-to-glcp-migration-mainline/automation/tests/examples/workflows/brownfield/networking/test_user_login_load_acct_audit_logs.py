import pytest
from automation.tests.examples.workflows.brownfield.networking.user_login_load_acct_audit_logs import WfUserLoginLoadAcctAudit

@pytest.mark.first
@pytest.mark.Regression
def test_get_audit_log_sm_details_iap(browser_instance, logged_in_storage_state):
    create_test = WfUserLoginLoadAcctAudit()
    assert create_test.wf_sm_iap_audit_log_info(browser_instance, logged_in_storage_state)

@pytest.mark.second
@pytest.mark.Regression
def test_get_audit_log_sm_details_sw(browser_instance, logged_in_storage_state):
    create_test = WfUserLoginLoadAcctAudit()
    assert create_test.wf_sm_sw_audit_log_info(browser_instance, logged_in_storage_state)