import time
import pytest

from android.screens.home import Home
from android.screens.login import Login
from lib.test_service import TestService
class Test:
    driver = None
    # Test parameters:
    testNum     = "0002"
    status      = "Pass"
    
    # Test services
    testService = TestService()
    
    # Get supported platforms for this test - Android, IOS
    supported_platforms = testService.updatePlatforms(testNum)
    @pytest.fixture(scope='module',params=supported_platforms)
    def platform(self,request):
        return request.param 
    
    def setup_method(self,platform):
#         global driver
        self.driver = self.testService.getPlatformDriver(platform)
    
    def test_0002(self):
#         global driver
        # Tested Screens
        home = Home(self.driver)
        login = Login(self.driver)
        
        # Steps:
        home.click_user_image_view()
        login.click_login_button()
        login.type_login_username('admin')
        login.type_login_password('123456')
        # click on the backgroud to hide the
        login.click_login_frame() 
        login.click_signin_button()
        time.sleep(30)
    
    def tearDown(self):
        self.driver.quit()    
    if __name__ == "__main__":  
        pytest.main('test_' + testNum  + '.py -s --tb=line')
