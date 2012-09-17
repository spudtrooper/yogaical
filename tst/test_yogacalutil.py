import unittest
from yogacal import yogacal
import json

class TestYogaCalUtil(unittest.TestCase):

    def test_dtstart(self):
        test = '201209160830'
        want = '20120916T0830'
        have = yogacal.YogaCal.dtstart(test)
        self.assertEqual(want, have)

    def test_dtend(self):
        test = '201209160830'
        mins = 75
        want = '20120916T0945'
        have = yogacal.YogaCal.dtend(test,mins)
        self.assertEqual(want, have)

    def test_dtend2(self):
        test = '201209160830'
        mins = 2*60 + 75
        want = '20120916T1145'
        have = yogacal.YogaCal.dtend(test,mins)
        self.assertEqual(want, have)

if __name__ == '__main__':
    unittest.main()
