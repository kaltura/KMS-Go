from android.screens.base_android import BaseAndroid


class LoginAndroid(BaseAndroid):
    login_button            = ('id', 'com.kms.kaltura.kmsapplication:id/login_button')
    text_login_username     = ('id', 'Login-username')
    text_login_password     = ('id', 'Login-password')
    signin_button           = ('id', 'Login-login')
    login_frame             = ('id', 'loginBox') #holds the login username, password, signin buttons
    logged_in_background    = ('id', 'com.kms.kaltura.kmsapplication:id/logged_in_background')
    
    #############################################################################
    ############################# Custom Click (tap) methods ####################    
 
    
    #############################################################################
    ############################# Custom Type text methods ######################
    
      
