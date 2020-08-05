import unittest
from utilities.RequestGeneratorUtil import create_GETParam

class TestHttpCalcState(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetInstances"

    # scenarios base
    # 1 --> no project id = 400
    # 2 invalid project id = 400
    # 3 200. when only a project id is added
    # 4 200. when a project id and instance is filled in.
    httpMissingProjectId = {'project':''}
    httpInvalidProjectId = {'project': 'RandomProjectId'}
    httpValidProjectId   = {'project':'template-SmartHotel360'}
    httpValidInstanceAndProjectId   = {'project':'template-SmartHotel360' , 'instance_name': 'JavaClient'}

    def test_NoProjectId(self):
        result = create_GETParam(self.api, self.httpMissingProjectId)
        self.assertEqual(result, 400)
    def test_InvalidProjectId(self):
        result = create_GETParam(self.api,self.httpInvalidProjectId)
        self.assertEqual(result, 404)
    def test_allInstanceProject(self):
        result = create_GETParam(self.api,self.httpValidProjectId)
        self.assertEqual(result,200)
    def test_getOneInstance(self):
        result = create_GETParam(self.api,self.httpValidInstanceAndProjectId)
        self.assertEqual(result,200)



#So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
