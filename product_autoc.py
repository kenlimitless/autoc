#!/usr/bin/env python
import json
import webapp2

from google.appengine.ext import ndb

class BBProduct(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    name_lower = ndb.StringProperty(indexed=True)

class BBProductSearch(webapp2.RequestHandler):
    def get(self):
        def to_name(p):
            return p.name

        products = self._search_by_name(self.request.get('prefix'))
        print("products", products)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(map(to_name, products)))

    def _search_by_name(self, prefix):
        prefix_lower = prefix.lower()
        prefix_upper = prefix_lower + u'\ufffd'
        print("prefix_lower", prefix_lower)
        print("prefix_upper", prefix_upper)
        products_query = BBProduct.query().filter(BBProduct.name_lower >= prefix_lower).filter(BBProduct.name_lower < prefix_upper)
        products = products_query.fetch(10)
        return products

app = webapp2.WSGIApplication([
    ('/product/', BBProductSearch)
], debug=True)
