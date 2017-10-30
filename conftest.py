import logging, pytest
import os
from appium import webdriver
  
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
  
logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

@pytest.fixture()
def log(request, content):
    mylogger.info(content)
    
    
    
# APPIUM_LOCAL_HOST_URL = 'http://localhost:4723/wd/hub'
# PLATFORM_VERSION = '6.0.1'
#  
#  
# @pytest.fixture()
# def android(request):
#     capabilities = {
#         'appPackage': 'com.kms.kaltura.kmsapplication',
#         'appActivity': '.activities.LoadingActivity',
#         'platformName': 'android',
#         'platformVersion': PLATFORM_VERSION,
#         'deviceName': 'Galaxy S6',
#         'noReset': 'true'
# #         'app': PATH('C:\\work\\Mobile\\KmsGo\\APK\\app.apk')
#     }
#     request.instance.driver = webdriver.Remote(APPIUM_LOCAL_HOST_URL, capabilities)
#   
#     def teardown():
#         request.instance.driver.quit()
#     request.addfinalizer(teardown)
#       
# @pytest.fixture() 
# def driver_setup_ios(request):
#     capabilities = {
#         'appPackage': 'com.kms.kaltura.kmsapplication',
#         'appActivity': '.activities.LoadingActivity',
#         'platformName': 'android',
#         'platformVersion': PLATFORM_VERSION,
#         'deviceName': 'Galaxy S6',
#         'noReset': 'true'
# #         'app': PATH('C:\\work\\Mobile\\KmsGo\\APK\\app.apk')
#     }
#     request.instance.driver = webdriver.Remote(APPIUM_LOCAL_HOST_URL, capabilities)
#   
#     def teardown():
#         request.instance.driver.quit()
#     request.addfinalizer(teardown)    