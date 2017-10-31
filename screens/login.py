from appium import webdriver
from screens.base import Base
from android.screens.login_android import LoginAndroid
from ios.screens.login_ios import LoginIos


class Login(Base):
    # Parameters
    platform = None
    driver = None
    
    # Module
    login = None
    preLogin = None
    home = None
    
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
        self.click(self.login.login_button)
    
    # Click 'Sign in'    
    def click_signin_button(self):
        self.click(self.login.signin_button)
        
    def click_coordinates_login_frame(self, x, y):
        self.click_with_offset(self.login.login_frame, x, y)      
    
    #############################################################################
    ############################# Type text methods #############################
    def type_login_username(self, text):
        self.send_keys(self.login.text_login_username, text)  
        
    def type_login_password(self, text):
        self.send_keys(self.login.text_login_password, text)           
