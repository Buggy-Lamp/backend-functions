import unittest
from utilities.RequestGeneratorUtil import create_GETParam

class TestHttpCalcState(unittest.TestCase):
    api = "http://localhost:7071/api/HttpGetExceptions"

    # looks like we can expect the same faulty responses as in GetAvailability
    # see https://discordapp.com/channels/681905163463688239/739865576523956357/740240599739007047



#So it can be run from commandline
if __name__ == '__main__':
    unittest.main()
