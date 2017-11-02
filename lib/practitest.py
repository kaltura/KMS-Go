import json
import os

import requests

from lib import logger
from lib.test_service import TestService


# The class contains functions that manage PractiTest integration with automation framework 
class PractiTest:
    # Function that returns all instances of a specific session 
    def getPractiTestSessionInstances(self, prSessionID):
        
        practiTestGetSessionsURL = "https://api.practitest.com/api/v2/projects/" + str(TestService.PRACTITEST_PROJECT_ID) + "/instances.json?set-ids=" + str(prSessionID) + "&developer_email=" + TestService.PRACTITEST_DEVELOPER_EMAIL + "&api_token=" + TestService.PRACTITEST_API_TOKEN
        sessionInstancesDct = {}
        headers = { 
            'Content-Type': 'application/json'
        }
        
        r = requests.get(practiTestGetSessionsURL,headers = headers)
        if (r.status_code == 200):
            dctSets = json.loads(r.text)
            if (len(dctSets["data"]) > 0):
                for testInstance in dctSets["data"]:
                    sessionInstancesDct[testInstance["attributes"]["test-display-id"]] = testInstance["attributes"]["display-id"]
                    logger.infoGlobalLog("Found test with id: " + str(testInstance["attributes"]["test-display-id"]))                          
            else:
                logger.infoGlobalLog("No instances in set. " + r.text)        
        else:
            logger.infoGlobalLog("Bad response for get sessions. " + r.text) 
        
        return sessionInstancesDct
        
    # Function that returns all sessions that are located under the filter "pending for automation"  
    def getPractiTestAutomationSession(self):
        practiTestGetSessionsURL = "https://api.practitest.com/api/v1/sets.json?project_id=" + str(TestService.PRACTITEST_PROJECT_ID) + "&filter_id=" + str(TestService.PRACTITEST_AUTOMATED_SESSION_FILTER_ID)
        
        prSessionInfo = {
            "sessionSystemID"  : -1,
            "sessionDisplayID" : -1,
            "setPlatform"      : ""
        }

        headers = {
            'Authorization': 'custom api_token=' + TestService.PRACTITEST_API_TOKEN,
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
        
    # Function that that set the test set from status pending to status processed in practitest
    def setTestSetAutomationStatusAsProcessed(self, prSessionID):
        
        practiTestSetAutomationStatusAsProcessedUrl = "https://api.practitest.com/api/v1/sets/" + str(prSessionID) + ".json?project_id=" + str(TestService.PRACTITEST_PROJECT_ID)
        
        headers = { 
            'Authorization': 'custom api_token=' + TestService.PRACTITEST_API_TOKEN,
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