import pytest
from lib import logger
from lib.test_service import TestService
from screens.login import Login
from lib.practitest import PractiTest


class Test:
    # Test parameters:
    platform = None
    driver = None
    testNum     = "0000_practitest"
    status      = "Fail"
    
    # Test services
    testService = TestService()
    practiTest = PractiTest()
    # Test Setup
    def setup(self):
        # Get platform from the platform list (testSet.csv)
        logger.initializeLog()

    # Test Flow        
    def test_0001(self):
        try:
            prSessionInfo = self.practiTest.getPractiTestAutomationSession()
            if (prSessionInfo["sessionSystemID"] != -1):
                testIDsDct = self.practiTest.getPractiTestSessionInstances(prSessionInfo["sessionSystemID"])
                if (len (testIDsDct) > 0):
                    self.practiTest.createAutomationTestSetFile(prSessionInfo["setPlatform"],testIDsDct,prSessionInfo["sessionDisplayID"])
                    if (self.practiTest.setTestSetAutomationStatusAsProcessed(prSessionInfo["sessionDisplayID"]) != True):
                        self.status = "Fail"
                        logger.infoGlobalLog("INFO","Unable to set test set as processed") 
                else:
                    self.status = "Fail"
                    logger.infoGlobalLog("INFO","Unable to get test list")            
            print('1')
            print('2')
#             self.status = "Pass"
            assert(self.status == "Pass")    
        # If an exception happened we need to handle it and fail the test       
        except Exception as exp:
            self.status = self.testService.handleException(self, exp)        
    
    #Test TearDown
    def teardown(self):
        if self.status == "Pass":
            logger.infoGlobalLog('PRACTITEST TEST PASSED')
        else:
            logger.infoGlobalLog('PRACTITEST TEST FAILED')
            assert(False) 
        
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')