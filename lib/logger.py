import datetime
import logging, sys, time, os

from lib.test_service import TestService


formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
testGogFilePath = ''
globalLogFilePath = ''
#TODO hardcoded
def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# loggerTest = setup_logger('test_log', testGogFilePath + '\log.log')
# loggerGlobal = setup_logger('global_log', testGogFilePath + '\log.log')

# logging.basicConfig(filename='C:\work\Mobile\KmsGo\workspace\KMS-Go\log\log.txt', 
#                     format='%(levelname)s %(asctime)s %(message)s', 
#                     datefmt='%m/%d/%Y %I:%M:%S %p: ', 
#                     filemode='w', 
#                     level=logging.INFO)
# testLog = logging.getLogger(__name__)

# Write log to each folder test    
def infoLog(content):
    infoTestLog(content)
    infoGlobalLog(content)
    
def warningLog(content):
    infoTestLog(content)
    infoGlobalLog(content)
    
def errorLog(content):
    infoTestLog(content)
    infoGlobalLog(content)
    
def debugLog(content):
    infoTestLog(content)
    infoGlobalLog(content)            
    
def infoTestLog(content):
    loggerTest = setup_logger('test_log', TestService.TEST_LOG_FILE_PATH)
    loggerTest.info(content)
    # Remove handler, if not remove, it will print multiple lines
    while loggerTest.handlers:
        loggerTest.handlers.pop()

def warningTestLog(content):
    loggerTest = setup_logger('test_log', TestService.TEST_LOG_FILE_PATH)
    loggerTest.info('WARNING: ' + content)
    while loggerTest.handlers:
        loggerTest.handlers.pop()
     
def errorTestLog(content):
    loggerTest = setup_logger('test_log', TestService.TEST_LOG_FILE_PATH)
    loggerTest.info('ERROR: ' + content)
    while loggerTest.handlers:
        loggerTest.handlers.pop()
     
def debugTestLog(content):
    loggerTest = setup_logger('test_log', TestService.TEST_LOG_FILE_PATH)
    loggerTest.info('DEBUG: ' + content)
    while loggerTest.handlers:
        loggerTest.handlers.pop()

# Write log to global, all test combined log    
def infoGlobalLog(content):
    loggerGlobal = setup_logger('global_log', TestService.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info(content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()

def warningGlobalLog(content):
    loggerGlobal = setup_logger('global_log', TestService.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info('WARNING: ' + content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()
     
def errorGlobalLog(content):
    loggerGlobal = setup_logger('global_log', TestService.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info('ERROR: ' + content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()
     
def debugGlobalLog(content):
    loggerGlobal = setup_logger('global_log', TestService.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info('DEBUG: ' + content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()   
    
# The function writes to the log that we started the test
def logStartTest(test,platform):
    os.environ["RUNNING_TEST_ID"] = test.testNum
    infoLog("INFO","************************************************************************************************************************")
    infoLog("INFO","test_" + test.testNum + " Start on platform " + platform + ".")
    
# The function writes in the log that we finished the test. we write if the test failed or succeeded and how much time it took 
def logFinishedTest(test, startTime):
        test.duration = str(round(time.time() - startTime))
        infoLog("INFO","test_" + test.testNum + ": " + test.status + " (" + test.duration + " sec)")
#         writeStatsToCSV(test)
        
# The function writes to log the excption 
def log_exception(inst):
    
    exc_type, exc_value, exc_traceback = sys.exc_info() 
    traceback_details = {
                             'filename': exc_traceback.tb_frame.f_code.co_filename,
                             'lineno'  : exc_traceback.tb_lineno,
                             'name'    : exc_traceback.tb_frame.f_code.co_name,
                             'type'    : exc_type.__name__
                            }
    
    
    infoLog("Exception at file     : " + traceback_details["filename"])
    infoLog("Exception at line     : " + str(traceback_details["lineno"]))
    infoLog("Exception at function : " + traceback_details["name"])
    infoLog("Exception type        : " + traceback_details["type"])
    infoLog("Value                 : " + str(exc_value))
    
# Initialize log - Create global log file in not exists, and creates log in current test folder
def initializeLog(testNum, platformName, platformVersion, deviceModel, deviceScreenSize):
    TestService.CURRENT_PLATFORM = 'android'
    # Get Test folder path
    TestService.TEST_LOG_FILE_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..',TestService.CURRENT_PLATFORM, testNum))
    # Get Test log path
    TestService.TEST_LOG_FILE_PATH = os.path.abspath(os.path.join(TestService.TEST_LOG_FILE_FOLDER_PATH, testNum + '.log'))
    # Get Global log path
    TestService.GLOBAL_LOG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..',TestService.CURRENT_PLATFORM, TestService.CURRENT_PLATFORM + '.log'))
    # Create test log folder if not exists
    if (os.path.isdir(TestService.TEST_LOG_FILE_FOLDER_PATH) == False):
        os.makedirs(TestService.TEST_LOG_FILE_FOLDER_PATH, exist_ok=True)             
   
    infoTestLog('************************************************************************************************************************')
    infoTestLog('Test Setup Ready: Test ' + testNum + ' started on ' + platformName + ', Version ' + platformVersion + ', Model ' + deviceModel + ', Resolution ' +deviceScreenSize)   