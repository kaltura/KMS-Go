from android.screens.base import Base

class PreLogin(Base):
    enter_url_of_your_site = ('id', 'com.kms.kaltura.kmsapplication:id/enter_url_text')
    url_edit_text = ('id', 'com.kms.kaltura.kmsapplication:id/url_edit_text')
    
    def click_enter_url_of_your_site(self):
        self.click(self.enter_url_of_your_site)
        
    def type_url_edit_text(self):
        self.send_keys(self.url_edit_text, '1722461-2.qakmstest.dev.kaltura.com\n')
