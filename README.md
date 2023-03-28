# Booqable Utilities

Python scripts to generate a more full report than the built-in CSV export and the custom SCSS used to format documents from the CRM.

Written for Ideas Events & Rentals but should work on any Booqable account.


## Custom CSS for Documents

`document_templates.scss` tracks our custom document CSS.


## Booqable API Wrapper

Python3 wrapper for Booqable API. This is not a complete library to interface with their APIs. I'm just adding to it as I need to access various pieces of information. It's "productionized" insofar as I want to be able to update it as Booqable makes changes on their end, but it is not intended to be used in any production applications.

### API Versions

Booqable uses a mix of `v2`, `v3`, and `boomerang` APIs in production. `v1` still seems to work and is still what the official documentation references, but I don't think it's currently maintained.

There doesn't appear to be any public facing documentation on the support timeline or endpoints for each of the API versions

### API authentication

To get your API key, go to your `User settings` page when logged into Booqable. This is at https://your-company.booqable.com/employees/current

All four of the APIs appear to use the same session. [Authentication still works as described in the v1 documentation](https://developers.booqable.com/#authentication).

### Concepts

Notes to help you get started with the API.

### Products and Product Groups

In Booqable there are `product_groups` and `products`.

All `products` belong to a `product_group`.

If your database is set up so that items are tracked in bulk (i.e. you only track the overall quantity of a product, not which individual items of that product are checked out) then there will only be one `product` in a `product_group`.

If you have variations enabled, each variation will be a separate `product` under a `product_group`.

The "Export" CSV feature on the webapp exports `products`, and the `product_group` id is one of the fields.

### Properties

What the documentation refers to as "Custom Fields" is refered to in the API as `default_properties`. Instances of a property are `properties`.

There are `default_properties` and `properties` for Orders, Products, and Customers. 

If you have 2 custom fields defined on Products and 5 on Orders, when you request `default_properties` through `api/2/default_properties` it would return 7 items. But if you request all the `properties` it will return the properties on every single Product.

### Requirements

Only requirement outside the python standard library is the `requests` library.

This was tested with `requests` 2.28.2 on python 3.9.6 on OSX.
