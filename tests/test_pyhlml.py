import unittest

import pyhlml

class TestPyHLML(unittest.TestCase):
    def setUp(self):
        pyhlml.hlmlInitWithFlags(0)

    def tearDown(self):
        pyhlml.hlmlShutdown()

    def test_init(self):
        pass

    def test_get_device_count(self):
        # Assume HLS1-H
        exp = 4 
        count = pyhlml.hlmlDeviceGetCount()
        

if __name__ == "__main__":
    unittest.main()