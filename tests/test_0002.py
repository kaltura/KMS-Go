import pytest
from lib import logger
from lib.test_service import TestService
from screens.login import Login


class Test:
    # Test parameters:
    platform = None
    driver = None
    practitTestId = None
    testNum     = "0002"
    status      = "Fail"
    
    # Test services
    testService = TestService()
    
    # Get supported platforms for this test - Android, IOS
    supported_platforms = testService.updatePlatforms(testNum)
    
    # Test Setup
    @pytest.fixture(scope='module',params=supported_platforms)
    def setup(self, request):
        global driver, practitTestId
        # Get platform from the platform list (testSet.csv)
        TestService.CURRENT_PLATFORM = request.param[0]
        self.practitTestId = request.param[1]
        driver = self.testService.basicSetup(TestService.CURRENT_PLATFORM, self.testNum)

    # Test Flow        
    def test_0001(self, setup):
        try:
            # Tested Screens
            login = Login(TestService.CURRENT_PLATFORM , driver)
            
            # Steps:
            logger.infoLog('STEP1: Goint to login')
            login.login_with_credentials('admin', '123456')
            print('3')
            print('4')
            self.status = "Pass"
        # If an exception happened we need to handle it and fail the test       
        except Exception as exp:
            self.status = self.testService.handleException(self, exp)        
    
    #Test TearDown
    def teardown_method(self, method):
        self.testService.basicTearDown(self, driver)
        
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')