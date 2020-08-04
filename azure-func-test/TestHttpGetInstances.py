import unittest
from utilities.RequestGeneratorUtil import create_GETParam

class TestHttpCalcState(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetInstances"

    # scenarios base
    # 1 --> no project id = 400
    # 2 invalid project id = 400
    # 3 invalid instance name = 400
    # 4 if no settings found return 404. line 34 - 39 most likely needs dummy data.
    # 5 200.


#So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
