import unittest

from pyhlml.hlml_lib import LibHLML

class TestLibHLML(unittest.TestCase):
    def setUp(self):
        self.lib = LoadHLML()

    def test_inc_ref(self):
        val = pyhlml._hlmlOBJ.ref_count
        pyhlml._hlmlOBJ.inc_ref()
        self.assertEqual(
            pyhlml._hlmlOBJ.ref_count,
            val + 1
        )

    def test_dec_ref(self):
        pyhlml._hlmlOBJ.ref_count = 0
        pyhlml._hlmlOBJ.dec_ref()
        self.assertEqual(
            pyhlml._hlmlOBJ.ref_count,
            0
        )
        pyhlml._hlmlOBJ.ref_count = 1
        pyhlml._hlmlOBJ.dec_ref()
        self.assertEqual(
            pyhlml._hlmlOBJ.ref_count,
            0
        )

if __name__ == "__main__":
    unittest.main()