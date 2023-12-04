# RecipeScrape
Designed to scrape recipes from the internet.

**Hello Fresh Scraper:**
**Status:** Working
**Issues:** 
  **Critical:**
    The "Load More" button doesn't load a new URL but it is a continuation of the current URL, so when going to page 2, all of the results that were loaded on
    page 1 are reloaded into the dataframe resulting in a duplicate entry for every pagination.


**Blue Apron Scraper:**
**Status:** Working
**Issues:** 
  **Non-Critical:**
    Current code is only working for writing recipes into flat files on a local machine. Script works when run from local machine with chrome driver installed.
