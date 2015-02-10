from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Foursquare import Checkin
import foursquare

engine = create_engine('sqlite:///foursquare.sqlite')
Session = sessionmaker(bind=engine)
session = Session()

api = foursquare.Foursquare(
    client_id='',
    client_secret='',
    redirect_uri='http://dmertl.com/test/dump.php')

# Get access token from oauth token
# access_token = api.oauth.get_token('')
# print "Access_token: '{0}'".format(access_token)

# Once you have access token
api.set_access_token('')

try:
    Checkin.db = session
    Checkin.api = api
    Checkin.stockpile()
    # Now I can query my local DB for checkins
except foursquare.NotAuthorized:
    auth_uri = api.oauth.auth_url()
    print "User not authorized. Get oauth token from: {0}".format(auth_uri)
