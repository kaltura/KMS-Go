import sys

from android.screens.home_android import HomeAndroid
from android.screens.pre_login_android import PreLoginAndroid
from ios.screens.home_ios import HomeIos
from ios.screens.pre_login_ios import PreLoginIos
from lib import logger, localConfig
from screens.base import Base
from screens.general import General
from screens.home import Home
from screens.login import Login


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
            logger.raiseException(driver, 'Unknown platform: "' + platform + '"')
        
        # For internal use (Reusable flow methods in this class)
        self.login     = Login(platform, driver)
        self.home      = Home(platform, driver) 
        self.general   = General(platform, driver) 
        
               
    #############################################################################
    ############################# Click (tap) methods ###########################
    # Click on the text field of the 'enter url of your site'        
    def click_enter_url_of_your_site(self):
        if self.click(self.preLogin.enter_url_of_your_site) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on enter_url_of_your_site button')
            return True
        else:
            logger.raiseException(self.driver, logger.generateErrorMsg('FAILED to click on enter_url_of_your_site button'))

    # Type instance to 'enter url of your site'         
    def type_url_edit_text(self, text):
        if self.send_keys(self.preLogin.url_edit_text, text)  == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Type in login url_edit filed: "' + text + '"')
            return True
        else:
            logger.raiseException(self.driver, logger.generateErrorMsg('FAILED to type in login url_edit filed: "' + text + '"'))
                           
                                  
    #############################################################################
    ############################# Reusable flow methods #########################
    # Verify Site URL is entered, if not then enter the Site URL
    def loginGeneric(self, username, password):
        try:
            # If user_image_view icon exists, then we are in
            if self.wait_visible(self.home.home.user_image_view, 15):
                return True
            
            # Case if after application loaded and the login screen is displayed
            if self.wait_visible(self.login.login.text_login_username, 15):
                self.login.enter_credentials_and_sing_in(username, password)
                return True
            
            # Case need to enter URL
            if self.wait_visible(self.preLogin.enter_url_of_your_site, 15):
                # Click on 'Enter URL of your site'
                self.click_enter_url_of_your_site()
                
                # Enter the Site URL (from localConfig.py)
                self.type_url_edit_text(localConfig.SITE_URL + '\n') #'\n' represents a click on 'enter'
                self.login.enter_credentials_and_sing_in(username, password)
        except Exception:
            logger.raiseException(self.driver, "FAILED to Login Generic with '" + username + "' @ '" + password + "'")