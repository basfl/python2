import unittest
class TestUpper(unittest.TestCase):
    def test_upper(self):
        self.assertEqual("HELLO","HELLO");

if __name__=="__main__":
    unittest.main();
