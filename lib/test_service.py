from appium import webdriver
from datetime import datetime
import pytest, csv, sys, os, time

from lib import logger
import conftest

#===========================================================================
# The class contains basic test functions and macros. 
# Driver and logs initialization, timeout handlers. 
# Check supported platform to run on, update final results matrix.
#===========================================================================
class TestService:
    # General parameters
    CURRENT_PLATFORM                = None
    # Logging parameters
#     LOG_LEVEL                       = "DEBUG" #TODO Enum
    LOG_LEVEL                       = "INFO" #TODO Enum
    GLOBAL_LOG_FILE_PATH            = None
    TEST_LOG_FILE_FOLDER_PATH       = None
    TEST_LOG_FILE_PATH              = None

    CURRENT_TEST_START_TIME         = None
    CURRENT_TEST_END_TIME           = None
    LAST_TEST_DURATION              = None
    
    # Appium parameters
    APPIUM_LOCAL_HOST_URL           = 'http://localhost:4723/wd/hub'
    
    # Android parameters
    PLATFORM_VERSION                = '6.0.1'
    
    # IOS parameters
    
    # PractiTest parameters
    PRACTITEST_PROJECT_ID                  = 1328
    PRACTITEST_AUTOMATED_SESSION_FILTER_ID = 259788
    PRACTITEST_API_TOKEN                   = "deee12e1d8746561e1815d0430814c82c9dbb57d"
    PRACTITEST_DEVELOPER_EMAIL             = "oleg.sigalov@kaltura.com"
    
    ## MTHODS
    def basicSetup(self, platform, testNum):
        try:
            # Initialize log, create log folder if needed
            logger.initializeLog(testNum)
            # Capture test start time
            self.logTestStartTime()
            # Return WebDriver (android/ios)
            driver = self.getDriver(platform)
            # Create log
            logger.readyForTestLog(testNum,
                                driver.capabilities['platformName'],
                                driver.capabilities['platformVersion'],
                                driver.capabilities['deviceModel'],
                                driver.capabilities['deviceScreenSize'])
            return driver
        except Exception:
            logger.infoLog('Test setup failed - Failed to get Driver')
            raise
    def basicTearDown(self, test, driver=None):
        logger.infoLog('Going to TearDown')
        if driver != None:
            # Take last screenshot before quitting
            driver.save_screenshot(conftest.LSAT_SCREENSHOT_PATH)    
            driver.quit()
            #write to log we finished the test
        self.logTestEndTime()

        if test.status == "Pass":
            logger.infoLog('TEST PASSED')
        else:
            logger.infoLog('TEST FAILED')
            assert(False)        
    
    #update the supported platforms for each test case by reading the supported browsers we pass to the fixture from platform_matrix.csv. 1 - support , 0 - not support.  
    def updatePlatforms(self,test_num):
        
        env = ""
        for arg in sys.argv[1:]:
            if "--env" in arg:
                env = arg[6:] 
            
        supported_platforms=[]
        case_str = "test_" + test_num
        matrixPath=os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','ini','testSet' + env +  '.csv'))
        with open(matrixPath, 'r') as csv_mat: #windows
            platform_matrix = csv.DictReader(csv_mat)
            for row in platform_matrix:
                if (row['case'] == case_str):
                    if (row['android']=='1'):
                        supported_platforms.append(pytest.mark.ff(['android', row['pt_id']]))
                    if (row['ios']=='1'):
                        supported_platforms.append(pytest.mark.ch('ios'))    
    
        return supported_platforms
    
    
    #TODO
    def getDriver(self, platform):
        if platform == 'android':
            return self.driver_setup_android()
        elif platform == 'ios':
            return self.driver_setup_ios()
        else:
            #TODO print
            return None
        
    def driver_setup_android(self):
        capabilities = {
            'appPackage': 'com.kms.kaltura.kmsapplication',
            'appActivity': '.activities.LoadingActivity',
            'platformName': 'android',
            'platformVersion': self.PLATFORM_VERSION,
            'deviceName': 'Galaxy S6',
            'noReset': 'true'
    #         'app': PATH('C:\\work\\Mobile\\KmsGo\\APK\\app.apk')
        }
        return webdriver.Remote(self.APPIUM_LOCAL_HOST_URL, capabilities)
    
    #TODO
    def driver_setup_ios(self):
        return None
    
    # The function handles exception inst, mark the test as fail and writes the error in the log 
    def handleException(self, test, exp):
        logger.log_exception(exp)
        test.status = "Fail"
        return test.status    
    
    # Get the test start time and print to log
    def logTestStartTime(self):
        self.CURRENT_TEST_START_TIME = time.time()
        logger.infoLog('************************************************************************************************************************')
        logger.infoLog("Test Started At: " + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(self.CURRENT_TEST_START_TIME)))
            
    
    # Get the test end time and print to log        
    def logTestEndTime(self):
        self.CURRENT_TEST_END_TIME = time.time()
        logger.infoLog("Test Ended At: " + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(self.CURRENT_TEST_END_TIME)))
        timeDiff = self.CURRENT_TEST_END_TIME - self.CURRENT_TEST_START_TIME 
        timeDiff = datetime.utcfromtimestamp(timeDiff).strftime('%H:%M:%S.%f')[:-3]
        logger.infoLog("Total Test Run: " + timeDiff)         
        
        
        
        
             