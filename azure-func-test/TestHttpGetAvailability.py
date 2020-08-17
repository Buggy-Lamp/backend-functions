import unittest
from utilities.RequestGeneratorUtil import create_get


class TestHttpGetAvailability(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetAvailability"

    missingKey = {'api_name': 'DEMO_APP'}
    missingApi = {'api_key': "DEMO_KEY"}
    invalidKeyApiPair = {'api_name': 'api123', 'api_key': 'apiKey123'}
    invalidName = {'api_name': 'api123', 'api_key': 'DEMO_KEY'}
    invalidKey = {'api_name': 'DEMO_APP', 'api_key': 'apiKey123'}
    invalidParam = {'faulty': 'error123'}
    noParams = {}
    validPair = {'api_name': 'DEMO_APP', 'api_key': 'DEMO_KEY'}

    def test_MissingKey(self):
        result = create_get(self.api, self.missingKey)
        self.assertEqual(result, 400)

    def test_MissingAPi(self):
        result = create_get(self.api, self.missingApi)
        self.assertEqual(result, 400)

    def test_invalidKeyApiPair(self):
        result = create_get(self.api, self.invalidKeyApiPair)
        self.assertEqual(result, 403)

    def test_invalidName(self):
        result = create_get(self.api, self.invalidName)
        self.assertEqual(result, 403)

    def test_invalidKey(self):
        result = create_get(self.api, self.invalidKey)
        self.assertEqual(result, 403)

    def test_invalidParams(self):
        result = create_get(self.api, self.invalidParam)
        self.assertEqual(result, 400)

    def test_noParams(self):
        result = create_get(self.api, self.noParams)
        self.assertEqual(result, 400)

    def test_validPair(self):
        result = create_get(self.api, self.validPair)
        self.assertEqual(result, 200)


# So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
