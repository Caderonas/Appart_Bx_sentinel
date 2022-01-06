from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import argparse
import json

'''
pip3 install -U selenium
pip3 install webdriver_manager
'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search appart')
    parser.add_argument('integers', metavar='N', type=int, nargs='?', help='Fixe max budget price')
    args = parser.parse_args()

    opt = Options()
    opt.add_argument("--ignore-certificate-errors")
    opt.add_argument("--incognito")
    opt.add_argument("--headless")
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = opt)


    # SPOTAHOME
    driver.get(f"https://www.spotahome.com/s/brussels/for-rent:apartments/for-rent:rooms/for-rent:studios/bedrooms:1/bedrooms:2?move-in=2022-01-06&budget=0-"+str(args.integers))
    
    soup = BeautifulSoup(driver.page_source, "lxml")

    for appart in soup.find_all("div", class_="l-list__item"):
        title = appart.find("p", class_="homecard-content__title__HomecardContent___OmV4c").text

        appart = {
            "title" : title,
            "price" : appart.find("span", class_="price__Price___OmV4c").text,
            "type" : appart.find("span", class_="homecard-content__type__HomecardContent___OmV4c").text,
            "available" : appart.find("span", class_="homecard-content__available-from__HomecardContent___OmV4c").text,
            "img" : appart.find("img")['src'],
            "link" : appart.find("a", class_="home-card__HomecardWrapper___OmV4c")['href']
        }

    # IMMOWEB
    driver.get(f"https://www.immoweb.be/en/search/house-and-apartment/for-rent/Brussels%20City/1000?countries=BE&maxPrice="+str(args.integers)+"&isImmediatelyAvailable=true&page=1&orderBy=relevance")