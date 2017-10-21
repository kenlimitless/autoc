#!/usr/bin/env python

# [START imports]
import json
import requests

from google.appengine.ext import ndb

# [START BBProduct]
class BBProduct(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    name = ndb.StringProperty(indexed=True)
# [END BBProduct]

class BBProductDataLoader(webapp2.RequestHandler):

    batch_size = 10000

    def get(self):
        url = "https://raw.githubusercontent.com/BestBuyAPIs/open-data-set/master/products.json"
        self._loadToDB(product_json_url)

    def _loadToDB(self, product_json_file):
        resp = requests.get(url)
        products = json.loads(resp.content)
        self._storeProducts(products)

    def _storeProducts(self, products):
        bb_products=[]

        for product in products:
            bb_product_model = BBProduct(name=product['name'])
            bb_products.append(bb_product_model)

            if len(bb_products) < self.batch_size:
                continue

            ndb.put_multi(bb_products)
            bb_products = []

# [START app]
app = webapp2.WSGIApplication([
    ('/', BBProductDataLoader)
], debug=True)
# [END app]
