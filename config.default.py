settings = {
    "foursquare": {
        # Foursquare Application Client ID
        "client_id": "",
        # Foursquare Application Client Secret
        "client_secret": "",
        # Foursquare Application Redirect URI
        "redirect_uri": "",
        # Connection string for SQLite database to save stockpile in
        "db": "'sqlite:///db/foursquare.sqlite'"
    }
}

debug = {
    "foursquare": {
        # Access token to use when making request to Foursquare API
        "access_token": None
    }
}
