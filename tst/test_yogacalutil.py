import unittest
from yogacal import yogacal
import json

class TestYogaCalUtil(unittest.TestCase):

    def test_dtstart(self):
        test = '201209160830'
        want = '20120916T083000'
        have = yogacal.YogaCal.dtstart(test)
        self.assertEqual(want, have)

    def test_dtstartOffset(self):
        test = '201209160830'
        want = '20120916T113000'
        offset = 3
        have = yogacal.YogaCal.dtstart(test, offset)
        self.assertEqual(want, have)

    def test_dtstartOffsetNegative(self):
        test = '201209160830'
        want = '20120916T053000'
        offset = -3
        have = yogacal.YogaCal.dtstart(test, offset)
        self.assertEqual(want, have)

    def test_dtend(self):
        test = '201209160830'
        mins = 75
        want = '20120916T094500'
        have = yogacal.YogaCal.dtend(test,mins)
        self.assertEqual(want, have)

    def test_dtendOffset(self):
        test = '201209160830'
        mins = 75
        offset = 3
        want = '20120916T124500'
        have = yogacal.YogaCal.dtend(test,mins,offset)
        self.assertEqual(want, have)

    def test_dtendOffsetNegative(self):
        test = '201209160830'
        mins = 75
        offset = -3
        want = '20120916T064500'
        have = yogacal.YogaCal.dtend(test,mins,offset)
        self.assertEqual(want, have)

    def test_dtend2(self):
        test = '201209160830'
        mins = 2*60 + 75
        want = '20120916T114500'
        have = yogacal.YogaCal.dtend(test,mins)
        self.assertEqual(want, have)

if __name__ == '__main__':
    unittest.main()
