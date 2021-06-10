import unittest

from pyhlml.hlml_lib import LibHLML

class TestLibHLML(unittest.TestCase):
    lib = None
    
    def setUp(self):
        if TestLibHLML.lib == None:
            setattr(TestLibHLML, 'lib', LibHLML())

    def test_single_setup(self):
        """ Init lib then shutdown """

    def test_inc_ref(self):
        TestLibHLML.lib.ref_count

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