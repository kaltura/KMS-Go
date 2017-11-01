from datetime import datetime
import time, os, sys

import pytest
import conftest
from lib import logger
from lib.test_service import TestService
from screens.general import General
from screens.home import Home
from screens.login import Login


class Test:
    # Test parameters:
    platform = None
    driver = None
    testNum     = "0001"
    status      = "Pass"
    
    # Test services
    testService = TestService()
    
    # Get supported platforms for this test - Android, IOS
    supported_platforms = testService.updatePlatforms(testNum)
    
    # Test Setup
    @pytest.fixture(scope='module',params=supported_platforms)
    def setup(self, request):
        global driver
        # Get platform from the platform list (testSet.csv)
        TestService.CURRENT_PLATFORM = request.param
        # Return WebDriver (android/ios)
        driver = self.testService.setup(TestService.CURRENT_PLATFORM)
        # Create log
        logger.initializeLog(self.testNum,
                            driver.capabilities['platformName'],
                            driver.capabilities['platformVersion'],
                            driver.capabilities['deviceModel'],
                            driver.capabilities['deviceScreenSize'])

    # Test Flow        
    def test_0001(self, setup):
        try:
            # Capture test start time
            self.testService.logTestStartTime()
            # Tested Screens
            login = Login(TestService.CURRENT_PLATFORM , driver)
            
            # Steps:
            logger.infoLog('STEP1: Goint to login')
            login.login_with_credentials('admin', '123456')
        # If an exception happened we need to handle it and fail the test       
        except Exception as inst:
            self.status = self.testService.handleException(self, inst, self.testService.CURRENT_TEST_START_TIME)        
    
    #Test TearDown
    def teardown_method(self, method):
        logger.infoLog('Test Flow Ended, Going to teardown')
        # Take last screenshot before quitting
        driver.save_screenshot(conftest.LSAT_SCREENSHOT_PATH)    
        driver.quit()
        #write to log we finished the test
        self.testService.logTestEndTime()

        if self.status == "Pass":
            logger.infoLog('TEST PASSED')
        else:
            logger.infoLog('TEST FAILED')
            assert(False)
        
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')