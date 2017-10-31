from screens.base import Base
from ios.screens.home_ios import HomeIos
from android.screens.home_android import HomeAndroid

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
        self.click(self.home.user_image_view)
        
        
