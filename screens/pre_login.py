import sys
from android.screens.pre_login_android import PreLoginAndroid
from ios.screens.pre_login_ios import PreLoginIos
from lib import logger
from screens.base import Base


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
        if self.click(self.preLogin.enter_url_of_your_site) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on enter_url_of_your_site button')
            return True
        else:
            logger.warningLog('Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on enter_url_of_your_site button')
            return False      
        
    def type_url_edit_text(self, text):
        if self.send_keys(self.preLogin.url_edit_text, text)  == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Type in login url_edit filed: "' + text + '"')
            return True
        else:
            logger.warningLog('Function: "' + sys._getframe().f_code.co_name + '" - Failed to type in login url_edit filed: "' + text + '"')
            return False         
