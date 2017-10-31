from screens.base import Base
from ios.screens.pre_login_ios import PreLoginIos
from android.screens.pre_login_android import PreLoginAndroid

class PreLogin(Base):
    # Parameters
    platform = None
    driver = None
    
    # Module
    preLogin = None
    
    def __init__(self, platform, driver):
        self.platform = platform
        self.driver   = driver
        
        if platform == 'android':
            self.preLogin = PreLoginAndroid(driver)
        elif platform == 'ios':
            self.preLogin = PreLoginIos(driver)
        else:
            platform = None
            #TODO PRINT ERROR 
        
        
    #############################################################################
    ############################# Click (tap) methods ###########################              
    def click_enter_url_of_your_site(self):
        self.click(self.preLogin.enter_url_of_your_site)
        
    def type_url_edit_text(self):
        self.send_keys(self.preLogin.url_edit_text, '1722461-2.qakmstest.dev.kaltura.com\n')
