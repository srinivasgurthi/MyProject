import requests
import logging
import click
import json
import sys
import os
import configparser
import requests
import json
from datetime import datetime

LOG = logging.getLogger(__name__)


class TestRail:
    def __init__(
            self,
            url,
            email,
            password,
            project_id=None,
            tr_config="/tmp",
    ):
        """
        Initializes the TestRail object with the TestRail API URL, email, password, project ID, headers, description,
        and TestRail configuration path.

        Args:
            url (str): The TestRail API URL.
            email (str): The email address associated with the TestRail account.
            password (str): The password associated with the TestRail account.
            project_id (int): The ID of the project in TestRail.
            tr_config (str): The TestRail configuration path.
        """
        self.password = password
        self.url = url
        self.email = email
        self.project_id = project_id
        self.headers = {"Content-Type": "application/json"}
        self.description = 'This Run is created from Automated code.'
        self.tr_config = tr_config

    def create_plan(self, plan_file):
        """
        Creates a Test Plan in TestRail.

        Args:
            plan_file (str): The absolute path of the JSON file containing the plan detail.

        Returns:
            {} if the creation is successful, else None.
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            add_plan_url = f"{self.url}/index.php?/api/v2/add_plan/{self.project_id}"
            with open(plan_file) as json_file:
                plan = json.load(json_file)
            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time
            milestone_id = plan.get('milestone_id')
            response = requests.post(
                add_plan_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(plan)
            )

            if response.status_code == 200:
                LOG.info(response.json())
                plan_id = response.json()['id']
                for entry in response.json()['entries']:
                    file = f"testrail-{entry['suite_id']}-{time}.cfg"
                    file_path = "{}".format(
                        os.path.join(self.tr_config, file)
                    )
                    self.create_testrail_config_file(
                        suite_id=entry["suite_id"],
                        run_id=entry["runs"][0]["id"],
                        run_name=entry["runs"][0]["name"],
                        file_path=file_path,
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                    )

                    output_data = {
                        "suite_id": int(entry["suite_id"]),
                        "run_id": entry["runs"][0]["id"],
                        "configuration_file": file_path,
                        "plan_id": plan_id
                        }
                    if milestone_id:
                        output_data["milestone_id"] = milestone_id
                    output["TestRail"].append(
                        output_data
                    )
                LOG.info(f"Plan Id: {plan_id} got created.")
                return output
            else:
                LOG.error(
                    f"Failed to create Test Plan in TestRail with error: {response.status_code}")
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def update_plan(self, plan_id, plan_file):
        """Update an existing Test Plan in TestRail with new test runs.

        Args:
            plan_id (int): The ID of the existing plan to update.
            plan_file (str): The absolute file path to the JSON file containing the plan details.

        Returns:
            dict: A dictionary containing information about the updated Test Plan.

        Raises:
            Exception: If an error occurs while updating the Test Plan.
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            update_plan_url = f"{self.url}/index.php?/api/v2/add_plan_entry/{plan_id}"
            with open(plan_file) as json_file:
                plan = json.load(json_file)

            milestone_id = plan.get('milestone_id')

            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time
                response = requests.post(
                    update_plan_url,
                    headers=self.headers,
                    auth=(self.email, self.password),
                    data=json.dumps(entry)
                )
                if response.status_code == 200:
                    plan_updated = response.json()
                    file = f"testrail-{plan_updated['suite_id']}-{time}.cfg"
                    file_path = "{}".format(
                        os.path.join(self.tr_config, file)
                    )
                    self.create_testrail_config_file(
                        suite_id=plan_updated["suite_id"],
                        run_id=plan_updated["runs"][0]["id"],
                        run_name=plan_updated["runs"][0]["name"],
                        file_path=file_path,
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                    )

                    output_data = {
                            "suite_id": int(plan_updated["suite_id"]),
                            "run_id": plan_updated["runs"][0]["id"],
                            "configuration_file": file_path,
                            "plan_id": plan_id
                        }
                    if milestone_id:
                        output_data["milestone_id"] = milestone_id

                    output["TestRail"].append(output_data)

                else:
                    LOG.error(
                        "Failed to update plan with new runs for suite id {}.".format(
                            entry["suite_id"]))
                    output["TestRail"][0].append(
                        {
                            "suite_id": int(entry["suite_id"]),
                            "error": "Failed to update plan with new runs for suite id {}."
                        }
                    )
            LOG.info(f"Plan ID {plan_id} got updated.")
            return output
        except Exception as e:
            LOG.error(e)
            return None

    def create_run(
            self,
            suite_id,
            run_name=None,
            milestone_id=None,
            case_ids=None):
        """Create a new TestRail test run and returns the run ID along with its configuration file path.

        Args:
            suite_id (int): The ID of the Test Suite.
            run_name (str, optional): The name of the test run. If None, a default name with the current timestamp will
            be used.
            milestone_id (int, optional): The ID of the milestone to link the test run to.
            case_ids (List[str], optional): The list of case IDs to include in the test run. If None, all cases in the
            suite will be included.
        Returns:
            A dictionary containing information about the created test run, including the Test Suite ID, Run ID, and
            the configuration file path. Returns None if the test run creation fails.
        Raises:
            None
        """
        output = {"TestRail": []}
        now = datetime.utcnow()
        time = now.strftime("%B-%d-%Y-%H:%M:%S")
        try:
            add_run_url = f"{self.url}/index.php?/api/v2/add_run/{self.project_id}"
            if run_name is None:
                run_name = "Automated Run - " + time
            else:
                run_name = "{}-{}".format(run_name, time)

            data = {
                "suite_id": int(suite_id),
                "name": run_name
            }
            if case_ids is None:
                data["include_all"] = True
            else:
                data["include_all"] = False
                data["case_ids"] = [int(case.replace('C', '')) if 'C' in case else int(
                    case) for case in case_ids]

            if milestone_id is not None:
                data["milestone_id"] = int(milestone_id)

            response = requests.post(
                add_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data)
            )
            if response.status_code == 200:
                run_id = response.json()['id']
                file = f"testrail-{suite_id}-{time}.cfg"
                file_path = "{}".format(
                    os.path.join(self.tr_config, file))
                self.create_testrail_config_file(
                    suite_id=suite_id,
                    run_id=run_id,
                    run_name=run_name,
                    plan_id=None,
                    milestone_id=None,
                    file_path=file_path)
                LOG.info(f"Run Id: {run_id} got created.")
                output_data = {
                        "suite_id": int(suite_id),
                        "run_id": int(run_id),
                        "configuration_file": file_path
                    }
                if milestone_id:
                    output_data["milestone_id"] = milestone_id
                output["TestRail"].append(output_data)
                return output
            else:
                LOG.error(
                    f"Failed to created Run in TestRail: Error {response.status_code}")
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def update_result(self, run_id, result_file):
        """Update test results for a TestRail test run.

        Args:
            run_id (int): ID of the TestRail test run.
            result_file (str): Absolute path of the JSON file containing test results.
        Returns:
            bool: True if the test results were successfully updated, False otherwise.
        """
        try:
            update_result_run_url = f"{self.url}/index.php?/api/v2/add_results_for_cases/{run_id}"

            with open(result_file) as json_file:
                data = json.load(json_file)

            response = requests.post(
                update_result_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data)
            )
            if response.status_code == 200:
                LOG.info(f"Result in Run Id {run_id} got updated.")
                return True
            else:
                LOG.error(
                    "Failed to update result in Run ID {} in TestRail.".format(run_id))
                LOG.error(f"TestRail Response: {response.status_code}")
                return None
        except Exception as e:
            LOG.error(e)
            return None

    def create_testrail_config_file(
            self,
            suite_id,
            run_id,
            run_name,
            file_path,
            plan_id,
            milestone_id):
        """Create a configuration file for TestRail.

        The configuration file will contain the following information:
        - API URL, email, and password
        - Test run details such as project ID, suite ID, run ID, and run name
        - Plan and milestone IDs (if provided)

        Args:
            suite_id: ID of the Test Suite.
            run_id: ID of the Test Run.
            run_name: Name of the Test Run.
            file_path: Absolute path of the configuration file to be created.
            plan_id (Optional): Plan ID.
            milestone_id (Optional): Milestone ID.

        Returns:
            None
        """
        config = configparser.ConfigParser()
        config.add_section('API')
        config.set('API', 'url', self.url)
        config.set('API', 'email', self.email)
        config.set('API', 'password', self.password)
        config.add_section('TESTRUN')
        config.set('TESTRUN', 'project_id', str(self.project_id))
        config.set('TESTRUN', 'suite_id', str(suite_id))
        config.set('TESTRUN', 'run_id', str(run_id))
        config.set('TESTRUN', 'run_name', run_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if plan_id is not None:
            config.set('TESTRUN', '#plan_id', str(plan_id))
        if milestone_id is not None:
            config.set('TESTRUN', '#milestone_id', str(milestone_id))
        with open(file_path, 'w') as configfile:
            config.write(configfile)

    def get_milestone_id(self, milestone_name):
        """Get milestone ID for the given milestone name.

        Args:
            milestone_name (str): Name of the milestone.

        Returns:
            milestone_id (int or None): ID of the milestone if found, otherwise None.
        """
        try:
            response = requests.get(
                f'{self.url}/index.php?/api/v2/get_milestones/{self.project_id}',
                headers=self.headers,
                auth=(
                    self.email,
                    self.password))
            if response.status_code == 200:
                milestone_id = None
                for milestone in response.json()["milestones"]:
                    if milestone['name'] == milestone_name:
                        milestone_id = milestone['id']
                return milestone_id
            else:
                LOG.error(
                    f"Failed to get milestone id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def get_plan_id(self, plan_name):
        """Get the Test Plan ID for the specified plan name.

        Args:
            plan_name (str): The name of the Test Plan.

        Returns:
            int or None: The Test Plan ID, or None if the request was unsuccessful.
        """
        try:
            response = requests.get(
                f'{self.url}/index.php?/api/v2/get_plans/{self.project_id}',
                headers=self.headers,
                auth=(self.email, self.password)
            )
            if response.status_code == 200:
                plan_id = None
                for plan in response.json()["plans"]:
                    if plan['name'] == plan_name:
                        plan_id = plan['id']
                return plan_id
            else:
                LOG.error(f"Failed to get plan id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")

    def get_suite_id(self, suite_name):
        """Get the ID of the Test Suite with the specified name.

        Args:
            suite_name (str): The name of the Test Suite.

        Returns:
            int or None: The ID of the Test Suite if it exists, or None otherwise.

        """
        try:
            response = requests.get(
                f'{self.url}/index.php?/api/v2/get_suites/{self.project_id}',
                headers=self.headers,
                auth=(self.email, self.password)
            )
            if response.status_code == 200:
                suite_id = None
                for suite in response.json():
                    if suite['name'] == suite_name:
                        suite_id = suite['id']
                return suite_id
            else:
                LOG.error(f"Failed to get suite_id id: {response.status_code}")
                return None
        except Exception as e:
            LOG.exception(f"Error: {e}")


@click.group()
def main():
    """
    Command for creating TestRun and TestPlan in TestRail.
    """
    pass


@main.command()
@click.option('--email',
              required=True,
              help="Email address of a TestRail User.",
              type=str)
@click.option('--url', required=True, help="URL of the TestRail.", type=str)
@click.option('--project_id', required=True,
              help="TestRail Project ID.", type=str)
@click.option('--suite_id', required=True, help="TestRail Suite ID.", type=str)
@click.option('--milestone_id', required=False, default=None,
              help="TestRail Milestone ID.", type=str)
@click.option('--case_ids', default=None,
              help="(,) separated case ids.", type=str)
@click.option('--run_name',
              default="Automated",
              help="Name of the Run (Date will be auto added in name)",
              type=str)
@click.option('--tr_config', required=True,
              help="Path where you want to save tr_config file.", type=str)
@click.option('--password_file',
              required=True,
              help="Full path of file where TestRail API key exist.",
              type=click.Path(exists=True))
def create_run(
        email,
        url,
        project_id,
        suite_id,
        run_name,
        case_ids,
        tr_config,
        password_file,
        milestone_id):
    """
    Command for creating a Test Run for a Test Suite.
    """

    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    if case_ids is not None:
        case_ids = case_ids.split(",")

    tr = TestRail(
        url=url,
        email=email,
        project_id=project_id,
        password=password,
        tr_config=tr_config
    )
    status = tr.create_run(
        suite_id=suite_id,
        run_name=run_name,
        case_ids=case_ids,
        milestone_id=milestone_id)
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Run.")
        sys.exit(-1)


@main.command()
@click.option('--email',
              required=True,
              help="Email address of a TestRail User.",
              type=str)
@click.option('--url', required=True, help="URL of the TestRail.", type=str)
@click.option('--project_id', required=True,
              help="TestRail Project ID.", type=str)
@click.option('--plan_file', required=True,
              help="Full path of the plan json file.", type=str)
@click.option('--tr_config', required=True,
              help="Path where you want to save tr_config file.", type=str)
@click.option('--password_file',
              required=True,
              help="Full path of file where TestRail API key exist.",
              type=click.Path(exists=True))
def create_plan(email, url, project_id, plan_file, tr_config, password_file):
    """
    Command for creatig a Test Plan.
    """
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        project_id=project_id,
        password=password,
        tr_config=tr_config
    )
    status = tr.create_plan(plan_file)
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Plan.")
        sys.exit(-1)


@main.command()
@click.option('--email',
              required=True,
              help="Email address of a TestRail User.",
              type=str)
@click.option('--url', required=True, help="URL of the TestRail.", type=str)
@click.option('--plan_id', required=True, help="TestRail Plan ID.", type=str)
@click.option('--plan_file', required=True,
              help="Full path of the plan json file.", type=str)
@click.option('--tr_config', required=True,
              help="Path where you want to save tr_config file.", type=str)
@click.option('--password_file',
              required=True,
              help="Full path of file where TestRail API key exist.",
              type=click.Path(exists=True))
def update_plan(email, url, plan_id, plan_file, tr_config, password_file):
    """
    Command for creating new test runs in already created plan.
    """

    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        password=password,
        tr_config=tr_config
    )
    status = tr.update_plan(plan_id, plan_file)
    if status is not None:
        click.echo(status)
        sys.exit(0)
    else:
        click.echo("Failed to create a Test Run.")
        sys.exit(-1)


@main.command()
@click.option('--email',
              required=True,
              help="Email address of a TestRail User.",
              type=str)
@click.option('--url', required=True, help="URL of the TestRail.", type=str)
@click.option('--run_id', required=True, help="TestRail Run ID.", type=str)
@click.option('--result_file', required=True,
              help="Full path of the result json file.", type=str)
@click.option('--password_file',
              required=True,
              help="Full path of file where TestRail API key exist.",
              type=click.Path(exists=True))
def update_result(email, url, run_id, result_file, password_file):
    """
    This command is used to update one or more new test results, comments or assigns
    one or more tests (using the case IDs).
    Ideal for test automation to bulk-add multiple test results in one step.
    """
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        password=password
    )
    status = tr.update_result(run_id, result_file)
    if status is not None:
        click.echo(f"Test Result update to Test Run ID: {run_id}")
        sys.exit(0)
    else:
        click.echo("Failed to update result in Test Run.")
        sys.exit(-1)


if __name__ == "__main__":
    main()
