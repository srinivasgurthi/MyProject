import requests
import logging
import traceback
import time
import sys
import os
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import threading

lock = threading.Lock()
log = logging.getLogger(__name__)

class Sel_Class(object):
    def __init__(self):
        log.info("selenium class")

    def restart_docker_sel_hub(self):
        log.info("cleaning up previous sessions")
        os.system("docker ps -a | grep selenium | awk '{print $1}' | xargs -L1 docker stop")
        os.system("docker ps -a | grep selenium | awk '{print $1}' | xargs -L1 docker rm")
        time.sleep(3)
        log.info("adding selenium hub and webdriver docker")
        # os.system("docker run -d -p 4446:4444 --name selenium-hub1 -P selenium/hub")
        # os.system("docker run -d -P --link selenium-hub1:hub selenium/node-chrome-debug")
        os.system(
            "docker run -d -p 4444:4444 -p 7900:7900 --shm-size='2g' selenium/standalone-chrome:4.1.0-prerelease-20211105")
        time.sleep(30)
        return

    def check_local_sel_hub(self, url1, hub_rst=None):
        try:
            url = url1 + '/status'
            response = requests.get(url, timeout=2)
            log.info("hub status response {}".format(response.content))
            hub_ready = False
            json_status = response.json()
            if 'ready' in response.json()['value']:
                if json_status['value']['ready'] == True:
                    hub_ready = True
            if hub_ready == False and not hub_rst:
                self.restart_docker_sel_hub()
                time.sleep(15)
                response = requests.get(url, timeout=2)
                log.info("hub status response {}".format(response.content))
            return True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.info(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            return False

    def check_k8s_sel_hub(self, url1):
        try:
            url = url1 + '/status'
            response = requests.get(url, timeout=2)
            hub_ready = False
            json_status = response.json()
            log.info("hub status response {}".format(response.json()))
            if 'ready' in response.json()['value']:
                if json_status['value']['ready'] == True:
                    hub_ready = True
            if hub_ready == False:
                self.restart_k8s_sel()
                time.sleep(15)
                response = requests.get(url, timeout=2)
                log.info("hub status response {}".format(response.json()))
            return True
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.info(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            return False

    def save_screen(self, driver, file_name):
        try:
            result = driver.save_screenshot(file_name)
            if not result:
                log.error("not able to take screenshot")
        except Exception as e:
            log.error("not able to take screenshot {}".format(e))
            pass

    def get_driver_with_restart(self, browser="chrome"):
        try:
            lock.acquire(timeout=60)
        except Exception as e:
            log.info("lock timeout {}".format(e))
        try:
            hub_restart = os.getenv("SEL_HUB_RESTARTED")
        except:
            hub_restart = None
        driver = None
        try:
            if not os.getenv("POD_NAMESPACE"):
                url = "http://selenium-hub:4444"
                # url = "http://127.0.0.1:4444"
                # url = "localhost:4446/wd/hub"
                self.check_local_sel_hub(url, hub_rst=hub_restart)
                os.environ["SEL_HUB_RESTARTED"] = "1"
            else:
                namespace = os.getenv("POD_NAMESPACE")
                url = "http://selenium-hub.{}.svc.cluster.local.:4444/wd/hub".format(
                    namespace
                )
                self.check_k8s_sel_hub(url)
                os.environ["SEL_HUB_RESTARTED"] = "1"
                log.info("connecting to remote webdriver url {}".format(url))
            if browser == "chrome":
                option = webdriver.ChromeOptions()
                capabilities = DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
                option.add_argument("--headless")
                option.add_argument("window-size=2460,1684")
                option.add_argument("--disable-gpu")
                option.page_load_strategy = 'normal'
                RemoteConnection.set_timeout(60)
                option = webdriver.ChromeOptions()
                driver = webdriver.Remote(command_executor=url, options=option, desired_capabilities=capabilities)
            if "selenium.webdriver.remote.webdriver.WebDriver (session=" in str(driver):
                self.lock_relase(lock)
                log.info("got driver value {}".format(driver))
                return driver
            else:
                self.lock_relase(lock)
                log.error("not able to get driver {}".format(str(driver)))
                return False
        except Exception as e:
            self.lock_relase(lock)
            log.error("not able to connect to remote webdriver {}".format(e))
            return False


    def get_driver_no_restart(self, browser="chrome"):
        try:
            lock.acquire(timeout=60)
        except Exception as e:
            log.info("lock timeout {}".format(e))
        driver = None
        try:
            if not os.getenv("POD_NAMESPACE"):
                # url = "http://selenium-hub:4444"
                url = "http://127.0.0.1:4444"
                # url = "localhost:4446/wd/hub"
            else:
                namespace = os.getenv("POD_NAMESPACE")
                url = "http://selenium-hub.{}.svc.cluster.local.:4444/wd/hub".format(
                    namespace
                )
                log.info("connecting to remote webdriver url {}".format(url))
            if browser == "chrome":
                option = webdriver.ChromeOptions()
                capabilities = DesiredCapabilities.CHROME
                capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
                option.add_argument("--headless")
                option.add_argument("--disable-gpu")
                option.add_argument("window-size=2460,1684")
                RemoteConnection.set_timeout(60)
                option = webdriver.ChromeOptions()
                driver = webdriver.Remote(
                    command_executor=url, options=option, desired_capabilities=capabilities
                )
            if "selenium.webdriver.remote.webdriver.WebDriver (session=" in str(driver):
                self.lock_relase(lock)
                log.info("got driver value {}".format(driver))
                return driver
            else:
                self.lock_relase(lock)
                log.error("not able to get driver {}".format(str(driver)))
                return False
        except Exception as e:
            self.lock_relase(lock)
            log.error("not able to connect to remote webdriver {}".format(e))
            return False


    def restart_k8s_sel(self):
        namespace = os.getenv("POD_NAMESPACE")
        cmd = (
                "kubectl get pod -n "
                + namespace
                + " | grep selenium-hub | awk '{print $1}' | xargs kubectl delete "
                  "pod -n " + namespace + " --force --grace-period=0"
        )
        os.system(cmd)
        cmd = (
                "kubectl -n "
                + namespace
                + " wait --for=condition=available --timeout=900s deployment selenium-hub"
        )
        os.system(cmd)
        time.sleep(5)
        cmd = (
                "kubectl get pod -n "
                + namespace
                + " | grep selenium-node-chrome | awk '{print $1}' | xargs kubectl "
                  "delete pod -n " + namespace + " --force --grace-period=0"
        )
        os.system(cmd)
        cmd = (
                "kubectl -n "
                + namespace
                + " wait --for=condition=available --timeout=900s deployment selenium-node-chrome"
        )
        os.system(cmd)
        time.sleep(10)
        url = "http://selenium-hub.{}.svc.cluster.local.:4444/wd/hub".format(namespace)
        return url

    def search_element_in_xpath(self, driver, inp, click=None, browser_log=None):
        count = 0
        log.info(inp)
        while count < 5:
            time.sleep(1)
            count = count + 1
            try:
                ret_value = WebDriverWait(driver, 6).until(
                    EC.visibility_of_element_located((By.XPATH, inp))
                )
                if click:
                    ret_value.click()
                    if browser_log:
                        self.get_browser_log(driver)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log.info(
                    repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                )
            else:
                count = 10
                if ret_value:
                    return ret_value
                else:
                    raise Exception

    def get_browser_log(self, driver):
        browser_log = driver.get_log("performance")
        events = self.process_browser_logs_for_network_events(browser_log)

    def search_element_clickable(self, driver, inp, click=None, browser_log=None):
        count = 0
        log.info(inp)
        while count < 7:
            time.sleep(1)
            count = count + 1
            try:
                ret_value = WebDriverWait(driver, 9).until(
                    EC.element_to_be_clickable((By.XPATH, inp))
                )
                if click:
                    if ret_value:
                        ret_value.click()
                        if browser_log:
                            self.get_browser_log(driver)
                if ret_value:
                    log.info("able to click on {}".format(ret_value))
                    return ret_value
                else:
                    log.error("not able to click")
                    raise Exception
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log.info(
                    repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
                )
                if count == 10:
                    log.error("not able to click after 10 tries")
                    raise Exception


    def typed_input(self, web_object, inp):
        log.info("web_object is: {}".format(web_object))
        log.info("Input is: {}".format(inp))
        try:
            web_object.send_keys(inp)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            log.info(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))


    def get_k8s_sel(self):
        namespace = os.getenv("POD_NAMESPACE")
        url = "http://selenium-hub.{}.svc.cluster.local.:4444/wd/hub".format(namespace)
        return url

    def lock_relase(self, lck):
        if lck.locked():
            lck.release()
            log.info("releasing the lock for get driver")


    def process_browser_logs_for_network_events(self, browser_logs):
        for entry in self.browser_logs:
            browser_log = json.loads(entry["message"])["message"]
            if (
                    "Network.responseReceived" in browser_log["method"]
                    and not "Network.responseReceivedExtraInfo" in browser_log["method"]
                    and not "Network.requestWillBeSentExtraInfo" in browser_log["method"]
                    and not "Network.responseReceivedExtraInfo" in browser_log["method"]
            ):
                log.info("web_page url: %s" % browser_log["params"]["response"]["url"])
                if browser_log["params"]["response"]["status"] != 200:
                    log.info(
                        "response status: %s" % browser_log["params"]["response"]["status"]
                    )
                    if "timing" in browser_log["params"]["response"]:
                        try:
                            if browser_log["params"]["response"]["timing"]['sendEnd'] \
                                    and browser_log["params"]["response"]["timing"]['sendStart']:
                                send_end = browser_log["params"]["response"]["timing"]['sendEnd']
                                send_start = browser_log["params"]["response"]["timing"]['sendStart']
                                log.info(
                                    "Diff of server send_end and server send_start {}".format(send_end - send_start) + "ms")
                            if (browser_log["params"]["response"]["timing"]['connectStart']
                                and browser_log["params"]["response"]["timing"]['connectEnd']) != -1:
                                connect_start_time = browser_log["params"]["response"]["timing"]['connectStart']
                                connect_end_time = browser_log["params"]["response"]["timing"]['connectEnd']
                                # log.info("connect start time {}".format(connect_start_time))
                                # log.info("connect end time {}".format(connect_end_time))
                                log.info("Diff of connect_end and connect_start {}"
                                         .format(connect_end_time - connect_start_time) + " ms")
                        except:
                            pass
                    else:
                        log.info("timing is not found in the browser logs")

