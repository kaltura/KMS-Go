import sys

from screens.base import Base


class General(Base):
    # Parameters
    platform = None
    driver = None
     
#     # Module
#     general = None
     
    def __init__(self, platform, driver):
        self.platform = platform
        self.driver   = driver
#         
#         if platform == 'android':
#             self.home     = HomeAndroid(driver)
#         elif platform == 'ios':
#             self.home     = HomeIos(driver)
#         else:
#             platform = None
#             #TODO PRINT ERROR 
        
           
    #############################################################################
    ############################# Click (tap) methods ####################    
 
    
    #############################################################################
    ############################# Type text methods ######################       
    # Click (tap) methods   
    def general_hide_keyboard(self):
        self.hide_keyboard()    
        
        
