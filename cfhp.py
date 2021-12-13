import os
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

#Wanna hear a joke? (Look all the way down...)
links = []
result_to_save = []


def notJsonQuestionMark(loadedDict):
    print("Executing parser")
    x = eval(str(loadedDict))
    for xo in x:
        if json.loads(xo.get('message'))["message"]["method"] == "Page.downloadWillBegin":
            if "url" in json.loads(xo.get('message'))["message"]["params"]:
                if "https://media.forgecdn.net/" in json.loads(xo.get('message'))["message"]["params"]["url"]:
                    return json.loads(xo.get('message'))["message"]["params"]["url"]
                    # Everything in this function does not make any sense. Don't ask. It just works.

def get_perf_log_on_load(url, headless=False, filter=None): #Headless does not work
    print("Executing driver on " + url)
    options = Options()
    #options.add_experimental_option('w3c', False)
    if headless:
        options.headless = headless
    options.add_argument('log-level=3')
    cap = DesiredCapabilities.CHROME
    cap["goog:loggingPrefs"] = {"performance": "ALL"}
    driver = webdriver.Chrome(r".\chromedriver.exe", desired_capabilities=cap, options=options)
    driver.get(url)
    log = driver.get_log("performance")
    if "https://media.forgecdn.net/files/" not in str(log):
        while "https://media.forgecdn.net/files/" not in str(log):
            log = driver.get_log("performance")
            time.sleep(1)
    driver.close()
    return log

def main():
    with open(r"./linkList.txt", 'r') as mainFile:
        mainContent = mainFile.read()
        mainContent_split = mainContent.split("\n")
        for splitText in mainContent_split:
            if len(str(splitText)) > 0:
                links.append(splitText.rstrip())
    os.makedirs("./data/", exist_ok=True)
    for link in links:
        print("Starting the gather from: " + link)
        ln = str(notJsonQuestionMark(get_perf_log_on_load(link)))
        if len(ln) > 0:
            print("Url found: " + ln)
            result_to_save.append(ln + "\n")
    date = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    print(f"Saving data to filename_{date}.data")
    with open(f"./data/filename_{date}.data", "w") as f:
        f.write(''.join(result_to_save))
    print(f"Data saved to filename_{date}.data")


main()


# The joke is... Python.
