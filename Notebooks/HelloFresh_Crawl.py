# Databricks notebook source
#%pip install selenium

# COMMAND ----------

import time, requests, csv, os
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from pyspark.sql.types import *

# Recipe Types:
#recipetype = "taco-recipes"
#recipetype = "burger-recipes"

recipetype = "burger-recipes"

# COMMAND ----------

def Crawl():
    success = 0
    URL = 'https://www.hellofresh.com/recipes/' + recipetype + '/'
    page = requests.get(URL)
    pagenum = 0
    v = 2
    driver2 = page
    strpage = str(page)
    bool_Paginate = False
    if strpage == "<Response [200]>":
        success = 1
        CrawlPage(page, URL, bool_Paginate, pagenum, v)
        quit()
    else:
        success = 0
        print("Connection failed with HTTP status:", page)
        print("Exiting..")
        quit()

# COMMAND ----------

def EmptyDF():
    field = [StructField("field1", StringType(), True)]
    schema = StructType(field)

    sp_df_Recipe3 = spark.sparkContext
    sp_df_Recipe3 = sqlContext.createDataFrame(sc.emptyRDD(), schema)

# COMMAND ----------

def CrawlPage(page, URL, bool_Paginate, pagenum, v):
    if bool_Paginate == 0:
        soup = BeautifulSoup(page.content, 'html.parser')
    if bool_Paginate == 1:
        soup = BeautifulSoup(page, 'html.parser')
    results = soup.find(id='page')
    recipe_elems = results.find_all('div', class_='web-1nlafhw')
    for recipe_elem in recipe_elems:
        link = recipe_elem.find('a')['href']
        strrecname = recipe_elem.text.strip()
        spltrecname = strrecname.replace("\n", "")
        name = spltrecname
        CrawlRecipe(link, name, v)
    nextbtn = soup.find(id='__next')
    next_button = nextbtn.find('div', class_='web-5mk6ar')

    if next_button:

        if bool_Paginate == False:
            pagenum = pagenum + 1
            print(pagenum)
            URL = 'https://www.hellofresh.com/recipes/taco-recipes?page=' + str(pagenum)
            page = requests.get(URL)
            CrawlPage(page, URL, bool_Paginate, pagenum, v)

        if bool_Paginate == True:
            pagenum = pagenum + 1
            print(pagenum)
            bool_Paginate = True
            URL = 'https://www.hellofresh.com/recipes/taco-recipes?page=' + str(pagenum)
            page = requests.get(URL)
            CrawlPage(page, URL, bool_Paginate, pagenum, v)
    else:
        print("broke")
        quit()

# COMMAND ----------

def AddToDataframe(v, sp_df_Recipe):
    if v == 2:
        sp_df_Recipe3 = (sp_df_Recipe)
        v=1
    if v == 1:
        sp_df_Recipe3=sp_df_Recipe3.union(sp_df_Recipe)
    else:
        print("BREAK")
        quit()

# COMMAND ----------

def CrawlRecipe(link, name, v):
    success = 0
    URL = link
    page = requests.get(URL)
    strpage = str(page)
    lst = []
    if strpage == "<Response [200]>":
        success = 1
    else:
        success = 0
    soup = BeautifulSoup(page.content, 'html.parser')
    ingrd_elems = soup.find('div', class_='sc-a6821923-0 kOxEZP')
    df_Recipe = pd.DataFrame(columns=['Name','Ingredient','Amount','Link'])
    df_RecipeInfo = pd.DataFrame(columns=['ID','Name','Link'])
    for div in soup.find_all('div', class_='sc-a6821923-0 frRfTC'):
        quantity = div.find('p', class_='sc-a6821923-0 bNkKoC').text
        ingredient = div.find('p', class_='sc-a6821923-0 fLfTya').text
        lst.append({'Name': name, 'Ingredient': ingredient, 'Amount': quantity, 'Link': link})

    df_Recipe = pd.DataFrame(lst, columns=['Name','Ingredient','Amount','Link'])
    sp_df_Recipe = spark.createDataFrame(df_Recipe)
    AddToDataframe(v, sp_df_Recipe)

# COMMAND ----------

Crawl()
print("Done")

# COMMAND ----------

sp_df_Recipe3.createOrReplaceTempView("tmp_vw_Recipes")

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from tmp_vw_Recipes
