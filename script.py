# SALTDEAN
from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen
#from fake_useragent import UserAgent

def get_html(url):
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except:
        pass

    return html_content

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.products .item-name a'):
            item = 'https://saltdeanstamps.com/' + item.get('href')   
            items.append(item)
    except:
        pass

    try:
        next_item = html.find_all("link", {"rel":"next"})[0]
        next_url = 'https://saltdeanstamps.com/' + next_item.get('href')   
    except:
        pass

    shuffle(items)

    return items, next_url

def get_categories(url):
    
    items = []
    
    try:
        html = get_html(url)
        for item in html.select('.cat-item-name a'):
            item_url = 'https://saltdeanstamps.com/' + item.get('href')
            items.append(item_url)
    except: 
        pass
    
    return items

def get_main_categories():
    
    url = 'https://saltdeanstamps.com/'
    
    items = {}
    try:
        html = get_html(url)
        category_items = html.select('#category-menu a')
        for category_item in category_items:
            item_url = 'https://saltdeanstamps.com/' + category_item.get('href')
            item_text = category_item.get_text().strip()
            if item_text != 'Thematic':
                items[item_text] = item_url
    except: 
        pass

    return items

def get_details(url):

    stamp = {}
    category = ''

    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price = html.select('#_EKM_PRODUCTPRICE')[0].get_text()
        price = price.replace(",", "").strip()
        stamp['price'] = price
    except:
        stamp['price'] = None
        
    try:
        title = html.select('#product-name')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        year = html.select('#_EKM_PRODUCTATRRIBUTE_YEAROFISSUE_VALUE')[0].get_text().strip()
        stamp['year'] = year
    except:
        stamp['year'] = None        

    try:
        country = html.select("#_EKM_PRODUCTATRRIBUTE_COUNTRIES_VALUE")[0].get_text()
        stamp['country'] = country
    except:
        stamp['country'] = None
        
    try:
        category_items = html.select("#location span a")
        for category_item in category_items:
            category_text = category_item.get_text().strip()
            if category:
                category = category + ' > '
            if category_text != 'Home':
                category = category + category_text
        stamp['category'] = category
    except:
        stamp['category'] = None    

    try:
        sku = html.select("#_EKM_PRODUCTCODE")[0].get_text().strip()
        stamp['sku'] = sku
    except:
        stamp['sku'] = None

    try:
        raw_text_temp = html.find_all("span", {"itemprop":"description"})[0].get_text().strip()
        raw_text_temp = raw_text_temp.replace("\r\n", ' ').replace("\n", ' ').strip()
        raw_text_parts = raw_text_temp.split('Our Ref')
        raw_text = raw_text_parts[0].strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    try:
    	temp = raw_text.split(' ')
    	stamp['SG']=temp[-1]
    except:
    	stamp['SG']=None

    stamp['currency'] = 'GBP'
    
    # image_urls should be a list
    images = []
    try:
        image_items = html.select('#product-image a')
        for image_item in image_items:
            img_href = image_item.get('href')
            if img_href != '#':
                img = 'https://saltdeanstamps.com' + img_href
                if img not in images:
                    images.append(img)
    except:
        pass

    stamp['image_urls'] = images

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
    return stamp

# choose input category
categories = get_main_categories()
for category_item in categories.items():
    print(category_item)

selected_category_name = input('Make a selection: ')
category = categories[selected_category_name]

# loop through all subcategories
subcategories = get_categories(category)
for subcategory in subcategories:
    # loop through all subcategories of level 2
    subcategories2 = get_categories(subcategory)
    if subcategories2:
        page_urls = subcategories2
    else:
        page_urls = subcategory
    for page_url in page_urls:        
        while(page_url):
            page_items, page_url = get_page_items(page_url)
            # loop through all items on current page
            for page_item in page_items:
                stamp = get_details(page_item)
