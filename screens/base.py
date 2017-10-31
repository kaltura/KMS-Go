from screens.screen import Screen
# import logging

# logging.basicConfig(filename='C:\work\Mobile\KmsGo\workspace\KmsGo\log\log.txt', filemode='w', level=logging.DEBUG)
# mylogger = logging.getLogger()
#     
class Base(Screen):
#     def log(self,content):
#         mylogger.info(content)
    # Alerts
    alert = ('class_name', 'UIAAlert')
    alert_title = ('id', 'Cool title')
    alert_text = ('id', 'this alert is so cool.')
    alert_cancel_button = ('id', 'Cancel')
    alert_ok_button = ('id', 'OK')