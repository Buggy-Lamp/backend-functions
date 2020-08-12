import unittest
from utilities.RequestGeneratorUtil import create_GETParam


class TestHttpDeleteInstance(unittest.TestCase):
    api = "http://localhost:7071/api/HttpDeleteInstance"

    # We can only unitTest invalid requests here as otherwise we will actively transform the database
    # resulting in an integration test.
    # even tho these tests also in some way shape or form interact with the database.

    httpRequestData = {'project': 'template-SmartHotel360'}
    httpRequestDataLamp = {'lampid': 'falseId'}
    invalidJson = {'invalid': 'json'}
    incorrectDetails = {'project': 'project123', 'lampid': 'lamp123'}

    def test_MissingLampParam(self):
        result = create_GETParam(self.api, self.httpRequestData)
        self.assertEqual(result, 400)

    def test_MissingParamProject(self):
        result = create_GETParam(self.api, self.httpRequestDataLamp)
        self.assertEqual(result, 400)

    def test_invalidRequest(self):
        result = create_GETParam(self.api, self.invalidJson)
        self.assertEqual(result, 400)

    def test_InvalidDetails(self):
        result = create_GETParam(self.api, self.incorrectDetails)
        self.assertEqual(result, 404)


# So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
