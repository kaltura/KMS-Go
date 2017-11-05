import os
  
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
   

def pytest_addoption(parser):
    parser.addoption("--env", action="store",help="env: the env that runs the tests e.g. qa , dev")

def pytest_funcarg__env(request):
    return request.config.option.env