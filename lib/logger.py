import inspect, logging, sys, time, os

from lib import localConfig


# TODO 
# Log Level Enum
# class LogLevel(enum.Enum):
INFO = "INFO"
DEBUG = "DEBUG"
ERROR = "ERROR"
    
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
testGogFilePath = ''
globalLogFilePath = ''
#TODO 
def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Write log to each folder test    
def infoLog(content):
    infoTestLog(content)
    infoGlobalLog(content)
    
def errorLog(content):
    if localConfig.LOG_LEVEL == ERROR:
        infoTestLog(content)
        infoGlobalLog(content)
    
def debugLog(content):
    if localConfig.LOG_LEVEL == DEBUG:
        infoTestLog(content)
        infoGlobalLog(content)            
    
def infoTestLog(content):
    loggerTest = setup_logger('test_log', localConfig.TEST_LOG_FILE_PATH)
    loggerTest.info(content)
    # Remove handler, if not remove, it will print multiple lines
    while loggerTest.handlers:
        loggerTest.handlers.pop()

def errorTestLog(content):
    loggerTest = setup_logger('test_log', localConfig.TEST_LOG_FILE_PATH)
    loggerTest.info('ERROR: ' + content)
    while loggerTest.handlers:
        loggerTest.handlers.pop()
     
def debugTestLog(content):
    loggerTest = setup_logger('test_log', localConfig.TEST_LOG_FILE_PATH)
    loggerTest.info('DEBUG: ' + content)
    while loggerTest.handlers:
        loggerTest.handlers.pop()

# Write log to global, all test combined log    
def infoGlobalLog(content):
    loggerGlobal = setup_logger('global_log', localConfig.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info(content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()

def errorGlobalLog(content):
    loggerGlobal = setup_logger('global_log', localConfig.GLOBAL_LOG_FILE_PATH)
    loggerGlobal.info('ERROR: ' + content)
    while loggerGlobal.handlers:
        loggerGlobal.handlers.pop()
     
def debugGlobalLog(content):
    loggerGlobal = setup_logger('global_log', localConfig.GLOBAL_LOG_FILE_PATH)
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
    
    
    infoGlobalLog("Exception at file     : " + traceback_details["filename"])
    infoGlobalLog("Exception at line     : " + str(traceback_details["lineno"]))
    #debugLog("Exception at function : " + traceback_details["name"])
    #debugLog("Exception type        : " + traceback_details["type"])
    infoGlobalLog("Value                 : " + str(exc_value))
    
# Initialize log - Create global log file in not exists, and creates log in current test folder
def initializeLog(testNum=None):
    if testNum != None:
        # Set Test folder path
        localConfig.TEST_LOG_FILE_FOLDER_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..',localConfig.CURRENT_PLATFORM, testNum))
        # Set Test log path
        localConfig.TEST_LOG_FILE_PATH = os.path.abspath(os.path.join(localConfig.TEST_LOG_FILE_FOLDER_PATH, testNum + '.log'))
        # Create test log folder if not exists
        if (os.path.isdir(localConfig.TEST_LOG_FILE_FOLDER_PATH) == False):
            os.makedirs(localConfig.TEST_LOG_FILE_FOLDER_PATH, exist_ok=True)        
    # Get Global log path
    localConfig.GLOBAL_LOG_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname( __file__ ),'..','Log_Global.log'))
   
# Prints to log that test setup ended, and going to execute the test flow
def readyForTestLog(testNum, platformName, platformVersion, deviceModel, deviceScreenSize):
    infoTestLog('Test Setup Ready: Test ' + testNum + ' started on ' + platformName + ', Version ' + platformVersion + ', Model ' + deviceModel + ', Resolution ' +deviceScreenSize)

# Create a screeshot with a given name it the test log folder
def takeScreeshotGeneric(driver, scName):
    # Set Test screenshot path
    scPath = os.path.abspath(os.path.join(localConfig.TEST_LOG_FILE_FOLDER_PATH, scName + '.png'))    
    try:
        driver.save_screenshot(scPath)  
    except:
        infoLog("Failed to take a screenshot, bad driver")

# Print to log the message and raises an Exception        
def raiseException(driver, msg):
    infoLog(msg)
    try:
        takeScreeshotGeneric(driver, inspect.stack()[1][3])
    except:
        infoLog("Failed to take a screenshot, bad driver")        
    raise Exception(msg)

# Return the caller class and function name
def generateErrorMsg(msg):
    return 'Function: "' + caller_name(3).split('.')[2] + '.' + caller_name(3).split('.')[3] + '.' + inspect.stack()[1][3] + ' - ' + msg

# Returns the caller class and methods when `skip` specifies how many levels of stack to skip while getting caller name
def caller_name(skip=2):
    """Get a name of a caller in the format module.class.method
    
       `skip` specifies how many levels of stack to skip while getting caller
       name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
       An empty string is returned if skipped levels exceed stack height
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start][0]    
    
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return ".".join(name)