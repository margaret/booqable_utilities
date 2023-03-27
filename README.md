# POR Migration
 
Scripts for extracting data out of Point of Rental via the website, since the database table exporter doesn't actually export all the tables (or any images).

Only requirement besides stdlib currently is the requests library (was tested with 2.28.2)

# Booqable API wrapper

Python3 wrapper for Booqable API. This is not a complete library to interface with their APIs. I'm just adding to it as I need to access various pieces of information. It's "productionized" insofar as I want to be able to update it as Booqable makes non-backwards-compatible changes but it is not intended to be used in any production applications.

## API Versions

Booqable uses a mix of v2, v3, and boomerang APIs in production. API v1 still seems to work and is still what the official documentation references, but I don't think it's currently maintained.

There doesn't appear to be any public facing documentation on the support timeline or endpoints for each of the API versions

## API authentication

To get your API key, go to your `User settings` page when logged into Booqable. This is at https://your-company.booqable.com/employees/current

All 4 of the APIs appear to use the same session. [Authentication still works as described in the v1 documentation](https://developers.booqable.com/#authentication).
