from appium import webdriver

from android.screens.base import Base



class Login(Base):
    login_button = ('id', 'com.kms.kaltura.kmsapplication:id/login_button')
    text_login_username = ('id', 'Login-username')
    text_login_password = ('id', 'Login-password')
    signin_button = ('id', 'Login-login')
    login_frame = ('id', 'loginBox') #holds the login username, password, signin buttons
    
    
    #############################################################################
    ############################# Click (tap) methods #############################    
    # Click 'LOGIN'  
    def click_login_button(self):
        self.click(self.login_button)
    
    # Click 'Sign in'    
    def click_signin_button(self):
        self.click(self.signin_button)
        
    def click_coordinates_login_frame(self, x, y):
        self.click_with_offset(self.login_frame, x, y)     
    
    #############################################################################
    ############################# Type text methods #############################
    
    def type_login_username(self, text):
        self.send_keys(self.text_login_username, text)  
        
    def type_login_password(self, text):
        self.send_keys(self.text_login_password, text)          
