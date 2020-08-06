import unittest

from utilities.RequestGeneratorUtil import create_GETParam

class TestHttpGetState(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetState"
    # scenarios base
    # 1 --> no project id = 404
    # 2 project id not found or invalid= 400
    # 3 200. state found

    httpMissingProjectId = {'project': ''}
    httpInvalidProjectId = {'project': 'RandomProjectId'}
    httpValidProjectId = {'project': 'template-SmartHotel360'}

    httpEscapeTest = {'project': 'template-Sm"""""artHotel360'}
    def test_noProjectid(self):
        result = create_GETParam(self.api, self.httpMissingProjectId)
        self.assertEqual(result, 404)
    def test_InvalidProjectId(self):
        result = create_GETParam(self.api, self.httpInvalidProjectId)
        self.assertEqual(result, 404)
    def test_ValidProjectId(self):
        result = create_GETParam(self.api,self.httpValidProjectId)
        self.assertEqual(result,200)
    def test_EscapeString(self):
        result = create_GETParam(self.api, self.httpEscapeTest)
        self.assertEqual(result, 400)

if __name__ == '__main__':
    unittest.main()
