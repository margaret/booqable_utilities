#!/usr/bin/python3

import requests


class Booqable:
  def __init__(self, company_slug, api_key):
    ################################################################################################################### 
    # Booqable appears to use a mix of api/2/ api/boomerang/ and api/3/
    # api/1/ also works but I'm not sure it's still used for anything in production
    # Thankfully(?) they all seem to accept the same session cookies
    ###################################################################################################################

    self.ENDPOINT_BASE = "https://{0}.booqable.com/".format(company_slug)
    self.API_KEY = api_key

    self.session = requests.Session()
    self._set_session()

  def _set_session(self):
    print("Setting up session")
    response = self.session.get(self.ENDPOINT_BASE+"api/1/customers", params={"api_key": self.API_KEY})
    print(response)

  def get(self, url, *args, **kwargs):
    response = self.session.get(url, *args, **kwargs)
    response.raise_for_status()
    return response
  
  #####################################################################################################################
  #
  # Unless otherwise noted, the requests below use the version of the API that is used by the current production
  # version of the Booqable webapp as determined by inspecting network requests
  #
  #####################################################################################################################

  def _extract_categories(self, categories_response_json):
    categories = []
    for category_item in categories_response_json["included"]:
      categories.append({
        "name": category_item["attributes"]["name"],
        "type": "subcategory" if category_item["attributes"]["parent_id"] else "category"
      })
    return categories
  
  def get_categories_of_product_group(self, product_group_id):
    response = self.get(self.ENDPOINT_BASE + \
      "api/3/category_items?include=category&filter[item_id]={}&page[per]=1000".format(product_group_id)
    )
    return self._extract_categories(response.json())

  def _extract_photo_urls(self, photos_response_json):
    """Booqable supports a maximum of 4 photos
    Need to confirm if that is per product_group or per product
    """
    photos = {
      "Photo 1": None,
      "Photo 2": None,
      "Photo 3": None,
      "Photo 4": None
    }
    for photo_item in photos_response_json["data"]:
      photo_key = "Photo {}".format(int(photo_item["attributes"]["position"]) + 1)
      photos[photo_key] = photo_item["attributes"]["original_url"]
    return photos

  def get_photos_of_product_group(self, product_group_id):
    return self.get(self.ENDPOINT_BASE + \
      "api/boomerang/photos?filter[owner_id]={}&filter[owner_type]=ProductGroup".format(product_group_id))

  def get_product_group_by_id(self, product_group_id):
    return self.get(self.ENDPOINT_BASE + \
      "api/3/product_groups/" + product_group_id).json()

  def _extract_product_properties(self, default_properties):
    """Return list of names of properties associated with Products"""
    product_properties = []
    for prop in default_properties["default_properties"]:
      if prop["owner_type"] == "Product":
        product_properties.append(prop["name"])

  def get_all_custom_fields(self):
    return self.get(self.ENDPOINT_BASE + \
       "api/2/default_properties?page[per]=1000"
    ).json()


