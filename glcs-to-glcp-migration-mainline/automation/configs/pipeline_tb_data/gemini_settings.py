def gemini_test_data(url):
    """
    Usage: Test bed data will be initialized in conftest.py
    define username, acct_name, app_name, device serials, subscriptions in this file
    Password and api_secret need to be in user_creds.json file
    """
    tb_data = {}
    tb_data["test_or_workflow_name1"] = {}
    tb_data["test_or_workflow_name2"] = {}
    if "gemini" in url:
        tb_data["url"] = url
        tb_data["test_or_workflow_name1"]["username"] = "hcloud203+usfampv@gmail.com"
        tb_data["test_or_workflow_name1"]["account_name"] = "account_name1"
        tb_data["test_or_workflow_name1"]["app_api_user"] = "_api"
        return tb_data
