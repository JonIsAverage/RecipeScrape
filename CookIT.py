# Author: Jonathan Wiggins
# Date:   20201028
# Title:  CookIT.py
# Purpose:Crawl websites for recipes and then evaluate if you have the on hand ingredients to cook these recipes, if not
#         what do you need.

import time
import RecipeCrawler
import RecipeAnalyzer
import RecipeNormalizer


def Main():
    #Crawls Blue Apron for recipes
    RecipeCrawler.CrawlBlueApron()

    #Analyzes recipes
    #RecipeAnalyzer.Analyze()

    #Normalizes the recipe data
    #RecipeNormalizer.Normalize()

Main()