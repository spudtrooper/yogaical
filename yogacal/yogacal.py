import urllib
import urllib2
import logging
import json
import re

class JsonObj:

    def __init__(self,id):
        self.id = int(id)

class Instructor(JsonObj):

    def __init__(self,id,name):
        JsonObj.__init__(self,id)
        self.name = name

    @staticmethod
    def fromJson(obj):
        return Instructor(obj['id'], obj['n'])

class Class(JsonObj):
    
    def __init__(self,id,name,description):
        JsonObj.__init__(self,id)
        self.name = name
        self.description = description

    @staticmethod
    def fromJson(obj):
        return Class(obj['id'], obj['n'], obj['d'])

class Location(JsonObj):

    def __init__(self,id,name,lat,lng,city,address,state,phone):
        JsonObj.__init__(self,id)
        self.name = name
        self.lat = float(lat)
        self.lng = float(lng)
        self.city = city
        self.address = address
        self.state = state
        self.phone = phone

    @staticmethod
    def fromJson(obj):
        return Location(obj['id'], obj['n'], obj['t'], obj['g'], obj['ct'], 
                        obj['ad'], obj['state'], obj['ph'])

class YogaCalItem:

    def __init__(self,instructor,klass,location,date,mins):
        self.instructor = instructor
        self.klass = klass
        self.location = location
        self.date = date
        self.mins = mins
        

class YogaCalJsonAdapter:
    
    def __init__(self,obj):

        self.items = []

        ids2instructors = {}
        for jsonObj in obj['instructors']:
            o = Instructor.fromJson(jsonObj)
            ids2instructors[o.id] = o

        ids2locations = {}
        for jsonObj in obj['locations']:
            o = Location.fromJson(jsonObj)
            ids2locations[o.id] = o

        ids2classes = {}
        for jsonObj in obj['classes']:
            o = Class.fromJson(jsonObj)
            ids2classes[o.id] = o

        for jsonObj in obj['data']:
            instructor = ids2instructors[int(jsonObj['s'])]
            klass = ids2classes[int(jsonObj['d'])]
            location = ids2locations[int(jsonObj['l'])]
            date = jsonObj['od']
            mins = int(jsonObj['r'])
            item = YogaCalItem(instructor, klass, location, date, mins)
            self.items.append(item)
            

class YogaCal:

    def __init__(self):
        self.log = logging.getLogger('YogaCal')

    def header(self,locations=None):
        res = ''
        res += "BEGIN:VCALENDAR\r\n"
        res += "VERSION:2.0\r\n"
        res += "PRODID:-//jeffpalm/yogacal//NONSGML v1.0//EN\r\n"
        name = 'Yoga'        
        if locations and len(locations) > 0:
            name += "--"
            name += "/".join(locations)
        res += "X-WR-CALNAME:%s\r\n" % (name)
        return res

    def footer(self):
        res = ''
        res += "END:VCALENDAR\r\n"
        return res

    @staticmethod
    def pad(n):
        if (n < 10):
            return '0%d' % (n)
        return '%d' % (n)

    @staticmethod
    def dtstart(dateStr):
        # 201209160830 -> 20120916T083000
        date = dateStr[0:8]    # 20120916
        time = dateStr[8:]     # 0830
        hours = int(time[0:2]) # 08
        mins = int(time[2:])   # 30
        newTime = '%s%s00' % (YogaCal.pad(hours), 
                              YogaCal.pad(mins))
        return '%sT%s' % (date,newTime)

    @staticmethod
    def dtend(dateStr,dur):
        # 201209160830, 75 -> 20120916T094500
        date = dateStr[0:8]            # 20120916
        time = dateStr[8:]             # 0830
        hours = int(time[0:2])         # 08
        mins = int(time[2:])           # 30
        
        carryHours = (mins + dur) / 60 # 1  = (30 + 75) / 60
        #                                   =       105 / 60
        newHours = hours + carryHours  # 9  = 8 + 1
        newMins = (mins + dur) % 60    # 15 = (30 + 75) % 60
        #                                   =       105 % 60
        newTime = '%s%s00' % (YogaCal.pad(newHours), 
                              YogaCal.pad(newMins))
        return '%sT%s' % (date,newTime)

    @staticmethod
    def removeHTML(str):
        res = str
        res = re.sub('&#\d{4};','',res)
        res = re.sub('\s+',' ',res)
        return res

    def toEvent(self,item):
        res = ''
        res += "BEGIN:VEVENT\r\n"
        uid = '%d-%d-%d' % (item.klass.id,
                            item.instructor.id,
                            item.location.id)
        #res += "UID:%s\r\n" % (uid)
        start = YogaCal.dtstart(item.date)
        end = YogaCal.dtend(item.date,item.mins)
        res += "DTSTART:%s\r\n" % (start)
        res += "DTEND:%s\r\n" % (end)
        summary = '%s: %s @ %s (%d mins)' % (item.instructor.name,
                                             item.klass.name,
                                             item.location.name,
                                             item.mins)
        summary = YogaCal.removeHTML(summary)
        res += "SUMMARY:%s\r\n" % (summary)
        res += "LOCATION:%s: %s, %s, %s\r\n" % (item.location.name,
                                                item.location.address,
                                                item.location.city,
                                                item.location.state)
        res += "END:VEVENT\r\n"
        return res

    def requestItems(self, locations=None, levels=None, instructors=None):
        """
        @param locations None or empty means we use all the cities
        @return iCal version of calendar at: http://schedule.yogaworks.com
        """
        if not locations:
            locations = []
        if not levels:
            levels = []
        if not instructors:
            instructors = []
        levelsStr = '|'.join(['.*\(%s\).*' % (str(level)) for level in levels])
        levelRe = re.compile(levelsStr)
        res = self.request()
        adp = YogaCalJsonAdapter(json.read(res))
        filteredItems = adp.items

        # Filter by locations
        filteredItems = filter(lambda it: len(locations) == 0 or 
                               (it.location.name in locations), 
                               filteredItems)

        # Filter by levels
        filteredItems = filter(lambda it: len(levels) == 0 or
                               re.match(levelRe, it.klass.name), 
                               filteredItems)

        # Filter by instructors
        filteredItems = filter(lambda it: len(instructors) == 0 or 
                               (it.instructor.name in instructors), 
                               filteredItems)
        return filteredItems
    
    def ics(self, **kwargs):
        items = self.requestItems(**kwargs)
        locations = kwargs.get('locations') or []
        res = self.header(locations)        
        for it in items:
            res += self.toEvent(it)
        res += self.footer()
        return res

    def request(self):
        data = {
            'hsrc':'rtc',
            'name':'gtSchd',
            'action':'pr',
            'owner':'yogaworks',
            'dy':'2',
            'offset':'0',
            'regionVl':'-140'
            }
        url = 'http://schedule.yogaworks.com/rq/'
        req = urllib2.Request(url, urllib.urlencode(data))
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        return response
        
