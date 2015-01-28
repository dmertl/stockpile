"""
Stockpile Foursquare checkins.
"""

# TODO: Add foursquare API somewhere in here
# TODO: Need to get database connection info

# TODO: Limit should move into API
limit = 250


def stockpile(user='self'):
    """

    :param user: Foursquare user to stockpile checkins for.
    :type user: str
    """
    params = {
        'afterTimestamp': _get_last_timestamp(),
        'offset': 0
    }
    stockpile_loop(user, params)


def stockpile_loop(user, params):
    """
    TODO: better name

    :param user: Foursquare user to stockpile checkins for.
    :type user: str
    :param params: API request parameters.
    :type params: dict
    """
    while True:
        response = _get_checkins(user, params)
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
    # TODO: Make API call
    pass


def save(response):
    """
    TODO: Link up with SQLAlchemy

    :param response: Checkin data from API response.
    :type response: dict
    """
    checkin = Model.Checkin.fromResponse(response)
    # TODO: Do we need to save venue separately from checkin? Or will SQL alchemy handle it for us?
    checkin.venue = Model.Venue.fromResponse(response['venue'])
    categories = []
    for category_response in response['categories']:
        categories += Model.Category.fromResponse(category_response)
    venue.categories = categories
    # TODO: Implement a shared method for doing insert/update checks


def _get_last_timestamp():
    """

    :return: Timestamp of last recorded checkin.
    :rtype: int
    """
    # TODO: Query database for max createdAt
    pass