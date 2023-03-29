#!/usr/bin/python3

import csv
# could definitely also just use pandas for csv munging if you have it already
# but I didn't want to deal with installing stuff / environment setup on the
# work computers
import json
import os

from collections import defaultdict

from booqable import (
  Booqable,
  extract_categories,
  extract_product_properties,
  extract_product_group_photo_urls
)


def printjson(j):
  print(json.dumps(j, indent=2))


def collect_all_product_group_info(custom_fields, category_map):
  product_group_data = {
  }


def sandbox():
  bq = Booqable("ideas-events-and-rentals", os.environ.get("API_KEY", ""))
  
  gillian_sofa_id = "ed32a654-3c04-4469-b7bd-7f87455c3e86"
  
  printjson(bq.get_product_group_by_id(gillian_sofa_id))
  
  printjson(bq.get_categories_of_product_group(gillian_sofa_id))


if __name__ == "__main__":
  sandbox()  
  
  
  
  
