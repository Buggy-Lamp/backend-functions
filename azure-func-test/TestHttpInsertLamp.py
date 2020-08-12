import unittest
from .utilities.RequestGeneratorUtil import create_POST


class TestHttpInsertLamp(unittest.TestCase):
    api = "http://localhost:7071/api/HttpInsertLamp"

    noData = {}
    incorrectData = {"invalid": "FF:FF:FF:FF:FF:FF"}
    correctData = {"mac": "FF:FF:FF:FF:FF:FF"}

    # scenarios base
    # 1 --> no JSON = 400
    # 2 invalid json = 400
    # 3 200. lamp added.
    # 4 no request body

    def test_noJson(self):
        result = create_POST(self.api, self.noData)
        self.assertEqual(result, 400)

    def test_invalidJson(self):
        result = create_POST(self.api, self.incorrectData)
        self.assertEqual(result, 400)

    def test_CorrectData(self):
        result = create_POST(self.api, self.correctData)
        self.assertEqual(result, 200)

    def test_theNoBodyBody(self):
        result = create_POST(self.api, "")
        self.assertEqual(result, 400)


if __name__ == '__main__':
    unittest.main()
