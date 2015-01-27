__author__ = 'dmertl'

class Base:
    def fromResponse(response):
        checkin = Checkin()
        for k,v in response.iteritems():
            checkin[k] = v
        return checkin

class Checkin(Base):
    whitelist = ['id', 'createdAt']

class Venue(Base):
    whitelist = ['id', 'name']

    def fromResponse(response):
        venue = super.fromResponse(response)
        for k,v in response.location.iteritems():
            venue['location_' + k] = v
        return venue

class Category(Base):
    whitelist = ['id', 'name', 'pluralName', 'shortName', 'primary']
