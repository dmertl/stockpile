__author__ = 'dmertl'

limit = 250

def stockpile():
    # No params? Always stockpile "self"

    # Find last timestamp for user
    params = {}
    params['createdAt'] = findLastTimestamp()
    params['offset'] = 0
    stockpile_loop(url, params)

# TODO: better name
def stockpile_loop(params):
    while True:
        # Query for checkins
        for checkin_response in response['response']['checkins']['items']:
            save(checkin_response)
        # TODO: potential problem if API doesn't always return limit results even when there's more to find
        if len(response['response']['checkins']['items']) < limit:
            break
        params['offset'] += limit

def save(response):
    checkin = Model.Checkin.fromResponse(response)
    # Do we need to save venue separately from checkin? Or will SQL alchemy handle it for us?
    checkin.venue = Model.Venue.fromResponse(response['venue'])
    categories = []
    for category_response in response['categories']:
        categories += Model.Category.fromResponse(category_response)
    venue.categories = categories
    # Method for save/update
    self._save(checkin)

def add_time(params, timestamp):
    params['createdAt'] = timestamp

def add_next_page(params, previous_params):
    if previous_params['offset']:
        params['offset'] += limit
    else:
        params['offset'] = limit
