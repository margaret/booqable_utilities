#!/usr/bin/python3

import json, os

from booqable import Booqable

def printjson(j):
  print(json.dumps(j, indent=2))

if __name__ == "__main__":
  bq = Booqable("ideas-events-and-rentals", os.environ.get("API_KEY", ""))
  
  gillian_sofa_id = "ed32a654-3c04-4469-b7bd-7f87455c3e86"
  
  gillian_sofa = bq.get_product_group_by_id(gillian_sofa_id)
  printjson(gillian_sofa)

  printjson(bq.get_categories_of_product_group(gillian_sofa_id))

  printjson(bq.get(bq.ENDPOINT_BASE + "api/3/category_items").json())