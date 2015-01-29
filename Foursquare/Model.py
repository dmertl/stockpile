from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, backref


Base = declarative_base()


class FoursquareBase(Base):
    """
    Foursquare base model.
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        # Only set attributes that are defined columns on the model
        # TODO: Problem with setting relationship attributes? i.e. Venue.categories and response['venue']['categories']
        for i in self.__class__.__table__.columns:
            try:
                self.__setattr__(i.key, kwargs[i.key])
            except KeyError:
                continue


class Checkin(FoursquareBase):
    """
    Foursquare checkin model.
    """
    __tablename__ = 'checkins'

    id = Column(String(24), primary_key=True)
    createdAt = Column(Integer)
    shout = Column(String(128))
    venue_id = Column(String(24), ForeignKey('venues.id'))

    venue = relationship('Venue', backref=backref('checkins'))


# Venue - Category join table
venue_categories = Table(
    'venue_categories',
    Base.metadata,
    Column('venue_id', String(24), ForeignKey('venues.id')),
    Column('category_id', String(24), ForeignKey('categories.id'))
)


class Venue(FoursquareBase):
    """
    Foursquare venue model.
    """
    __tablename__ = 'venues'

    locationFields = ['address', 'crossStreet', 'lat', 'lng', 'postalCode', 'cc', 'city', 'state', 'country']

    id = Column(String(24), primary_key=True)
    name = Column(String(128))
    location_address = Column(String(128))
    location_crossStreet = Column(String(128))
    location_lat = Column(Float)
    location_lng = Column(Float)
    location_postalCode = Column(String(32))
    location_cc = Column(String(32))
    location_city = Column(String(64))
    location_state = Column(String(64))
    location_country = Column(String(64))

    categories = relationship('Category', secondary=venue_categories, backref='venues')

    def __init__(self, **kwargs):
        # Map Foursquare venue location dict to location_ fields
        for i in self.locationFields:
            try:
                self.__setattr__('location_' + i, kwargs['location'][i])
            except KeyError:
                continue
        try:
            del kwargs['location']
        except KeyError:
            pass
        super(Venue, self).__init__(**kwargs)


class Category(FoursquareBase):
    """
    Foursquare category model.
    """
    __tablename__ = 'categories'

    id = Column(String(24), primary_key=True)
    name = Column(String(128))
    pluralName = Column(String(128))
    shortName = Column(String(128))
    primary = Column(Boolean)
