import csv
import json
import os

import requests
from lib import logger


# PractiTest parameters
PRACTITEST_PROJECT_ID                  = 1328
PRACTITEST_AUTOMATED_SESSION_FILTER_ID = 259788
PRACTITEST_API_TOKEN                   = "deee12e1d8746561e1815d0430814c82c9dbb57d"
PRACTITEST_DEVELOPER_EMAIL             = "oleg.sigalov@kaltura.com"

# The class contains functions that manage PractiTest integration with automation framework 
class PractiTest:
    TEST_LOG_FILE_FOLDER_PATH = None
    
    def updateTestLogFileFolder(self, value):
        self.TEST_LOG_FILE_FOLDER_PATH = value
        
        
    # Function that returns all instances of a specific session 
    def getPractiTestSessionInstances(self, prSessionID):
        
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(PRACTITEST_PROJECT_ID) + "/instances.json?set-ids=" + str(prSessionID) + "&developer_email=" + PRACTITEST_DEVELOPER_EMAIL + "&api_token=" + PRACTITEST_API_TOKEN
        sessionInstancesDct = {}
        headers = { 
            'Content-Type': 'application/json'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (len(dctSets["data"]) > 0):
                for testInstance in dctSets["data"]:
                    try:
#                         sessionInstancesDct[testInstance["attributes"]["test-display-id"]] = testInstance["attributes"]["display-id"] #testInstance["attributes"]["custom-fields"]['---f-30336']
                        sessionInstancesDct[testInstance["attributes"]["custom-fields"]['---f-30336']] = testInstance["attributes"]["display-id"]
                        logger.infoGlobalLog("Found test with id: " + str(testInstance["attributes"]["test-display-id"]))
                    except Exception:
                        pass                        
            else:
                logger.infoGlobalLog("No instances in set. " + r.text)        
        else:
            logger.infoGlobalLog("Bad response for get sessions. " + r.text) 
        
        return sessionInstancesDct
        
    # Function that returns all sessions that are located under the filter "pending for automation"  
    def getPractiTestAutomationSession(self):
        practiTestGetSessionsURL = "https://api.practitest.com/api/v1/sets.json?project_id=" + str(PRACTITEST_PROJECT_ID) + "&filter_id=" + str(PRACTITEST_AUTOMATED_SESSION_FILTER_ID)
        
        prSessionInfo = {
            "sessionSystemID"  : -1,
            "sessionDisplayID" : -1,
            "setPlatform"      : ""
        }

        headers = {
            'Authorization': 'custom api_token=' + PRACTITEST_API_TOKEN,
            'Content-Type': 'application/json',
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (dctSets["additional_data"]["pagination"]["total_entities"] > 0):
                prSessionInfo["sessionSystemID"]  = dctSets["data"][0]["system_id"]
                prSessionInfo["sessionDisplayID"] = dctSets["data"][0]["display_id"]
                prSessionInfo["setPlatform"]      = dctSets["data"][0]["___f_10353"]["value"].lower() #Operation System
                logger.infoGlobalLog("Automation set found: " + str(prSessionInfo["sessionDisplayID"]) + " on platform: " + prSessionInfo["setPlatform"])
            else:
                logger.infoGlobalLog("No automated sessions found.")
        else:
            logger.infoGlobalLog("Bad response for get sessions. " + r.text) 
        
        return prSessionInfo
    
    # Function that that creates the csv that contains the automation tests to be run
    def createAutomationTestSetFile(self, platform, testIDsDict, testSetID):
        
        platformList = ["android","ios"]
        testSetFile  = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testSetAuto.csv'))
        
        automationTestSetFileHeader = "case"
        for plat in platformList:
            automationTestSetFileHeader = automationTestSetFileHeader + "," + plat
        automationTestSetFileHeader = automationTestSetFileHeader + ",instanceID\n"
        file = open(testSetFile, "w")
        file.write (automationTestSetFileHeader)
        for testID in testIDsDict:
            sTestID = str(testID)
            testPlatformLine = "test_" + sTestID.rjust(4,"0")
            for plat in platformList:
                if plat == platform:
                    testPlatformLine = testPlatformLine + ",1"
                    logger.infoGlobalLog("Adding: " + "test_" + sTestID.rjust(4,"0") + " for platform: " + plat)
                else:           
                    testPlatformLine = testPlatformLine + ",0"
            testPlatformLine = testPlatformLine + "," + testIDsDict[testID]
            file.write (testPlatformLine + "\n")
        file.close()
        
    # Function that that set the test set from status pending to status processed in PractiTest
    def setTestSetAutomationStatusAsProcessed(self, prSessionID):
        
        practiTestSetAutomationStatusAsProcessedUrl = "https://api.practitest.com/api/v1/sets/" + str(prSessionID) + ".json?project_id=" + str(PRACTITEST_PROJECT_ID)
        
        headers = { 
            'Authorization': 'custom api_token=' + PRACTITEST_API_TOKEN,
            'Content-Type': 'application/json',
        }
        
        data = {"___f_30327":{"value":"Processed"}} #PractiTest Filed: "AutomationStatus"
        
        r = requests.put(practiTestSetAutomationStatusAsProcessedUrl,headers = headers, data = json.dumps(data))
        if (r.status_code == 200):
            logger.infoGlobalLog("Session: " + str(prSessionID) + " updated as processed")
            return True
        else:
            logger.infoGlobalLog("Bad response for get sessions. " + r.text)
            return False
        
    # Function that update the test results of a specific test run in PractiTest
    def setPractitestInstanceTestResults(self, testStatus, testID):
        practiTestUpdateTestInstanceResultsURL = "https://api.practitest.com/api/v1/automated_tests/upload_test_result.json"
        
        if (testStatus == "Pass"):
            exit_code = "0"
        else:
            exit_code = "1"
         
        # Extract test set id from instance id in the test set file    
        testSet = self.getTestSetIDFromTestSetFile(testID)
        
        # Extract test id from instance id in the test set file    
        testInstance = self.getTestInstanceId(testID)        
        
        data = [ 
                 ("api_token" , PRACTITEST_API_TOKEN),
                 ("project_id", str(PRACTITEST_PROJECT_ID)), 
                 ("exit_code",  exit_code), 
                 ("instance_display_id", testSet + ":" + testInstance)
        ]         
        fileList = self.getFilesInTestLogFolder(self.TEST_LOG_FILE_FOLDER_PATH)       
         
        r = requests.post(practiTestUpdateTestInstanceResultsURL,data = data ,files=fileList)
         
        if (r.status_code == 200):
            logger.debugLog("Updated test: " + testID + " as: " + testStatus) 
            return True
        else:
            logger.debugLog("Bad response for update instances. " + r.text)
            return False
        
    # Function that retrievs  the test set id of a specific test in the csv file that contains the test list
    def getTestSetIDFromTestSetFile(self, testID):
        testSet = ""
        
        case_str = "test_" + testID
        testSetFilePath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testSetAuto.csv'))
        with open(testSetFilePath, 'r') as csv_mat: #windows
                platform_matrix = csv.DictReader(csv_mat)
                for row in platform_matrix:
                    if (row['case'] == case_str):
                        testSet = row['instanceID'][0:row['instanceID'].index(":")]
                        break    
        return testSet
    
    # Function that retrievs the test instance id of a specific test in the csv file that contains the test list
    def getTestInstanceId(self, testID):
        testSet = ""
        
        case_str = "test_" + testID
        testSetFilePath = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testSetAuto.csv'))
        with open(testSetFilePath, 'r') as csv_mat: #windows
                platform_matrix = csv.DictReader(csv_mat)
                for row in platform_matrix:
                    if (row['case'] == case_str):
                        testSet = row['instanceID'].split(":")[1]
                        break    
        return testSet    
    
    # Function that gets all the file names in a given folder
    def getFilesInTestLogFolder(self, path):
        
        files = []
        i = 0
        fileList =  os.listdir(path)
        for file in fileList:
            fileParameters = ('result_files[file' + str(i) + ']', (file, open(path + "\\" +  file, 'rb')))
            files.append (fileParameters)
            i = i + 1
        return files               