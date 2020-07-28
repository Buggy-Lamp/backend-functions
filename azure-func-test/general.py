import unittest

import requests

# http://localhost:7071/api/HttpCalcState?project=template-SmartHotel360
api = "http://localhost:7071/api/HttpCalcState"


def create_request(payload):
    post = requests.post(url=api, json=payload)
    return post.status_code


class MyTestCase(unittest.TestCase):
    httpRequestData = {'project': 'template-SmartHotel360'}

    httpRequestFalseData = {'project': 'test\'ad'}

    httpRequestNotFoundData = {'project': 'project1234'}

    # This one shouldn't get caught by the server resulting in a 500 of sorts.
    httpRequestInvalidJson = {'proj3ct': 'project1234'}

    def test_validProject(self):
        # need valid project
        result = create_request(self.httpRequestData)
        self.assertEqual(200, result)

    def test_ProjectInvalidString(self):
        # InvalidProjectId literally cannot find any documentation of this exception or when it throws
        # 404 != 400
        # Expected: 400
        # Actual: 404
        result = create_request(self.httpRequestFalseData)
        self.assertEqual(400, result)

    def test_ProjectNotFound(self):
        result = create_request(self.httpRequestNotFoundData)
        self.assertEqual(404, result)

    def test_InvalidJSON(self):
        result = create_request(self.httpRequestInvalidJson)
        self.assertEqual(400, result)


if __name__ == '__main__':
    unittest.main()
