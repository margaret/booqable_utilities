#!/usr/bin/python3

import json
import os

import requests

class Booqable:
	def __init__(self, company_slug, api_key):
		self.API_VERSION = "1"
		self.ENDPOINT_BASE = "https://{0}.booqable.com/api/{1}/".format(company_slug, self.API_VERSION)
		self.API_KEY = api_key

		self.session = requests.Session()
		self._set_session()

		self.products_data = dict()
		self.products_by_name = dict()

	def _set_session(self):
		print("setting up session")
		response = self.session.get(self.ENDPOINT_BASE+"customers", params={"api_key": self.API_KEY})
		print(response)

	def get(self, url, *args, **kwargs):
		return self.session.get(url, *args, **kwargs)

	def get_all_products(self, refresh=False):
		"""https://developers.booqable.com/#list-all-product-groups
		"""
		if not self.products_data or refresh:
			print("getting all product_groups")
			url = self.ENDPOINT_BASE + "product_groups"
			response = self.get(url)
			response.raise_for_status()
			self.products_data = response.json()
			self._group_products_by_name()
		return self.products_data

	def _group_products_by_name(self):
		if not self.products_data:
			raise ValueError("No product data. Please call Booqable.get_all_products")
		# products_data is a list of dict
		print(self.products_data)
		for product in self.products_data['product_groups']:
			self.products_by_name[product['name']] = product

	def product(self, product):
		return self.products_by_name[product]



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
	# 		    "updated_at": "2023-03-07T02:42:14.609Z",
	# 		    "created_at": "2023-03-07T02:42:14.609Z",
	# 		    "owner_id": "5d9d5871-8897-4448-aa67-776ef575f570",
	# 		    "owner_type": "Item",
	# 		    "coordinates": {
	# 		      "x": 0,
	# 		      "y": 0
	# 		    },
	# 		    "position": 1,
	# 		    "preview": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+AjIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCAAZABkDAREAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAAAgQAAQMF/8QAIBABAAICAgIDAQAAAAAAAAAAAQACAxEEMRJBIVGRsf/EABcBAAMBAAAAAAAAAAAAAAAAAAABAgP/xAAaEQEBAAMBAQAAAAAAAAAAAAAAAQIRMSES/9oADAMBAAIRAxEAPwDqcm9seFtTvZ6iy4rGbpWt+Q5KeTYGwdamc+l3Wj81ZJAMeU6413W9RXh49LPKL6VRHYa6Zncq0mMM8fM5R2a1LxtvUZTTaUkGajfDap2kVOeUDjL8hfrxf7Fr09+DpVMmRT4U1+RzpXg4ySAV7YBcAkA//9k=",
	# 		    "original_url": "https://cdn3.booqable.com/uploads/ea0edc76d45549c86bd654a4096029f3/photo/photo/cad19987-f95a-4b70-9b8e-785a3e2e1afb/photo.png",
	# 		    "large_url": "https://cdn3.booqable.com/uploads/ea0edc76d45549c86bd654a4096029f3/photo/photo/cad19987-f95a-4b70-9b8e-785a3e2e1afb/large_photo.jpg"		
	]




