import unittest
from utilities.RequestGeneratorUtil import create_post

class TestHttpInsertTreshold(unittest.TestCase):
    api = "http://localhost:7071/api/InsertTreshold"
    def test_newproject(self):
        json = {
            "project": "testproject",
            "tools": [
                {
                    "tool_name": "application_insights",
                    "instances": [
                        {
                            "instance_name": "test",
                            "api_name": "DEMO_APP",
                            "api_key": "DEMO_KEY",
                            "properties": [
                                {
                                    "property_name": "exceptions",
                                    "active": False,
                                    "thresholds": [
                                        {
                                            "min": 0,
                                            "color": "green"
                                        },
                                        {
                                            "min": 5,
                                            "color": "orange"
                                        },
                                        {
                                            "min": 20,
                                            "color": "red"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        result = create_post(self.api, json)
        self.assertEqual(result, 200)
    def test_newtool(self):
        json = {
            "project": "testproject",
            "tools": [
                {
                    "tool_name": "new_tool",
                    "instances": [
                        {
                            "instance_name": "test",
                            "api_name": "DEMO_APP",
                            "api_key": "DEMO_KEY",
                            "properties": [
                                {
                                    "property_name": "exceptions",
                                    "active": False,
                                    "thresholds": [
                                        {
                                            "min": 0,
                                            "color": "green"
                                        },
                                        {
                                            "min": 5,
                                            "color": "orange"
                                        },
                                        {
                                            "min": 20,
                                            "color": "red"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        result = create_post(self.api, json)
        self.assertEqual(result, 200)
    def test_newinstance(self):
        json = {
            "project": "testproject",
            "tools": [
                {
                    "tool_name": "newtool",
                    "instances": [
                        {
                            "instance_name": "test",
                            "api_name": "DEMO_APP",
                            "api_key": "DEMO_KEY",
                            "properties": [
                                {
                                    "property_name": "exceptions",
                                    "active": False,
                                    "thresholds": [
                                        {
                                            "min": 0,
                                            "color": "green"
                                        },
                                        {
                                            "min": 5,
                                            "color": "orange"
                                        },
                                        {
                                            "min": 20,
                                            "color": "red"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        result = create_post(self.api, json)
        self.assertEqual(result, 200)
    def test_newtreshold(self):
        json = {
            "project": "testproject",
            "tools": [
                {
                    "tool_name": "newtool",
                    "instances": [
                        {
                            "instance_name": "test",
                            "api_name": "DEMO_APP",
                            "api_key": "DEMO_KEY",
                            "properties": [
                                {
                                    "property_name": "exceptions",
                                    "active": False,
                                    "thresholds": [
                                        {
                                            "min": 0,
                                            "color": "green"
                                        },
                                        {
                                            "min": 3,
                                            "color": "orange"
                                        },
                                        {
                                            "min": 20,
                                            "color": "red"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        result = create_post(self.api, json)
        self.assertEqual(result, 200)

if __name__ == '__main__':
    unittest.main()
