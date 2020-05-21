
# Used Books

A website for getting second hand version of books at
[GoodReads](https://www.goodreads.com/api) (GR).

## Features

- Search books from `www.goodreads.com` by adding `used` at the front of the link i.e. `www.usedgoodreads.com`.
- Search translations of books using subdomains like `de.usedgoodreads.com` for German literature or `fr.usedgoodreads.com` for French literature.


## Frontend

Imitate the same frontend interface to the user as GR. The user simply
has to edit the URL from `www.goodreads.com` to `www.usedgoodreads.com`
and the available information is being shown to the user. Since GR is
mostly for English literature, this should be the default search engine.
Translations of the book (e.g. German, French) should be also available
for search. One option is to use subdomains (e.g.
`de.usedgoodreads.com`, `fr.usedgoodreads.com`) for searching
translation of the books.

> - [ ] Analyse URL structure of GR
> - [ ] Search for edge cases
> - [ ] Find translations of a single book, based on ISBN from GR

## Backend

The starting point is the information gathered by the GR API. From there different second hand shops are queried (either on-the-fly or db-supported).

### Shops
There are two types of second hand shops:

- Aggregators <br>
These are websites where individuals can put their second hand books up for sale. These websites need to be scraped/queried and the indiviudal sellers identified.
- Sellers <br>
These are the actual sellers of the books. They can be individuals or cooperations. Most of these might not even have a website and use only Aggregators to sell their books (e.g.[booklooker](http://www.booklooker.de)).

> - [ ] Identify aggregators
>   - [ ] [eBay Kleinanzeigen DE](http://www.kleinanzeigen.ebay.de)
>   - [ ] [Booklooker.de](http://www.booklooker.de)
>   - [ ] [Amazon Used Sellers](http://www.amazon.de)
> - [ ] Individual sellers
>   - [ ] [rebuy.de](http://www.rebuy.de)

## Datamodel
There are three objects which need to be modeled:

- Book <br> 
A single book. Ideally coherent with the model used by GR.
- AggregateShop <br> 
An entity selling books online with individuals or companies in the backend.
- IndividualShop <br> 
Actual individual selling the product. This can be the AggregateShop itself or another seller.

## API
The API used can be different from the one used by GR.

## RESOURCES

- [\#REST API](20200511150216-rest_api.org)
- [GoodReads API Documentation](https://www.goodreads.com/api)
- [Possible role model :P](https://www.nsfwyoutube.com)
