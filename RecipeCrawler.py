import time
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
from selenium import webdriver

# Variables
# vegetarian, beef,porkpoultry

recipetype = "poultry"

def CrawlBlueApron():
    print("Connecting to Blue Apron..")
    success = 0
    URL = 'https://www.blueapron.com/cookbook/' + recipetype + '/'
    page = requests.get(URL)
    next_button2 = page
    pagenum = 0
    driver2 = page
    strpage = str(page)
    bool_Paginate = False
    if strpage == "<Response [200]>":
        print("Connection successful.")
        success = 1
        CrawlPage(page, URL, bool_Paginate, next_button2, driver2, pagenum)
    else:
        success = 0
        print("Connection failed with HTTP status:", page)
        print("Exiting..")
        quit()


def CrawlPage(page, URL, bool_Paginate, next_button2, driver2, pagenum):
    print("Crawling page..")
    if bool_Paginate == 0:
        soup = BeautifulSoup(page.content, 'html.parser')
    if bool_Paginate == 1:
        soup = BeautifulSoup(page, 'html.parser')
    results = soup.find(id='cookbook-thumbs')
    recipe_elems = results.find_all('div', class_='recipe-thumb col-md-4')
    for recipe_elem in recipe_elems:
        link = recipe_elem.find('a')['href']
        strrecname = recipe_elem.text.strip()
        spltrecname = strrecname.replace("\n", "")
        print(spltrecname)
        name = spltrecname
        print(f"Recipe Link here: https://www.blueapron.com{link}\n")
        CrawlRecipe(link, name)
    next_button = soup.find('a', id='paginate_cookbook', href=True)

    if next_button:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome("C:\chromedriver\\bin\chromedriver.exe", chrome_options=options)

        if bool_Paginate == False:
            pagenum = pagenum + 1
            driver.get(URL)
            next_button = driver.find_element_by_id("paginate_cookbook")
            driver.execute_script("arguments[0].click();", next_button)
            print("Executing page: " + str(pagenum))
            time.sleep(5)
            driver2 = driver
            next_button2 = driver.find_element_by_id("paginate_cookbook")
            page = driver.page_source
            bool_Paginate = True
            pagenum = pagenum + 1
            CrawlPage(page, URL, bool_Paginate, next_button2, driver2, pagenum)

        if bool_Paginate == True:
            driver2.execute_script("arguments[0].click();", next_button2)
            print("Executing page: " + str(pagenum))
            time.sleep(5)
            next_button2 = driver2.find_element_by_id("paginate_cookbook")
            page = driver2.page_source
            bool_Paginate = True
            pagenum = pagenum + 1
            CrawlPage(page, URL, bool_Paginate, next_button2, driver2, pagenum)
    else:
        print("broke")
        quit()


def CrawlRecipe(link, name):
    print(f"Reading recipe: {name}\n")
    # print("Ignoring recipes to improve debug performance.")

    success = 0
    URL = 'https://www.blueapron.com' + link
    page = requests.get(URL)
    strpage = str(page)
    if strpage == "<Response [200]>":
        print("Connection successful.")
        success = 1
    else:
        success = 0
        print("Recipe not found at:", page)
        print("Moving on to the next recipe.")
    soup = BeautifulSoup(page.content, 'html.parser')
    ingrd_elems = soup.find('section', class_='section-recipe recipe-ingredients p-15')
    ingrd_elems1 = ingrd_elems.find_all('div', class_='non-story')
    recipenamefile = name.replace(" ", "_")
    recipenamefile = name.replace('"', "_")
    recipenamefile = recipenamefile.replace("-", "_")
#    csvfile = ('C:\CookIT\Recipes\BlueApron\Vegetarian\\' + recipenamefile + ".csv")
    csvfile = ('C:\CookIT\Recipes\BlueApron\\' + recipetype + '\\' + recipenamefile + ".csv")
    if os.path.isfile(csvfile) == True:
        os.remove(csvfile)
    df_Recipe = pd.DataFrame(columns=['Ingredient', 'Amount', 'URL'])
    df_Recipe.to_csv(csvfile)
    for ingrd_elem1 in ingrd_elems1:
        ingrd = ingrd_elem1.text.strip()
        ingrd = ingrd.replace("\n", ",")
        ingrd = ingrd.replace(",", "", 2)
        ingrd = ingrd.split(",")
        ingrdname = ingrd[1]
        ingrdamt = ingrd[0]
        new_row = {'Ingredient': ingrdname, 'Amount': ingrdamt, 'URL': URL}
        df_Recipe = df_Recipe.append(new_row, ignore_index=True)
    df_Recipe.to_csv(csvfile)
