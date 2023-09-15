import requests
import click
import logging
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
            tr_config=None,
            case_ids=None):
        self.password = password
        self.url = url
        self.email = email
        self.project_id = project_id
        self.headers = {"Content-Type": "application/json"}
        self.description = 'This Run is created from Automated code.'
        self.include_all = False
        self.tr_config = tr_config
        self.case_ids = case_ids
        if case_ids is None:
            self.include_all = True
        else:
            self.case_ids = [int(case.replace('C', '')) if 'C' in case else int(
                case) for case in case_ids.split(",")]

    def create_plan(self, plan_file):
        """Create a Test Plan in TestRail.
        Args:
            plan_file: Abosulte Json file path containing the plan detail.
        Returns:
            0 (store testrail configuration file in tr_config path)
            or
            -1
        """
        now = datetime.now()
        time = now.strftime("%B-%d-%Y %H:%M:%S")
        milestone_id = None
        plan = ""
        try:
            add_plan_url = f"{self.url}/index.php?/api/v2/add_plan/{self.project_id}"
            plan = ""
            with open(plan_file) as json_file:
                plan = json.load(json_file)
            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time

            if plan.get('milestone_id') is not None:
                milestone_id = plan.get('milestone_id')

            response = requests.post(
                add_plan_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(plan),
                verify=False
            )

            if response.status_code == 200:
                LOG.info(response.json())
                plan_id = response.json()['id']
                for entry in response.json()['entries']:
                    self.create_testrail_config_file(
                        suite_id=entry["suite_id"],
                        run_id=entry["runs"][0]["id"],
                        run_name=entry["runs"][0]["name"],
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                        file_path="{}".format(
                            os.path.join(
                                self.tr_config,
                                "testrail-{}.cfg".format(
                                    entry["suite_id"]))))
                LOG.info(f"Run Id: {plan_id} got created.")
                return 0
            else:
                LOG.error("Failed to Plan in TestRail.")
                LOG.error(f"TestRail Response: {response.status_code}")
                return -1
        except Exception as e:
            LOG.error(e)
            return -1

    def update_plan(self, plan_id, plan_file):
        """Update a existing Test Plan in TestRail.
        Args:
            plan_id: ID of the existing plan.
            plan_file: Abosulte Json file path containing the plan detail.
        Returns:
            0 (store testrail configuration file in tr_config path)
            or
            -1
        """

        now = datetime.now()
        time = now.strftime("%B-%d-%Y %H:%M:%S")
        milestone_id = None
        plan = ""
        try:
            update_plan_url = f"{self.url}/index.php?/api/v2/add_plan_entry/{plan_id}"

            with open(plan_file) as json_file:
                plan = json.load(json_file)

            if plan.get('milestone_id') is not None:
                milestone_id = plan.get('milestone_id')

            for entry in plan["entries"]:
                entry["name"] = entry["name"] + " - " + time
                response = requests.post(
                    update_plan_url,
                    headers=self.headers,
                    auth=(self.email, self.password),
                    data=json.dumps(entry),
                    verify=False
                )

                if response.status_code == 200:
                    plan_updated = response.json()
                    self.create_testrail_config_file(
                        suite_id=plan_updated["suite_id"],
                        run_id=plan_updated["runs"][0]["id"],
                        run_name=plan_updated["runs"][0]["name"],
                        plan_id=plan_id,
                        milestone_id=milestone_id,
                        file_path="{}".format(
                            os.path.join(
                                self.tr_config,
                                "testrail-{}.cfg".format(
                                    plan_updated["suite_id"]))))
                else:
                    LOG.error(
                        "Failed to update plan with new runs for suite id {}.".format(
                            entry["suite_id"]))
            LOG.info(f"Plan ID {plan_id} got updated.")
            return 0
        except Exception as e:
            LOG.error(e)
            return -1

    def create_run(self, suite_id, run_name=None, milestone_id=None):
        """Create a Run in TestRail.
        Args:
            suite_id: ID of the Test Suite ID.
            run_name (Optional): Name of the Run Name
            milestone_id (Optional): Milestone ID.
        Returns:
            0 (store testrail configuration file in tr_config path)
            or
            -1
        """

        now = datetime.now()
        time = now.strftime("%B-%d-%Y %H:%M:%S")
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
            if self.case_ids is None:
                data["include_all"] = self.include_all
            else:
                data["include_all"] = self.include_all
                data["case_ids"] = self.case_ids

            if milestone_id is not None:
                data["milestone_id"] = int(milestone_id)

            response = requests.post(
                add_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
                verify=False
            )
            if response.status_code == 200:
                run_id = response.json()['id']
                self.create_testrail_config_file(
                    suite_id=suite_id,
                    run_id=run_id,
                    run_name=run_name,
                    plan_id=None,
                    milestone_id=milestone_id,
                    file_path="{}".format(
                        os.path.join(
                            self.tr_config,
                            'testrail.cfg')))
                LOG.info(f"Run Id: {run_id} got created.")
                return 0
            else:
                LOG.error("Failed to created Run in TestRail.")
                LOG.error(f"TestRail Response: {response.status_code}")
                return -1
        except Exception as e:
            LOG.error(e)
            return -1

    def update_result(self, run_id, result_file):
        """Update Result in Testrail which Automated using Postman.
        Args:
            run_id: ID of the Test RUN.
            result_file: Absolute Path of the file containing test result.
        Returns:
            0 (store testrail configuration file in tr_config path)
            or
            -1
        """
        try:
            update_result_run_url = f"{self.url}/index.php?/api/v2/add_results_for_cases/{run_id}"

            data = ""
            with open(result_file) as json_file:
                data = json.load(json_file)

            response = requests.post(
                update_result_run_url,
                headers=self.headers,
                auth=(self.email, self.password),
                data=json.dumps(data),
                verify=False
            )
            if response.status_code == 200:
                LOG.info(f"Result in Run Id {run_id} got updated.")
                return 0
            else:
                LOG.error(
                    "Failed to update result in Run ID {} in TestRail.".format(run_id))
                LOG.error(f"TestRail Response: {response.status_code}")
                return -1
        except Exception as e:
            LOG.error(e)
            return -1

    def create_testrail_config_file(
            self,
            suite_id,
            run_id,
            run_name,
            plan_id,
            milestone_id,
            file_path):
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
        if plan_id is not None:
            config.set('TESTRUN', 'plan_id', str(plan_id))
        if milestone_id is not None:
            config.set('TESTRUN', 'milestone_id', str(milestone_id))

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as configfile:
            config.write(configfile)


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
    '''
    Command for creating a Test Run for a Test Suite.
    '''

    password = ""
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        project_id=project_id,
        case_ids=case_ids,
        password=password,
        tr_config=tr_config
    )
    tr.create_run(
        suite_id=suite_id,
        run_name=run_name,
        milestone_id=milestone_id)
    print("TestRail configuration file is created in {}".format(tr_config))


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
    '''
    Command for creatig a Test Plan.
    '''
    """This will return a set path which contains multiple testrail.cfg for same test plan for different suite."""

    password = ""
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
    tr.create_plan(plan_file)
    print("TestRail configuration files are created in {} path for same plan.".format(tr_config))


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
    '''
    Command for creating new test runs in already created plan.
    '''

    password = ""
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        password=password,
        tr_config=tr_config
    )
    tr.update_plan(plan_id, plan_file)
    print("TestRail configuration files are created in {} path for same plan.".format(tr_config))


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
    '''
    This command is used to update one or more new test results, comments or assigns
    one or more tests (using the case IDs).
    Ideal for test automation to bulk-add multiple test results in one step.
    '''
    password = ""
    with open(password_file) as json_file:
        data = json.load(json_file)
        password = data["token"]

    tr = TestRail(
        url=url,
        email=email,
        password=password
    )
    tr.update_result(run_id, result_file)
    print("Result for Run ID {} updated in TestRail.".format(run_id))


if __name__ == "__main__":
    main()
