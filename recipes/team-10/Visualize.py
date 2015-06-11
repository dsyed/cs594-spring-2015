"""
Requires html5lib (pip install html5lib)

@author: Daanyaal, Dustin, Marvin
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json

forJson = {'name': 'Vulnerabilities', 'children': []}


def getVendors(collection, field):
    vendor_names_cursor = collection.find({}, {field: 1})
    vendor_names_list = []
    for vendor in vendor_names_cursor.distinct(field):
        vendor_names_list.append(str(vendor))
        vendor_dict = {'name': str(vendor), 'children': []}
        getProducts(collection, vendor, vendor_dict)
        forJson['children'].append(vendor_dict)
    # print vendor_names_list


# get products specific vendor
def getProducts(collection, vendor, vendor_dict):
    product_list_cursor = collection.find(
        {'Vendor': vendor}, {'Product': 1})
    product_list = []
    for product in product_list_cursor.distinct('Product'):
        product_list.append(str(product))
        product_dict = {
            'name': str(product),
            'children': []
        }
        getVersions(collection, vendor, product, product_dict)
        vendor_dict['children'].append(product_dict)
    # print product_list


# versions for each product
def getVersions(collection, vendor, product, product_dict):
    version_list_cursor = collection.find(
        {'Vendor': vendor, 'Product': product}, {'Version': 1})
    version_list = []
    for version in version_list_cursor.distinct('Version'):
        version_list.append(str(version))
        product_dict['children'].append({
            'name': str(product) + ' -- ' + str(version),
            'size': 1
        })
    # print version_list


def getJson(collection):
    getVendors(collection, 'Vendor')
    the_json = json.dumps(forJson, indent=2)
    # the_json = json.dumps(forJson)
    print the_json
    return the_json

if __name__ == '__main__':
    client = MongoClient()
    database = client.bigdata
    getJson(database.vendors)
