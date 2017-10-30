from android.screens.base import Base

class Home(Base):
    user_image_view = ('id', 'com.kms.kaltura.kmsapplication:id/user_image_view')
    
    # Click (tap) methods   
    def click_user_image_view(self):
        self.click(self.user_image_view)
        
        
