import unittest

import pyhlml

def count_from_smi():
	""" Get device count from SMI as a reference """
	with os.popen(
		"/usr/bin/hl-smi --query-aip=name --format=csv,nounits,noheader"
	) as proc:
		stdout = proc.readlines()
	return len(stdout)

class TestPyHLML_Metrics(unittest.TestCase):
    def setUp(self):
        pyhlml.hlmlInit()
        self.device = pyhlml.hlmlDeviceGetHandleByIndex(0)
	
    def tearDown(self):
        pyhlml.hlmlShutdown()

if __name__ == "__main__":
    unittest.main()
