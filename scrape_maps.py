import numpy as np
import pandas as pd
import urllib
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    

    ########## NEWS
    target = "https://mars.nasa.gov/news/"
    response = requests.get(target) 
    print(response)
    url = target
    browser.visit(url)
    print(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slides = soup.find_all("div", {"class":"list_text"}) #summary-sale-item-price-retail (for suggested retail)

    for slide in slides:
        #print(slide)
        ct = soup.find("div", {"class":"content_title"})
        print(ct.text)
        news_title = ct.text
        atb = soup.find("div", {"class":"article_teaser_body"})
        print(atb.text)
        new_p = atb.text
        break;
    

    ################### JPL Image
    jplimage= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    url = jplimage
    print(url)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slides = soup.find_all("article") #summary-sale-item-price-retail (for suggested retail)

    for x in slides:
        print(x['style'])
        imgURL = soup.find("a", {"class":"button fancybox"})
        print(imgURL)
        print(imgURL['data-fancybox-href'])
        feature_image_url = 'https://www.jpl.nasa.gov' + imgURL['data-fancybox-href']

    ####### TWIT
    twitter = "https://twitter.com/marswxreport?lang=en"
    url = twitter
    browser.visit(url)
    print(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slides = soup.find("p", {"class":"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}) #summary-sale-item-price-retail (for suggested retail)
    print(slides.text)
    mars_weather = slides.text  

    ########## FACTS!
    res = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    print(df[0].to_json(orient='records'))
    mars_facts = df[0].to_html

    ############## IMAGERY

    hemi = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    url = hemi
    browser.visit(url)
    print(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slides = soup.find_all("div") #summary-sale-item-price-retail (for suggested retail)
    ####### THIS SERVICE IS DOWN ##########

    masterDict = {"news":{news_title, new_p}, "feature_image_ulr":feature_image_url, "mars_weather":mars_weather, "mars_facts":mars_facts}
    return masterDict

mdat = scrape()
print(mdat)
print(mdat['news'])