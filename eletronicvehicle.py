from google.appengine.ext import ndb


class Reviews(ndb.Model):
    review = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    vehicle_id = ndb.IntegerProperty()
    sequence = ndb.IntegerProperty()
    email_address = ndb.StringProperty()



class EleVhe(ndb.Model):
    #email address of this users
    email_address = ndb.StringProperty()
    #name, manufacturer, year, battery size (Kwh), WLTP range(Km), cost, power (Kw).

    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    btrysize = ndb.IntegerProperty()
    wltprng = ndb.IntegerProperty()
    cost = ndb.IntegerProperty()
    power = ndb.IntegerProperty()
    review = ndb.StructuredProperty(Reviews, repeated=True)
