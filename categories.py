def get_all_categories(soup):
  categories = []
  for h2 in soup.find_all('h2')[:-1]:
    categories.append(h2.text.replace('&amp;', '&').replace('\xad', ''))
  return categories


def store_all_categories(categories, mongo):
  mongodb = mongo['bryng-test']
  category_collection = mongodb['categories']
  for category in categories:
    category_collection.update({ 'name': category }, { 'name': category }, upsert=True)

