"""
Script for scraping product info from www.osta.ee.

Running this script from command line will scrape all valid product data from
specified subcategory at https://www.osta.ee.
Category can be specified as first command-line argument.
Category nesting is supported.
Scraped results will be written to a JSON output file.
Output filename can be specified as second command-line argument, default filename
is 'products.json'.
This script runs synchronously and may take several seconds depending on category
size and internet connection.
Minimal user input verification is provided, entering invalid arguments will break
the script.
Depends on: BeautifulSoup4.
"""

from bs4 import BeautifulSoup
import json
import sys
import requests
import urllib.request
import urllib.error


def scrape_product_category(category_url, filename):
    """
    Scrape a specified Osta.ee product category and write results to a JSON file.

    :param category_url: url to osta.ee product category
    :param filename: desired output filename
    """
    print(f"Scraping category at url: {category_url}\n")

    entry_page_object = get_page_object_from_url(category_url)
    page_count = get_sub_page_count(entry_page_object)
    items_per_page = 60

    print(f"Category has roughly {page_count * items_per_page} products:"
          f" {page_count} pages with {items_per_page} products per page\n")
    print(f"Scraping page 1...")

    scraped_products = get_product_list_from_page_object(entry_page_object)

    for page_number in range(2, page_count + 1):
        print(f"Scraping page {page_number}...")
        url = f"{category_url}/page-{page_number}"
        scraped_products += get_product_list_from_page_object(get_page_object_from_url(url))

    print(f"\nScraping done, products scraped: {len(scraped_products)}")
    print(f"\nWriting results to {filename}...")

    write_product_list_to_json_file(scraped_products, filename)

    print(f"Scrape results successfully written to file.")


def get_product_list_from_page_object(page_object):
    """
    Get list of dictionary objects containing product information from page object.

    :param page_object: BeautifulSoup4 page object
    :return:
    """
    product_objects = get_product_objects_from_page(page_object)
    products = []
    for product_object in product_objects:
        product = {
            "title": get_product_title(product_object),
            "price": get_product_price(product_object),
            "img_href": get_product_img_href(product_object)
        }
        products.append(product)
    return products


def get_sub_page_count(page_object) -> int:
    """
    Get number of sub pages in a category from a category page object.

    :param page_object: BeautifulSoup4 page object.
    :return: number of sub pages in category.
    """
    return int(page_object.find("span", {"class": "page-count"}).text)


def get_page_object_from_url(url):
    """
    Get BeautifulSoup4 page object from url.

    :param url: web page url
    :return: BeautifulSoup4 page object representing web page with specified url.
    """
    request = requests.get(url)
    return BeautifulSoup(request.text, "html.parser")


def get_product_objects_from_page(page_object):
    """
    Get sub page-objects containing product information from main page object.

    :param page_object: BeautifulSoup4 page object
    :return: List of BeautifulSoup4 page objects
    """
    main_product_lists = page_object.findAll("ul", {"class": "js-main-offers-list"})
    return main_product_lists[1].findAll("figure", {"class": "offer-thumb"})


def get_product_title(product_page_object):
    """
    Get product title string from product page-object.

    :param product_page_object: BeautifulSoup4 page object
    :return: string representation of product title
    """
    return product_page_object.find("p", {"class": "offer-thumb__title"}).get("title")


def get_product_price(product_page_object):
    """
    Get product price string from product page-object.

    :param product_page_object: BeautifulSoup4 page object
    :return: string representation of product price
    """
    return product_page_object.find("span", {"class": "price-cp"}).text


def get_product_img_href(product_page_object) -> str:
    """
    Get product image href link from product page-object.

    :param product_page_object: BeautifulSoup4 page object
    :return: string representation of product image href
    """
    anchor_element = product_page_object.find("figure", {"class": "offer-thumb__image"}).find("a", {"class": "lazy"})
    return anchor_element.get("data-original")


def write_product_list_to_json_file(product_list, filename: str):
    """
    Write list of product items into .json file with specified filename.

    :param product_list: List of product items to write.
    :param filename: Name of output file
    """
    with open(filename, 'w') as file:
        json.dump(product_list, file, indent=4)


def check_url(url: str):
    print(f"Checking URL {url}")
    try:
        connection = urllib.request.urlopen(url)
        status_code = connection.getcode()
        print(f"Server responded with status code {status_code}\n")
    except urllib.error.HTTPError as error:
        print(f"URL checking failed, url {url} raised {error}")
        print("This is most likely due to the provided category not being valid or Osta.ee servers are not "
              "responding.")
        sys.exit()


if __name__ == "__main__":
    base_url = "https://www.osta.ee/kategooria/"
    output_filename = "products.json"
    category = ""

    if len(sys.argv) >= 2:
        category = sys.argv[1].lstrip("/")
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]

    if not category:
        print("Scraping failed, please enter a valid category to scrape as a command line argument,"
              " for example arvutid/sulearvutid")
    else:
        full_url = base_url + category
        check_url(full_url)
        scrape_product_category(full_url, output_filename)
