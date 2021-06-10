import requests
import html5lib
import string
#import pymongo
from bs4 import BeautifulSoup

def extract_url(url):
  if url.find("www.amazon.ca") != -1:
    index = url.find("/dp/")
    if index != -1:
      index2 = index + 14
      url = "https://www.amazon.ca" + url[index:index2]
    else:
      index = url.find("/gp/")
      if index != -1:
        index2 = index + 22
        url = "https://www.amazon.ca" + url[index:index2]
      else:
        url = None
  else:
      url = None
  return url

def get_converted_price(price):
  stripped_price = price.strip("$ ,")
  replaced_price = stripped_price.replace(",", "")
  converted_price = float(replaced_price)

  return converted_price


def get_product_details(url):
  headers = {
    'Host': 'www.amazon.ca',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
  }
  details = {"name": "", "current_price": 0, "original_price": True, "url": ""}
  extracted_url = extract_url(url)
  if extracted_url == "":
    details = None
  else:
    page = requests.get(extracted_url, headers=headers)
    soup = BeautifulSoup(page.content, "html5lib")
    title = soup.find(id="productTitle")
    spans = soup.find_all('span', {'class' : 'priceBlockStrikePriceString a-text-strike'})
    if len(spans) > 0:
      details["original_price"] = spans[0].get_text().strip()
    else:
      details["original_price"] = False

    price = soup.find(id="priceblock_ourprice")

    if title is not None and price is not None:
      details["name"] = title.get_text().strip().translate(string.punctuation)
      details["current_price"] = get_converted_price(price.get_text())
      details["url"] = extracted_url
    else:
      return None
  return details