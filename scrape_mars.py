from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
import pymongo


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    listings = {}

    # Visit https://mars.nasa.gov/news/
    News_url = "https://mars.nasa.gov/news/"
    browser.visit(News_url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    listings["news_title"]=soup.find('div', class_='content_title').get_text()
    listings["news_p"]=soup.find('div', class_='article_teaser_body').get_text()
    

    JPL_Mars_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit"
    browser.visit(JPL_Mars_url)
    html=browser.html
    soup=bs(html,'html.parser')

    featured_image_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars#submit"
    browser.visit(featured_image_url)
    html=browser.html
    soup=bs(html,'html.parser')
    featured_image_url=soup.find('img', class_='fancybox-image')
    listings["featured_image_url"]=soup.find('img', class_='fancybox-image')


    mars_weather="https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather)
    html=browser.html
    soup=bs(html,'html.parser')
    listings["mars_weather"] = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    mars_facts_url="https://space-facts.com/mars/"
    tables = pd.read_html(mars_facts_url)
    df = tables[0]
    df.columns = ['0', '1']
    listings["html_table"] = df.to_html()

    #executable_path = {'executable_path': 'chromedriver'}
    #browser = Browser('chrome', **executable_path, headless=False)

    hemisphere_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    hem_img_urls = []
    hem_dict = {'title': [], 'img_url': [],}

    x = soup.find_all('h3')

    for i in x:
       t = i.get_text()
       title = t.strip('Enhanced')
       browser.click_link_by_partial_text(t)
       url = browser.find_link_by_partial_href('download')['href']
       hem_dict = {'title': title, 'img_url': url}
       hem_img_urls.append(hem_dict)
       browser.back()

    listings["hemispheres"]=hem_img_urls
    return listings
