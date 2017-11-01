import sys
from android.screens.home_android import HomeAndroid
from ios.screens.home_ios import HomeIos
from lib import logger
from screens.base import Base


class Home(Base):
    # Parameters
    platform = None
    driver = None
    
    # Module
    home = None
    
    def __init__(self, platform, driver):
        self.platform = platform
        self.driver   = driver
        
        if platform == 'android':
            self.home     = HomeAndroid(driver)
        elif platform == 'ios':
            self.home     = HomeIos(driver)
        else:
            platform = None
            #TODO PRINT ERROR 
        
           
    #############################################################################
    ############################# Click (tap) methods ####################    
 
    
    #############################################################################
    ############################# Type text methods ######################       
    # Click (tap) methods   
    def click_user_image_view(self):
        if self.click(self.home.user_image_view) == True:
            logger.debugLog('Function: "' + sys._getframe().f_code.co_name + '" - Clicked on user image view button')
            return True
        else:
            logger.warningLog('Function: "' + sys._getframe().f_code.co_name + '" - Failed to click on user image view button')
            return False        
        
        
