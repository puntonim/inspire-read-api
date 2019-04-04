
# INSPIRE-READ-API

**This is an unfinished POC - Proof of concept**

Inspire-next collects data that include relationships, for instance: author <-> publication <-> citation.
Unfortunately Inspire-next data model was poorly designed using one non-relational field: the
effect is that querying relationships is utterly complex and costly.

This POC is an attempt of:
 - encapsulate all queries in a single layer
 - add a layer on top of the DB model layer in order to provide relationship-like queries
 - this new layer does not query the DB via SQL (unlike the DB model layer), but it
   queries the JSON model (stored in the non-relational field) using an object-oriented
   interface (similarly to an ORM)
 - add a RESTful webservice to expose an API to enable relationship-like requests
 - use Django instead of Flask+SQLAlchemy to test if Django's simpler ORM (compared to SQLAlchemy)
   is a better fit
 - the whole project is limited to READ-ONLY ops on the database. Any write should be
   considered non-compatible with Inspire-next because of the different toolset

Results so far are great: the idea of the new layer simplifies all queries and encapsulates
all query logic,
performance of the REST API are great even on a db with a size similar to the prod db,
and Django ORM provides a clar and simple interface (thanks to its implicit session handling).

