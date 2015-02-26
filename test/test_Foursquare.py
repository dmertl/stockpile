import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Foursquare import Checkin, Model
import json
import os


class Test(unittest.TestCase):
    def test_stockpile_checkins(self):
        # Mock API
        Checkin.api = FoursquareApiTest()

        # Create connection to test DB
        # TODO: Move test DB creation and cleanup into somewhere shareable
        os.remove('data/test_foursquare.sqlite')
        engine = create_engine('sqlite:///db/test_foursquare.sqlite')
        Session = sessionmaker(bind=engine)
        session = Session()
        Model.Base.metadata.create_all(engine)

        Checkin.db = session

        # Stockpile
        Checkin.limit = 20
        Checkin.stockpile()

        # Assert
        self.assertEqual(59, session.query(Model.Checkin).count())
        self.assertEqual(45, session.query(Model.Venue).count())
        self.assertEqual(33, session.query(Model.Category).count())
        checkin = session.query(Model.Checkin).filter(Model.Checkin.id == '54850764498e71cb1901cf3c').first()
        self.assertEqual(1418004324, checkin.createdAt)
        self.assertEqual('with pinguino', checkin.shout)
        self.assertEqual('Reno-Tahoe International Airport (RNO)', checkin.venue.name)
        self.assertEqual('Airport', checkin.venue.categories[0].name)

# TODO: Use mock library rather than creating separate class
class FoursquareApiTest(object):
    class Users(object):
        def __call__(self):
            return {
                'user': {
                    'id': 1234
                }
            }

        def checkins(self, USER_ID=u'self', params={}):
            # Test data only supports limit=20 and offset=0,20,40
            offset = params['offset'] if 'offset' in params else 0
            data_filename = 'checkins_{}.json'.format(offset)
            return json.load(open(os.path.join('data', data_filename)))

    users = Users()

if __name__ == "__main__":
    unittest.main()
