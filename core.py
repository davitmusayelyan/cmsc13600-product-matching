'''
The core module sets up the data structures and 
and references for this programming assignment.
'''

import platform
import csv

#defines an iterator over the catalogs
class Catalog():

    def __init__(self, filename):
      self.filename = filename

    def __iter__(self):
      f = open(self.filename, 'r', encoding = "ISO-8859-1")
      self.reader = csv.reader(f, delimiter=',', quotechar='"')
      next(self.reader)
      return self

    def __next__(self):
      row = next(self.reader)
      return {'id': row[0],
               'title': row[1],
               'description': row[2],
               'mfg': row[3],
               'price': row[4]
              }

def google_catalog():
    return Catalog('GoogleProducts.csv')

def amazon_catalog():
    return Catalog('Amazon.csv')
