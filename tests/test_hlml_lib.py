import unittest

from pyhlml.libhlml import LibHLML

class TestLibHLML(unittest.TestCase):
    def setUp(self):
        self.lib = LibHLML()

    def test_inc_ref(self):
        val =self.lib.ref_count
        self.lib.inc_ref()
        self.assertEqual(
           self.lib.ref_count,
            val + 1
        )

    def test_dec_ref(self):
       self.lib.ref_count = 0
       self.lib.dec_ref()
       self.assertEqual(
           self.lib.ref_count,
            0
        )
       self.lib.ref_count = 1
       self.lib.dec_ref()
       self.assertEqual(
           self.lib.ref_count,
            0
        )

if __name__ == "__main__":
    unittest.main()