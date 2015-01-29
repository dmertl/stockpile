# stockpile

A framework for creating a local copy of API data and keeping it up to date.

## Planning

Simplest form of command usage. Provide an adapter object for the API entity we want to retrieve and store. Provide a
param object that filters API request to only what we're interested in (dmertl's checkins).

    from stockpile import stockpile, Foursquare
    stockpile(Foursquare.Checkin, {'user': 'dmertl'})
    
The adapter object needs to provide a mapping from API response to DB model data (SQLAlchemy?).

The adapter object needs to provide a method for querying the API.

The adapter object needs to convert the provided parameters into API query params.

The adapter object needs to provide a method for finding the latest record in the DB and adjusting API query params to 
only get more recent records. If no records are found, start from the beginning. 

The adapter object needs to provide a method for handling pagination from the API response.

The adapter object needs to provide a method for saving related entities (checkin and checkin venu, category, etc.) 
Related entities may require secondary API queries. Should create adapters for every desired entity in API.

The adapter object should return the maximum number of results from the API query if option is available.

The adapter object needs to define if the entity is temporal or reference. Temporal entities should be kept up to date 
by querying for any new entities any time a stockpile is requested. Reference entities are not kept up to date. They are
normaly only created when linked from a temporal entity. Reference entities must have a unique ID. Temporal focuses on 
inserting new entites and keeping the list up to date. Reference entities focus on keeping their data up to date, but 
rarely creating new entities.

Update temporal is like INSERT INTO temporal WHERE created >= $last_timestamp.
 
Update reference is like UPDATE IF EXISTS ELSE INSERT INTO temporal WHERE id = $reference_id

Think about support for push based APIs like Foursquare's real time API: https://developer.foursquare.com/overview/realtime

### Temporal Entities

Main focus of stockpile. Entities created over time and must be cached locally. Query API for new entities and insert 
into local cache.

### Reference Entities

Used as reference data from a temporal entity. Requires a unique identifier. Created if doesn't exist. Updated if 
exists.

## Adapters

### Framework Responsibilities

- Abstract stockpile method (main method)
- Provide simple conversion to SQL (API fields directly to SQL fields)
- Outline for time params
- Outline for pagination
- Detect duplicate entities (don't insert duplicates)

### Individual API Responsibilities

- API client
- Handle standardized options, e.g. if pagination is standardized across all entities

### Individual Entity Responsibilities

- Convert API response into SQL insert query.
- Handle API pagination
 - Make request for next page
 - Detect if more pages required
- Handle API time params
- Handle getting newest timestamp from local DB
- Handle reference entities

## Foursquare Checkins Example

API Query Sample:

    https://api.foursquare.com/v2/users/self/checkins?offset=100&afterTimestamp=1279044824&limit=250

Find date of latest checkin in local database.

    SELECT MAX(createdAt) FROM checkins

Query for new checkins:

    https://api.foursquare.com/v2/users/self/checkins?afterTimestamp=1279044824&limit=250
    
Check if next page is required:

    return len(response.checkins) == 250
    
Get next page (requires previous query's params):

    https://api.foursquare.com/v2/users/self/checkins?afterTimestamp=1279044824&limit=250&offset=250
    
Convert to local DB model:

    return model.fromArray({ key: response[key] for key in self.whitelist })

Save references (who handles check if id exists then save/update?). Does refEntity need to know if it's primary entity? 
Need to handle saving multiple levels of references, but maybe that could be done in main entity. Model adapter could 
just convert data in table.

    self.save(refEntity.fromResponse(response[refentity]))

### Foursquare.Checkin

Handles stockpiling foursquare checkins. Makes API query, handles timestamps, pagination. Creates checkins and any 
related records. Chooses what depth of related records are created.

Naming convention? Checkin, CheckinStockpile?

### Foursquare.model.checkin

SQLAlchemy model for a foursquare checkin. Can convert from foursquare response to model data using field whitelist.

### Foursquare.model.venue

SQLAlchemy model for a foursquare venue. Can convert from foursquare response to model data using field whitelist.

## TODO

- Add setup.py listing to create proper python package
 - SQLAlchemy
