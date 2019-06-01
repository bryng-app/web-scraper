def get_all_products_with_category(soup):
  categories_count = [
    { 'name': 'Backwaren', 'amount': 28 },
    { 'name': 'Brot­aufstrich & Cerealien', 'amount': 16 },
    { 'name': 'Drogerie­artikel', 'amount': 54 },
    { 'name': 'Fertig­produkte', 'amount': 8 },
    { 'name': 'Fette & Öle','amount': 9 },
    { 'name': 'Fisch & Meeres­früchte', 'amount': 22 },
    { 'name': 'Fleisch- & Wurst­waren', 'amount': 14 },
    { 'name': 'Gesundheit & Wellness', 'amount': 2 },
    { 'name': 'Getränke, alkoholfrei', 'amount': 20 },
    { 'name': 'Getränke, alkohol­haltig', 'amount': 13 },
    { 'name': 'Gewürze, Backzutaten', 'amount': 15 },
    { 'name': 'Käse', 'amount': 15 },
    { 'name': 'Kaffee, Tee & Instant­getränke', 'amount': 5 },
    { 'name': 'Molkerei­produkte, Eis & Eier', 'amount': 30 },
    { 'name': 'Nudeln & Reis', 'amount': 5 },
    { 'name': 'Obst, Gemüse & Nüsse', 'amount': 1 },
    { 'name': 'Salate & Feinkost', 'amount': 7 },
    { 'name': 'Fertig­saucen', 'amount': 5 },
    { 'name': 'Rand­sortiment', 'amount': 8 },
    { 'name': 'Süß­waren & Snacks', 'amount': 43 },
    { 'name': 'Tier­nahrung', 'amount': 2 },
  ]

  product_count = 1
  category_index = 0
  products = {}
  categories_products = {}
  for tr in soup.find_all('tr', { 'valign': 'top' }):
    if categories_count[category_index]['amount'] != product_count:
      product_count += 1
    else:
      product_count = 1
      categories_products.update({
        categories_count[category_index]['name'].replace('\xad', ''): products
      })
      products = {}
      if category_index != 20:
        category_index += 1

    # find product name and weight data
    th = [th.text for th in tr.find_all('th')]
    # find product prices
    td = [td.text.strip().replace('\r', '').replace('\n', '') for td in tr.find_all('td')]

    # get the product name
    product_name = th[0].split("(")[0].replace('Ã¼', 'ü').replace('Ã¶', 'ö').replace('Ã¤', 'ä')
    
    # get the weight
    product_weight = th[0].split('(')[1].replace(')', '')

    # get the prices
    product_prices = [('' if not price.split('€')[0] else price.split('€')[0] + '€') for price in td]
    weight_prices = ['€'.join(price.split('€')[1:]) for price in td]

    # construct prices dictionary
    prices = []
    for i in range(len(product_prices)):
      price_dict = {
        'product_price': product_prices[i],
        'weight_price': weight_prices[i]
      }
      prices.append(price_dict)

    # construct the dictionary
    product_dict = { 
      product_name: {
        'prices': prices[0],
        'weight': product_weight
      }
    }

    products.update(product_dict)
  return categories_products


"""def get_all_products(soup):
  products = {}
  for tr in soup.find_all('tr', { 'valign': 'top' }):
    # find product name and weight data
    th = [th.text for th in tr.find_all('th')]
    # find product prices
    td = [td.text.strip().replace('\r', '').replace('\n', '') for td in tr.find_all('td')]

    # get the product name
    product_name = th[0].split("(")[0].replace('Ã¼', 'ü').replace('Ã¶', 'ö').replace('Ã¤', 'ä')
    
    # get the weight
    product_weight = th[0].split('(')[1].replace(')', '')

    # get the prices
    product_prices = [('' if not price.split('€')[0] else price.split('€')[0] + '€') for price in td]
    weight_prices = ['€'.join(price.split('€')[1:]) for price in td]

    # construct prices dictionary
    prices = []
    for i in range(len(product_prices)):
      price_dict = {
        'product_price': product_prices[i],
        'weight_price': weight_prices[i]
      }
      prices.append(price_dict)

    # construct the dictionary
    product_dict = { 
      product_name: {
        'prices': prices,
        'weight': product_weight
      }
    }

    products.update(product_dict)
  return products"""


def store_product(name, product_price, weight, store_name, category_name, mongo):
  mongodb = mongo['bryng-test']
  product_collection = mongodb['products']
  price_str = product_price.split('€')[0]
  if not price_str:
    price_str = 0.0
  price = float(price_str)

  if price != 0.0:
    product_collection.update(
      { 'name': name, 'image': '', 'price': price, 'weight': weight, 'storeName': store_name, 'categoryName': category_name },
      { 'name': name, 'image': '', 'price': price, 'weight': weight, 'storeName': store_name, 'categoryName': category_name },
      upsert=True
    )
