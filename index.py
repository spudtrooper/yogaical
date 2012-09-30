from yogacal import yogacal

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class YogaCalPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        levels = self.request.get_all('levels')
        locations = self.request.get_all('locations')
        instructorsIn = self.request.get_all('instructors')
        
        # Make sure there are no empty strings
        instructors = []
        for i in instructorsIn:
            if i and i != '':
                instructors.append(i)
        offset = self.request.get('offset')
        cal = yogacal.YogaCal()
        self.response.out.write(cal.ics(locations=locations,
                                        levels=levels,
                                        instructors=instructors,
                                        offset=offset))

application = webapp.WSGIApplication(
  [('/yoga/cal.ics', YogaCalPage)],
  debug=True
  )

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
