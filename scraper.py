import requests
import pymongo
from bs4 import BeautifulSoup
from categories import get_all_categories, store_all_categories
from products import store_product, get_all_products_with_category

def get_all_stores():
  grocery_shops = []
  tr = soup.find_all('tr')
  for i in range(len(tr)):
    current_tr = tr[i]
    if i == 0:
      values = [th.text for th in current_tr.find_all('th')]
      grocery_shops = values[1:]
  return grocery_shops


# Connect to mongodb
mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017/')

# get the data
data = requests.get('https://site')

# load data into bs4
soup = BeautifulSoup(data.text, 'html.parser')

# specify data output
grocery_shops = []
products = {}

# get the grocery shops
grocery_shops = get_all_stores()

# Get and store all categories
categories = get_all_categories(soup)
store_all_categories(categories, mongo)

# get all products with category
products = get_all_products_with_category(soup)
print(products)

store_index = 0
store_name = 'aldi_sued'
for category in categories:
  for product in products[category]:
    prices = products[category][product]['prices']
    product_price = prices['product_price']
    weight = products[category][product]['weight'].replace('ue', 'ü')
    
    store_product(product, product_price, weight, store_name, category, mongo)

# for product in products:
  # prices = products[product]['prices']
  # product_price = prices[store_index]['product_price']
  # weight_price = prices[store_index]['weight_price']
  
  # store_product(product, product_price, weight_price, store_name, mongo)
