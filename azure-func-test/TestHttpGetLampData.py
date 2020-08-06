import unittest
from utilities.RequestGeneratorUtil import create_GETParam


class TestHttpGetLampData(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetLampData"
    # scenarios base
    # 1 --> no lamp id = 404
    # 2 Lamp  id  not found or invalid= 400
    # 3 200. Lamp found

    httpMissingLampID = {'lampid': ''}

    httpRandomLampID = {'lampid': 'randomlampid'}

    httpFoundlampId = {'lampid': 'f427249f-61d7-4e05-a495-a64e28478af0'}
    def test_noLampId(self):
        result = create_GETParam(self.api, self.httpMissingLampID)
        self.assertEqual(result, 404)
    def test_LampIdNotFound(self):
        result = create_GETParam(self.api, self.httpRandomLampID)
        self.assertEqual(result, 404)
    def test_LampIdNotFound(self):
        result = create_GETParam(self.api, self.httpFoundlampId)
        self.assertEqual(result, 200)


if __name__ == '__main__':
    unittest.main()
