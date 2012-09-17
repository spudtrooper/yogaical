import unittest
from yogacal import yogacal
import json

class TestYogaCalAdapter(unittest.TestCase):

    def test_instructor(self):
        obj = {"n":"Dilshad Keshwani","id":100000033,"instFd":0}
        res = yogacal.Instructor.fromJson(obj)
        self.assertEqual("Dilshad Keshwani",res.name)
        self.assertEqual(100000033,res.id)

    def test_location(self):
        obj = {"id":1,"n":"Eastside","t":40.7719049,"g":-73.958608,"ct":"New York","ad":"1319 Third Avenue (2nd Floor)","state":"NY","ph":"2126509642"}
        res = yogacal.Location.fromJson(obj)
        self.assertEqual("Eastside",res.name)
        self.assertEqual(40.7719049,res.lat)
        self.assertEqual(-73.958608,res.lng)
        self.assertEqual("New York",res.city)
        self.assertEqual('1319 Third Avenue (2nd Floor)',res.address)
        self.assertEqual('NY',res.state)
        self.assertEqual('2126509642',res.phone)

    def test_class(self):
        obj = {"id":-1047507937,"n":"Ishta (2)","d":"Designed to take students to the intermediate level. Further strength, stamina, and flexibility will be required as more advanced postures and sequences are introduced.  Introduction to inversions, more challenging backbends, and arm balances.  Created by yogi master Alan Finger, ISHTA (Integrated Science of Hatha, Tantra, and Ayurveda) combines asana, pranayama, and meditation for a comprehensive physical and spiritual practice.  Ishta is a Sanskrit word meaning \u201cindividualized,\u201d reflecting the tradition\u2019s aim of helping each student develop a practice that meets his or her personal needs.  "}
        res = yogacal.Class.fromJson(obj)
        self.assertEqual('Ishta (2)',res.name)
        self.assertEqual('Designed to take students to the intermediate level. Further strength, stamina, and flexibility will be required as more advanced postures and sequences are introduced.  Introduction to inversions, more challenging backbends, and arm balances.  Created by yogi master Alan Finger, ISHTA (Integrated Science of Hatha, Tantra, and Ayurveda) combines asana, pranayama, and meditation for a comprehensive physical and spiritual practice.  Ishta is a Sanskrit word meaning \u201cindividualized,\u201d reflecting the tradition\u2019s aim of helping each student develop a practice that meets his or her personal needs.  ',res.description)

    def test_adapter(self):
        str = ''
        with open('tst/adapter.json', 'r') as f:
            str += f.read()
        obj = json.read(str)
        adp = yogacal.YogaCalJsonAdapter(obj)
                         
        

if __name__ == '__main__':
    unittest.main()
