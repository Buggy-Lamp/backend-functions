import unittest
from utilities.RequestGeneratorUtil import create_GETParam


class TestHttpGetTypes(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetTypes"
    # scenarios base
    # 1 --> no project id = 404

    Httpcheck = {}

    def test_TypesAvailible(self):
        result = create_GETParam(self.api, self.Httpcheck)
        self.assertEqual(result, 200)


if __name__ == '__main__':
    unittest.main()
