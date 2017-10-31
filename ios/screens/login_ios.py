from appium import webdriver
from ios.screens.base_ios import BaseIos



class LoginIos(BaseIos):
    login_button = ('id', 'com.kms.kaltura.kmsapplication:id/login_button')
    text_login_username = ('id', 'Login-username')
    text_login_password = ('id', 'Login-password')
    signin_button = ('id', 'Login-login')
    login_frame = ('id', 'loginBox') #holds the login username, password, signin buttons
    
    
    #############################################################################
    ############################# Custom Click (tap) methods ####################  
    
    #############################################################################
    ############################# Custom Type text methods ######################
