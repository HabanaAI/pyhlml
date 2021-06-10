from pyhlml.hlml_error import HLMLError
import unittest

from pyhlml.hlml_lib import LibHLML

class TestLibHLML(unittest.TestCase):
    lib = None
    
    def setUp(self):
        self.lib = LibHLML()

    def tearDown(self):
        self.lib = None

    def test_single_setup(self):
        """ Init lib then shutdown
            Autocompletes as part of setUp/Teardown
        """
        pass

    def test_inc_ref(self):
        start = self.lib.ref_count
        self.lib.inc_ref()
        self.assertEqual(start+1, self.lib.ref_count)

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

    def test_load_init(self):
        ret = self.lib.get_func_ptr("hlml_init")
        self.assertIsNotNone(ret)

    def test_invalid_ptr(self):
        with self.assertRaises(HLMLError):
            self.lib.get_func_ptr("foo")
       
if __name__ == "__main__":
    unittest.main()