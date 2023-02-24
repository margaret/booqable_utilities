#!/usr/bin/python3

import time
import json

import requests


PRODUCT_PAGE_URL = "https://www.ideas-events.com/equipment.asp?action=category&key={}"

ERROR_TEXT = """No Items Found - Possible query error - please report this error to the store."""

IMAGE_DIR = 'src="itemimages/'
IMAGE_URL_BASE = "https://www.ideas-events.com/itemimages/"

COMMENT_TAG = "por-item-detail-comments"

ITEM_DETAIL_TAG = "por-item-detail-name"

# Utility Functions

def parse_raw_keys(text):
	return [k.strip() for k in text.split()]


def get_product_page_source(product_key):
	product_url = PRODUCT_PAGE_URL.format(product_key)
	print(product_url + "\n")
	return requests.get(product_url).text


def product_exists(page_source):
	return ERROR_TEXT not in page_source


def parse_image_filename(src_slug):
	return src_slug.replace(IMAGE_DIR, "").replace('"', "") # remove the trailing double quotation mark


def parse_image_urls(page_source):
	url_lines = []
	for line in page_source.split(): # intentionally splitting by space and not newline
		if IMAGE_DIR in line:
			image_filename = parse_image_filename(line)
			url_lines.append(IMAGE_URL_BASE + image_filename)
	return url_lines


def parse_comments(page_source):
	comments = list()
	for line in page_source.split("\n"):
		if COMMENT_TAG in line:
			# Remove carriage return character because it can mess up text display.
			for txt in line.replace("\r", "").split("<li>"):
				# If it starts with an opening tag, then it's the junk before the comment block.
				if not txt.startswith("<"):
					# It appears that the closing tag </li> is not applied consistently.
					comments.append(txt.split("<", 1)[0])
	return "\n".join(comments)


def parse_product_name(page_source):
	for line in page_source.split("\n"):
		if ITEM_DETAIL_TAG in line:
			# get the text before "</h1>"
			# then from that text get everything after "<h1>"
			# then remove carriage return character
			return line.split("</h1>", 1)[0].split("<h1>", 1)[1].replace("\r", "")


def parse_product_category(page_source):
	"""
	The html looks like this but without newlines:

	</div><div id='mainpage'><!--#POR#M#B-->
	<table  border='0' cellpadding='4' cellspacing='0'>
	<tr>
	<td align='left' valign='middle' colspan='2'>
	<h2 style='margin-left: 0px;'><a class="por-item-detail-name" href='equipment.asp?action=category&amp;category=36'>Candlesticks & Candelabras</a></h2><h1>Vienna Stand - Large</h1>
	</td>
	</tr>
	<tr bgcolor=''><td class='detailedviewrow'></td>
	"""
	for line in page_source.split("\n"):
		if ITEM_DETAIL_TAG in line:
			# remove carriage returns
			# get the text after "<a "
			# from that text get everything before "</a>"
			# then everything after ">"
			return line.replace("\r", "").split("<a ", 1)[1].split("</a>", 1)[0].split(">", 1)[1]


def import_keys(keys_filename):
	with open(keys_filename) as f:
		keys = parse_raw_keys(f.read())
	return keys


def save_product_info(product_dict, filename):
	"""Write product_dict to filename as json
	"""
	with open(filename, "w") as f:
		f.write(json.dumps(product_dict))


# Test run

def check():
	# ASDR1 is the chinese dragon, has 1 image and a 3-line comment
	# CAVI1 has multiple images
	# VAZO2 does not exist on website
	TEST_PRODUCT_KEYS = """VOMC1
ASDR1
CAVI1
VAZO2
"""
	product_keys = parse_raw_keys(TEST_PRODUCT_KEYS)

	processed_keys = []
	nonexistent_products = []

	product_data = dict()
	for i, product_key in enumerate(product_keys):
		print("=== Getting page {0}/{1}: {2} ===\n".format(i+1, len(product_keys), product_key))
		page_source = get_product_page_source(product_key)
		if product_exists(page_source):
			product_data[product_key] = dict()
			print("\nPRODUCT NAME")
			product_name = parse_product_name(page_source)
			print(product_name)
			product_data[product_key]["name"] = product_name
			print("\nCATEGORY")
			product_category = parse_product_category(page_source)
			print(product_category)
			product_data[product_key]["category"] = product_category
			print("\nIMAGES")
			image_urls = parse_image_urls(page_source)
			print("\n".join(image_urls))
			product_data[product_key]["image_urls"] = image_urls
			print("\nDESCRIPTION")
			product_description = parse_comments(page_source)
			print(product_description)
			product_data[product_key]["description"] = product_description
			processed_keys.append(product_key)
		else:
			print("Product page does not exist for {}\n".format(product_key))
			nonexistent_products.append(product_key)

		# There probably isn't rate limiting on our site, but let's be polite
		time.sleep(2)
		print("\n")


	print(json.dumps(product_data, indent=2))
	save_product_info(product_data, "test_data.json")
	
	print("\nNot found on website:")
	print("\n".join(nonexistent_products))


	print("\bFinished!\n")



if __name__ == "__main__":
	check()

