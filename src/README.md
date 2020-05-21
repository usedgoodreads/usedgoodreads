# Status Report

Currently two routes are supported. Running the server in the background (`FLASK_APP=app.py flask run --reload`) and changing the good read link like the following:

Initial link
```
https://www.goodreads.com/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
```

API with URLs to different second hand shops by replacing `www.goodreads.com` via `localhost:5000/api/v1`
```
https://localhost:5000/api/v1/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
```

Redirect to booklooker.de search page by replacing `www.goodreads.com` via `localhost:5000`
```
https://localhost:5000/book/show/136251.Harry_Potter_and_the_Deathly_Hallows
```

## API

Current location is `usedgoodreads.com/api/v1/..` for the API. This could be changed to a subdomain `api.usedgoodreads.com`. Maybe the latter version is better.

## Shops

A couple shops are added in the [Flask App](app.py):

- ebay Kleinanzeigen (de)
- Amazon (de)
- booklooker (de)
- rebuy (de)

Currently the search pages of these are added in the API. There are no problems with Amazon and booklooker, since they have an interface to search via ISBN. Rebuy and eBay Kleinanzeigen only support title searches. These need to be sanitized. Additionally all methods should be properly setup via classes and data models.
