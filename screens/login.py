import sys
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException
from android.screens.login_android import LoginAndroid
from ios.screens.login_ios import LoginIos
from lib import logger
from screens.base import Base


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
        
        
    #############################################################################
    ############################# Click (tap) methods ###########################    
    # Click 'LOGIN'  
    def click_login_button(self):
        if self.click(self.login.login_button) == True:
            logger.debug('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on login button')
            return True
        else:
            logger.info('WARNING: Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on login button')
            raise Exception('Failed to click on login button')
        
    # Click 'Sign in'    
    def click_signin_button(self):
        if self.click(self.login.signin_button) == True:
            logger.debug('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on signin button')
            return True
        else:
            logger.info('WARNING: Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on signin button')
            return False        
        
    def click_coordinates_login_frame(self, x, y):
        if self.click_with_offset(self.login.login_frame, x, y) == True:
            logger.debug('Function: "' + sys._getframe().f_code.co_name + '" - Clicked with coordinates on login frame')
            return True
        else:
            logger.info('WARNING: Function: "' + sys._getframe().f_code.co_name + '" - Failed to click with coordinates on login frame: x,y:' + str(x) + ',' + str(y))
            return False         
    
    #############################################################################
    ############################# Type text methods #############################
    def type_login_username(self, text):
        if self.send_keys(self.login.text_login_username, text)  == True:
            logger.debug('Function: "' + sys._getframe().f_code.co_name + '" - Type in login username filed: "' + text + '"')
            return True
        else:
            logger.info('WARNING: Function: "' + sys._getframe().f_code.co_name + '" - Failed to type in login username filed: "' + text + '"')
            return False          
        
    def type_login_password(self, text):
        if self.send_keys(self.login.text_login_password, text)  == True:
            logger.debug('Function: "' + sys._getframe().f_code.co_name + '" - Type in login password filed: "' + text + '"')
            return True
        else:
            logger.info('WARNING: Function: "' + sys._getframe().f_code.co_name + '" - Failed to type in login password filed: "' + text + '"')
            return False