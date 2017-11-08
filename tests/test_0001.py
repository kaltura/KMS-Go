import pytest

from lib import logger, localConfig
from lib.test_service import TestService
from screens.pre_login import PreLogin


class Test:
    # Test parameters:
    platform = None
    driver = None
    practitTestId = None
    testNum     = "0001"
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
        localConfig.CURRENT_PLATFORM = request.param[0]
        self.practitTestId = request.param[1]
        driver = self.testService.basicSetup(localConfig.CURRENT_PLATFORM, self.testNum)

    # Test Flow        
    def test_0001(self, setup):
        try:
            # Tested Screens
            preLogin = PreLogin(localConfig.CURRENT_PLATFORM , driver)
            
            # Steps:
            logger.infoLog('STEP1: Goint to login')
            preLogin.loginGeneric('admin', '123456')
            self.status = "Pass"
        # If an exception happened we need to handle it and fail the test       
        except Exception as exp:
            self.status = self.testService.handleException(self, exp)        
    
    #Test TearDown
    def teardown_method(self, method):
        self.testService.basicTearDown(self, driver)
        
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')