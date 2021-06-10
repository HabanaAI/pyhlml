import unittest
import subprocess

import pyhlml

def count_from_smi():
	""" Get device count from SMI as a reference """
	res = subprocess.run(
		["hl-smi", "--query-aip=name", "--format=csv,nounits,noheader", "|", "wc", "-l"],
		stdout=subprocess.PIPE
	)
	return res.stdout.decode()

class TestPyHLML_Handles(unittest.TestCase):
	def setUp(self):
		pyhlml.hlmlInit()

	def tearDown(self):
		pyhlml.hlmlShutdown()

	def test_get_handle_by_index(self):
		""" We expect the number of handles == device count """
		smi_count = count_from_smi()
		devices = []
		for i in range(smi_count):
			device = pyhlml.hlmlDeviceGetHandleByIndex(i)
			self.assertIsNotNone(device.value)
			devices.append(device)
		self.assertEqual(len(devices), smi_count)

