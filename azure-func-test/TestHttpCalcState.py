import unittest
from RequestGeneratorUtil import create_POST

api = "http://localhost:7071/api/HttpCalcState"
# http://localhost:7071/api/HttpCalcState/template-SmartHotel360


class TestHttpCalcState(unittest.TestCase):
    httpRequestData = {'project': 'template-SmartHotel360'}

    httpRequestFalseData = {'project': 'test\'ad'}

    httpRequestNotFoundData = {'project': 'project1234'}

    httpRequestInvalidJson = {'proj3ct': 'project1234'}

    def test_validProject(self):
        # need valid project
        result = create_POST(api,self.httpRequestData)
        self.assertEqual(200, result)

    def test_ProjectInvalidString(self):
        result = create_POST(api,self.httpRequestFalseData)
        self.assertEqual(400, result)

    def test_ProjectNotFound(self):
        result = create_POST(api,self.httpRequestNotFoundData)
        self.assertEqual(404, result)

    def test_InvalidJSON(self):
        result = create_POST(api,self.httpRequestInvalidJson)
        self.assertEqual(400, result)


#So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
