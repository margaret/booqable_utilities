#!/usr/bin/python3

import requests


class Booqable:
  def __init__(self, company_slug, api_key):
    ###############################################################################################
    # Booqable's production webapp appears to use a mix of api/2/ api/boomerang/ and api/3/
    # api/1/ also works but I'm not sure it's still used for anything in production
    # Thankfully(?) they all seem to accept the same session cookies
    ###############################################################################################

    self.ENDPOINT_BASE = "https://{0}.booqable.com/".format(company_slug)
    self.API_KEY = api_key

    self.session = requests.Session()
    self._set_session()

  def _set_session(self):
    response = self.session.get(self.ENDPOINT_BASE + \
      "api/1/customers", params={"api_key": self.API_KEY}
    )
    response.raise_for_status()

  def get(self, endpoint, *args, **kwargs):
    response = self.session.get(self.ENDPOINT_BASE + endpoint, *args, **kwargs)
    response.raise_for_status()
    return response
  
  #################################################################################################
  # Unless otherwise noted, the requests below use the version of the API that is used by the 
  # current production version of the Booqable webapp as determined by inspecting network requests
  #################################################################################################
  
  def get_all_custom_fields(self):
    """Get the custom fields, i.e. the fields/properties you can change from
    https://help.booqable.com/en/articles/2170699-adding-custom-fields-to-customers-orders-and-products
    """
    return self.get(
       "api/2/default_properties?page[per]=1000"
    ).json()

  def get_categories_of_product_group(self, product_group_id):
    return self.get(
      f"api/3/category_items?include=category&filter[item_id]={product_group_id}&page[per]=1000"
    ).json()

  def get_photos_of_product_group(self, product_group_id):
    return self.get(
      f"api/boomerang/photos?filter[owner_id]={product_group_id}&filter[owner_type]=ProductGroup"
    ).json()

  def get_product_group_by_id(self, product_group_id):
    return self.get(
      f"api/3/product_groups/{product_group_id}"
    ).json()

  def get_product_groups(self):
    response = self.get(
      f"api/boomerang/product_groups?sort=name&filter[archived]=false&page[number]=1&page[size]=500"
    ).json()


#############
# Utilities #
#############

def extract_categories(category_items_json):
  """Returns [str]
  """
  categories = []
  for category_item in category_items_json["included"]:
    categories.append({
    "name": category_item["attributes"]["name"],
    "type": "subcategory" if category_item["attributes"]["parent_id"] else "category"
    })
  return categories


def extract_product_properties(default_properties_json):
  """Returns [str]
  Properties (custom fields) associated with Products (not Clients or Orders)
  """
  product_properties = []
  for prop in default_properties_json["default_properties"]:
    if prop["owner_type"] == "Product":
      product_properties.append(prop["name"])


def extract_product_group_photo_urls(photos_json):
  """Returns dict
  
  * Use with get_photos_of_product_group
  * Booqable supports a maximum of 4 photos.
  * Need to confirm if that is per product_group or per product
  """
  photos = {
    "Photo 1": None,
    "Photo 2": None,
    "Photo 3": None,
    "Photo 4": None
  }
  for photo_item in photos_json["data"]:
    photo_key = "Photo {}".format(int(photo_item["attributes"]["position"]) + 1)
    photos[photo_key] = photo_item["attributes"]["original_url"]
  return photos

