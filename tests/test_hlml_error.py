from pyhlml.hlml_error import HLMLError
import unittest

import pyhlml

class TestPyHLML_Error(unittest.TestCase):

	def raise_HLMLError(self, error):
		raise HLMLError(error)

	def test_HLMLError(self):
		""" Verify exception thrown for each input """
		count = 0
		num_errs_types = len(pyhlml.HLMLError._errcodes)
		for i in range(num_errs_types):
			with self.assertRaises(HLMLError):
				self.raise_HLMLError(i)
			count += 1
		self.assertEqual(count, num_errs_types)


if __name__ == "__main__":
	unittest.main()