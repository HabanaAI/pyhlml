import unittest
import subprocess

import pyhlml

_hlmlOBJ = pyhlml.LibHLML()

def count_from_smi():
	""" Get device count from SMI as a reference """
	res = subprocess.run(
		["hl-smi", "--query-aip=name", "--format=csv,nounits,noheader", "|", "wc", "-l"],
		stdout=subprocess.PIPE
	)
	return res.stdout.decode()

class TestPyHLML_Handles(unittest.TestCase):

	def test_get_handle_by_index(self):
		""" We expect the number of handles == device count """
		count = pyhlml.LibHLML 