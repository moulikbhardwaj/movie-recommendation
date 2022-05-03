GET
- /movies/      -- returns list of movies object
  -- Params: limit: limit number of objects returned
- /movies/id/   -- return specific movie
- /movies/id/set-watched/ -- set given movie as watched
- /collections/
  -- Params: ids: array of ids of collections, returns array of objects of the collections
- /casts/
  -- Params: ids: array of ids of casts, returns array of objects of the casts
- /crew/
  -- Params: ids: array of ids of crew, returns array of objects of the crew

- /movies/get-recommendation
- /movies/get-initial-recommendation