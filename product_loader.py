#!/usr/bin/env python

# [START imports]
import json
import webapp2
import urllib2

from google.cloud import datastore

class BBProductDataLoader(object):
    batch_size = 500
    kind = 'BBProduct'
    datastore_client = datastore.Client()

    def load_to_db(self):
        def download_products():
            product_json_url = "https://raw.githubusercontent.com/BestBuyAPIs/open-data-set/master/products.json"
            return urllib2.urlopen(product_json_url)

        def reset_batch():
            batch = self.datastore_client.batch()
            batch.begin()
            return batch

        def add_product_to_batch():
            product_names[bb_product['name']] = True
            batch.put(bb_product)

        def should_commit_batch():
            return count % self.batch_size == 0

        count = 0
        batch = reset_batch()
        product_names=dict()

        for line in download_products():
            bb_product = self._parse_to_product(line)
            if bb_product is None:
                continue
            if bb_product['name'] in product_names:
                print('found duplicate', bb_product['name'])
                # store only one product with the same name
                continue
            add_product_to_batch()
            count += 1
            if not should_commit_batch():
                continue
            print('Storing products to datastore...', count)
            batch.commit()
            batch = reset_batch()

        print('Final Storing products to datastore...', count)
        batch.commit()

    def _parse_to_product(self, line):
        def to_json_line():
            clean_line = line.rstrip()
            if clean_line.startswith('['):
                clean_line = clean_line[1:]
            if clean_line.endswith(']'):
                clean_line = clean_line[:-1]
            if clean_line.endswith(','):
                clean_line = clean_line[:-1]
            return clean_line

        try:
            data = json.loads(to_json_line())
            name = data['name']
            if name is None:
                print('Found product without name', data)
                return None

            product_key = self.datastore_client.key(self.kind, name)
            product = datastore.Entity(key=product_key)
            product['name'] = name
            product['name_lower'] = name.lower()

            return product
        except Exception as ex:
            print('Unable to parse', line, ex)
            return None

def main():
    loader = BBProductDataLoader()
    loader.load_to_db()

if __name__ == "__main__":
    main()