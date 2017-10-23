#!/usr/bin/env python
import json
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import memcache

class BBProduct(ndb.Model):
    name = ndb.StringProperty(indexed=False)
    name_lower = ndb.StringProperty(indexed=True)

class BBProductSearch(webapp2.RequestHandler):
    def get(self):
        def to_name(p):
            return p.name

        prefix = self.request.get('prefix')
        products = memcache.get(self._get_memcache_search_key(prefix)) or self._search_by_name(prefix)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(map(to_name, products)))

    def _search_by_name(self, prefix):
        prefix_left = prefix.lower()
        prefix_right = prefix_left + u'\ufffd'
        products_query = BBProduct.query().filter(BBProduct.name_lower >= prefix_left).filter(BBProduct.name_lower < prefix_right)
        products = products_query.fetch(10)
        memcache.set(self._get_memcache_search_key(prefix), products)
        return products

    def _get_memcache_search_key(self, prefix):
        return 'product:search:%s' % prefix

app = webapp2.WSGIApplication([
    ('/product/', BBProductSearch)
], debug=True)
