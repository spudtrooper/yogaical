import unittest
from yogacal import yogacal
import json

class TestYogaCal(unittest.TestCase):

    def setUp(self):
        self.c = yogacal.YogaCal()

    def test_request(self):
        req = self.c.request()
        self.assertIsNotNone(req)

    def test_yogacal(self):
        self.assertIsNotNone(self.c)

if __name__ == '__main__':
    unittest.main()
