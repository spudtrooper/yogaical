import unittest
from yogacal import yogacal
import json
import re

class TestYogaCal(unittest.TestCase):

    def setUp(self):
        self.c = yogacal.YogaCal()

    def test_request(self):
        req = self.c.request()
        self.assertIsNotNone(req)

    def test_ics(self):
        ics = self.c.ics()
        self.assertIsNotNone(ics)

    def test_ics_soho(self):
        locations = ['Soho']
        ics = self.c.requestItems(locations=locations)
        self.assertIsNotNone(ics)
        self.assertGreater(len(ics), 1)

    def test_ics_soho_unionSquare(self):
        locations = ['Soho', 'Union Square']
        ics = self.c.requestItems(locations=locations)
        self.assertIsNotNone(ics)
        self.assertGreater(len(ics), 1)

    def test_ics_soho_levels1(self):
        levels = ['1']
        ics = self.c.requestItems(levels=levels)
        self.assertIsNotNone(ics)
        self.assertGreater(len(ics), 1)
        for i in ics:
            self.assertTrue(re.search('\(1\)', i.klass.name))

    def test_ics_instructor(self):
        instructors = ['Chrissy Carter']
        ics = self.c.requestItems(instructors=instructors)
        self.assertIsNotNone(ics)
        self.assertGreater(len(ics), 1)
        for i in ics:
            self.assertTrue(re.search('Chrissy Carter', i.instructor.name))

    def test_yogacal(self):
        self.assertIsNotNone(self.c)

if __name__ == '__main__':
    unittest.main()
