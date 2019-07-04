"""
Arxiv Category scraper
===========
Toy indexing example for testing purposes.
:Author: Omid Mohammadi Kia
"""
from bs4 import BeautifulSoup
import requests
import numpy as np
# url to scrape
cat_url = 'https://arxiv.org/'
subcat_url = 'https://arxiv.org/archive/'

def return_soup(url):
    url = requests.get(url).content
    soup = BeautifulSoup(url,"html.parser")
    return soup
    
def get_namespace(x):
    name = x.find('a').text
    tag = x.find('b').text
    return name, tag

def convert_to_markdown(*args):
    print (('|'+a for a in args))

    
main_page = return_soup(cat_url).find_all('li')    
CategoryDict={}   
print ('| Category | Code |  Subcategories | Subcode |\n| --- | --- | --- | --- |')
for x in main_page[0:]:
    try:
        xname,xtag = get_namespace(x)
        string = '| ' + xname + ' | `' + xtag + '` | '
	CategoryDict.update(xname= xtag )
        print (string)
        subcat_page = return_soup(subcat_url + xtag).find_all('ul')[-1].find_all('b')
        for y in subcat_page:
            subs = y.text.split(' - ')
            print ('| | | '+ subs[1] + ' | `' +  subs[0] + '`')
	    CategoryDict.update(subs[1]= subs[0] )
    except:
		pass
#saving dictionary in a file
#https://stackoverflow.com/a/32216025/6594253
np.save('CategoryDict.npy', CategoryDict) 
