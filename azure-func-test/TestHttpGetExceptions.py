import unittest
from utilities.RequestGeneratorUtil import create_GETParam


class TestHttpGetExceptions(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetExceptions"

    # looks like we can expect the same faulty responses as in GetAvailability
    # see https://discordapp.com/channels/681905163463688239/739865576523956357/740240599739007047

    # TODO: Fix HTTP responses, all give 200 now. even for bad requests.
    # TODO: Edit test-implementation accordingly.

    missingKey = {'api_name': 'DEMO_APP'}
    missingApi = {'api_key': "DEMO_KEY"}
    invalidKeyApiPair = {'api_name': 'api123', 'api_key': 'apiKey123'}
    invalidName = {'api_name': 'api123', 'api_key': 'DEMO_KEY'}
    invalidKey = {'api_name': 'DEMO_APP', 'api_key': 'apiKey123'}
    invalidParam = {'faulty': 'error123'}
    noParams = {}
    validPair = {'api_name': 'DEMO_APP', 'api_key': 'DEMO_KEY'}

    def test_MissingKey(self):
        result = create_GETParam(self.api, self.missingKey)
        self.assertEqual(result, 400)

    def test_MissingAPi(self):
        result = create_GETParam(self.api, self.missingApi)
        self.assertEqual(result, 400)

    def test_invalidKeyApiPair(self):
        result = create_GETParam(self.api, self.invalidKeyApiPair)
        self.assertEqual(result, 400)

    def test_invalidName(self):
        result = create_GETParam(self.api, self.invalidName)
        self.assertEqual(result, 400)

    def test_invalidKey(self):
        result = create_GETParam(self.api, self.invalidKey)
        self.assertEqual(result, 400)

    def test_invalidParams(self):
        result = create_GETParam(self.api, self.invalidParam)
        self.assertEqual(result, 400)

    def test_noParams(self):
        result = create_GETParam(self.api, self.noParams)
        self.assertEqual(result, 400)

    def test_validPair(self):
        result = create_GETParam(self.api, self.validPair)
        self.assertEqual(result, 200)


# So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
