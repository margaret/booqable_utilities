#!/usr/bin/python3

import json
import os

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

    self.product_groups_data = dict()
    self.product_groups_by_name = dict()

  def _set_session(self):
    print("Setting up session")
    response = self.session.get(self.ENDPOINT_BASE+"customers", params={"api_key": self.API_KEY})
    print(response)

  def get(self, url, *args, **kwargs):
    return self.session.get(url, *args, **kwargs)
  
  #####################################################################################################################
  #
  # Unless otherwise noted, the requests below use the version of the API that is used by the current production
  # version of the Booqable webapp as determined by inspecting network requests
  #
  #####################################################################################################################

  def _extract_categories(categories_response_json):
    categories = []
    for category_item in categories_response_json["included"]:
      categories.append({
        "name": category_item["attributes"]["name"],
        "type": "subcategory" if category_item["attributes"]["parent_id"] else "category"
      })
    return categories
  
  def get_categories_of_product_group(product_group_id):
    response = self.session.get(self.ENDPOINT_BASE + \
      "api/3/category_items?include=category&filter[item_id]={}&page[per]=1000".format(product_group_id)
    )
    return self._extract_categories(response.json())

  def _extract_photo_urls(photos_response_json):
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

  def get_photos_of_product_group(product_group_id):
    response = self.session.get(self.ENDPOINT_BASE + \
      "api/boomerang/photos?filter[owner_id]={}&filter[owner_type]=ProductGroup".format(product_group_id))

  def get_product_group_by_id(product_group_id):
    response = self.session.get(self.ENDPOINT_BASE + \
      "api/v3/product_groups/" + product_group_id)

  def _extract_product_properties(default_properties):
    """Return list of names of properties associated with Products"""
    product_properties = []
    for prop in default_properties["default_properties"]:
      if prop["owner_type"] == "Product":
        product_properties.append(prop["name"])

  def get_all_custom_fields():
    response = self.session.get(self.ENDPOINT_BASE + \
       "api/2/default_properties?page[per]=1000"
    )

  ### old methods, these don't use the same API that the production app does

  def get_all_product_groups(self, refresh=False):
    """https://developers.booqable.com/#list-all-product-groups
    Returns dict of json directly from the API response
     {
      "product_groups": [list of product dict],
      "meta": {
        "total_count": int,
        "tag_list": {
          "a tag": int,
          "another tag": int
        },
        "status": {
          "active": int,
          "bulk": int,
          "has_variations": int
        }
      }
     }
    """
    if not self.products_groups_data or refresh:
      url = self.ENDPOINT_BASE + "api/1/product_groups"
      response = self.get(url)
      response.raise_for_status()
      self.products_data = response.json()
      self._store_product_groups_by_name()
    return self.product_groups_data

  def _store_product_groups_by_name(self):
    if not self.product_groups_data:
      raise ValueError("No product data. Please call Booqable.get_all_products")
    for product in self.product_groups_data['product_groups']:
      self.product_groups_by_name[product['name']] = product

  def product(self, product):
    return self.product_groups_by_name[product]



if __name__ == "__main__":
  bq = Booqable("ideas-events-and-rentals", os.environ.get("API_KEY", ""))
  bq.get_all_products()
  chair = bq.product("Generic Demo Chair")
  fields = [
      "id",
        "updated_at",
        "created_at",
        ## dict
        # "properties_attributes",
      #   "location": "Warehouse",
      #   "aisle": "NCC-1701",
      #   "vendor": "Emojipedia",
      #   "purchase_price": "$50.00"
        "name",
        "slug",
        "sku",
        "lag_time",
        "lead_time",
        "always_available",
        "trackable",
        "archived",
        "archived_at",
        "extra_information",
        "photo_url",
        "allow_shortage",
        "shortage_limit",
        "sorting_weight",
        "description",
        "show_in_store",
        "base_price_in_cents",
        "price_wrapper_id",
        "price_type",
        "price_period",
        "tax_category_id",
        "flat_fee_price_in_cents",
        "structure_price_in_cents",
        "deposit_in_cents",
        "discountable",
        "taxable",
        # "custom_fields",
            # "location": "Warehouse",
        # "aisle": "NCC-1701",
        # "vendor": "Emojipedia",
        # "purchase_price": "$50.00"
        "stock_count",
        "has_variations",
        "variation_fields",
        "stock_item_properties",
        # "tags",
          # [
      #   "dining chairs"
      # ],
        "product_type",
        "tracking_type",
        "price_ruleset_id",
        "base_price_as_decimal",
        "base_price",
        "flat_fee_price_as_decimal",
        "flat_fee_price",
        "structure_price_as_decimal",
        "structure_price",
        "deposit_as_decimal",
        "deposit",
        # "photo",
    #             "id": "cad19987-f95a-4b70-9b8e-785a3e2e1afb",
  #         "updated_at": "2023-03-07T02:42:14.609Z",
  #         "created_at": "2023-03-07T02:42:14.609Z",
  #         "owner_id": "5d9d5871-8897-4448-aa67-776ef575f570",
  #         "owner_type": "Item",
  #         "coordinates": {
  #           "x": 0,
  #           "y": 0
  #         },
  #         "position": 1,
  #         "preview": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCAAZABkDAREAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAAAgQAAQMF/8QAIBABAAICAgIDAQAAAAAAAAAAAQACAxEEMRJBIVGRsf/EABcBAAMBAAAAAAAAAAAAAAAAAAABAgP/xAAaEQEBAAMBAQAAAAAAAAAAAAAAAQIRMSES/9oADAMBAAIRAxEAPwDqcm9seFtTvZ6iy4rGbpWt+Q5KeTYGwdamc+l3Wj81ZJAMeU6413W9RXh49LPKL6VRHYa6Zncq0mMM8fM5R2a1LxtvUZTTaUkGajfDap2kVOeUDjL8hfrxf7Fr09+DpVMmRT4U1+RzpXg4ySAV7YBcAkA//9k=",
  #         "original_url": "https://cdn3.booqable.com/uploads/ea0edc76d45549c86bd654a4096029f3/photo/photo/cad19987-f95a-4b70-9b8e-785a3e2e1afb/photo.png",
  #         "large_url": "https://cdn3.booqable.com/uploads/ea0edc76d45549c86bd654a4096029f3/photo/photo/cad19987-f95a-4b70-9b8e-785a3e2e1afb/large_photo.jpg"    
  ]




