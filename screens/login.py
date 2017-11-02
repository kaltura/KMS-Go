import sys

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

from android.screens.login_android import LoginAndroid
from ios.screens.login_ios import LoginIos
from lib import logger
from screens.base import Base
from screens.general import General
from screens.home import Home


class Login(Base):
    # Parameters
    platform = None
    driver = None
    
    # Module
    login = None
    
    def __init__(self, platform, driver):
        self.platform = platform
        self.driver   = driver
        
        if platform == 'android':
            self.login    = LoginAndroid(driver)
        elif platform == 'ios':
            self.login = LoginIos(driver)
        else:
            platform = None
            #TODO PRINT ERROR
        
        # For internal use (Reusable flow methods in this class)
        self.home     = Home(platform, driver) 
        self.general  = General(platform, driver)
    #############################################################################
    ############################# Click (tap) methods ###########################    
    # Click 'LOGIN'  
    def click_login_button(self):
        if self.click(self.login.login_button) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on login button')
            return True
        else:
            logger.infoLog('WARNING: Failed to click on login button')
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on login button')
        
    # Click 'Sign in'    
    def click_signin_button(self):
        if self.click(self.login.signin_button) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on signin button')
            return True
        else:
            logger.infoLog('WARNING: Failed to click on signin button')
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on signin button')
        
    def click_coordinates_login_frame(self, x, y):
        if self.click_with_offset(self.login.login_frame, x, y) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked with coordinates on login frame')
            return True
        else:
            logger.infoLog('WARNING: Failed to click on login frame: x,y:' + str(x) + ',' + str(y))
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Failed to click with coordinates on login frame: x,y:' + str(x) + ',' + str(y))
        
    #############################################################################
    ############################# Wait for methods ##############################          
    def wait_for_logged_in_background(self, timeout):
        if self.wait_visible(self.login.logged_in_background, timeout) != None:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Wait for logged_in_background')
            return True
        else:
            logger.infoLog('WARNING: Element logged_in_background doesn\'t appear after ' + str(timeout))
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Element logged_in_background doesn\'t appear after ' + str(timeout))
    
    #############################################################################
    ############################# Type text methods #############################
    def type_login_username(self, text):
        if self.send_keys(self.login.text_login_username, text)  == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Type in login username filed: "' + text + '"')
            return True
        else:
            logger.infoLog('WARNING: Failed to type in login username filed: "' + text + '"')
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Failed to type in login username filed: "' + text + '"')
        
    def type_login_password(self, text):
        if self.send_keys(self.login.text_login_password, text)  == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Type in login password filed: "' + text + '"')
            return True
        else:
            logger.infoLog('WARNING: Failed to type in login password filed: "' + text + '"')
            raise Exception('Function: "' + sys._getframe().f_code.co_name + '" - Failed to type in login password filed: "' + text + '"')
        
    #############################################################################
    ############################# Reusable flow methods #########################    
    def login_with_credentials(self, username, password):
        try: 
            self.home.click_user_image_view()
            self.click_login_button()
            self.type_login_username(username)
            self.type_login_password(password)
            self.general.hide_keyboard()
            self.click_signin_button()
            self.wait_for_logged_in_background(15)
            logger.infoLog("Logged in successfully with '" + "'" + username + "'@'" + password + "'")
        except Exception:
            logger.infoLog("FAILED to login with '" + "'" + username + "'@'" + password + "'")
            raise
        