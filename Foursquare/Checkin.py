from Model import Checkin, Venue, Category

"""
Stockpile Foursquare checkins.
"""

# TODO: Limit should move into API
limit = 250

# TODO: Better way to set db and api
db = None
api = None


def stockpile(USER_ID='self'):
    """

    :param USER_ID: Foursquare user to stockpile checkins for.
    :type USER_ID: str
    """
    if USER_ID == 'self':
        user = api.users()
        user_id = user['user']['id']
    else:
        user_id = USER_ID
    params = {
        'offset': 0
    }
    # Get timestamp of user's last checkin
    last_checkin = _get_last_timestamp(user_id)
    if last_checkin:
        # Get only checkins newer than user's last checkin
        params['afterTimestamp'] = last_checkin
    else:
        # Get all user's checkins starting with the oldest
        params['sort'] = 'oldestfirst'

    _stockpile_loop(user_id, params)


def _stockpile_loop(user_id, params):
    """
    TODO: better name

    :param user_id: Foursquare user to stockpile checkins for.
    :type user_id: str
    :param params: API request parameters.
    :type params: dict
    """
    while True:
        response = _get_checkins(user_id, params)
        for checkin_response in response['response']['checkins']['items']:
            save(checkin_response)
        # If response count is less than limit we're out of new checkins to stockpile
        if len(response['response']['checkins']['items']) < limit:
            break
        # If not, get next page of checkins
        params['offset'] += limit


def _get_checkins(user, params):
    """

    :param user: Foursquare user to get checkins for.
    :type user: str
    :param params: API request parameters.
    :type params: dict
    :return: API response.
    :rtype: dict
    """
    response = api.users.checkins(USER_ID=user, params=params)
    return response


def save(response):
    """

    :param response: Checkin data from API response.
    :type response: dict
    """
    checkin = Checkin(**response)
    #TODO: Implement a base method to check for existing records and update or inset
    db.add(checkin)
    try:
        venue = Venue(**response['venue'])
        checkin.venue = venue
        db.add(venue)
        for category_response in response['venue']['categories']:
            category = Category(**category_response)
            db.add(category)
            venue.categories.append(category)
    except KeyError:
        pass
    db.flush()


def _get_last_timestamp(user_id):
    """

    :param user_id: Foursquare user to get checkins for.
    :type user_id: str
    :return: Timestamp of last recorded checkin.
    :rtype: int
    """
    last_checkin = db.query(Checkin).filter(Checkin.user_id == user_id).order_by(Checkin.createdAt).first()
    if last_checkin:
        return last_checkin.createdAt
    else:
        return None
