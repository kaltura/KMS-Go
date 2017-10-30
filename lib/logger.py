import logging, sys, time, os

logging.basicConfig(filename='C:\work\Mobile\KmsGo\workspace\KmsGo\log\log.txt', 
                    format='%(levelname)s %(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p: ', 
                    filemode='w', 
                    level=logging.INFO)
mylogger = logging.getLogger(__name__)
    
def info(content):
    mylogger.info(content)

def warning(content):
    logging.warning(content)
    
#=============================================================================================================================
# the function writes to the log that we started the test
#=============================================================================================================================
def logStartTest(test,platform):
    os.environ["RUNNING_TEST_ID"] = test.testNum
    info("INFO","************************************************************************************************************************")
    info("INFO","test_" + test.testNum + " Start on platform " + platform + ".")
    
#=============================================================================================================================
# the function writes in the log that we finished the test. we write if the test failed or succeeded and how much time it took 
#=============================================================================================================================
def logFinishedTest(test, startTime):
        test.duration = str(round(time.time() - startTime))
        info("INFO","test_" + test.testNum + ": " + test.status + " (" + test.duration + " sec)")
#         writeStatsToCSV(test)
        
#=============================================================================================================================
# the function writes to log the excption 
#=============================================================================================================================    
    
def log_exception(inst):
    
    exc_type, exc_value, exc_traceback = sys.exc_info() 
    traceback_details = {
                             'filename': exc_traceback.tb_frame.f_code.co_filename,
                             'lineno'  : exc_traceback.tb_lineno,
                             'name'    : exc_traceback.tb_frame.f_code.co_name,
                             'type'    : exc_type.__name__
                            }
    
    
    info("Exception at file     : " + traceback_details["filename"])
    info("Exception at line     : " + str(traceback_details["lineno"]))
    info("Exception at function : " + traceback_details["name"])
    info("Exception type        : " + traceback_details["type"])
    info("Value                 : " + str(exc_value))