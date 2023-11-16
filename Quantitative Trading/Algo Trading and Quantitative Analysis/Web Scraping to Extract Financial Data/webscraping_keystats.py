# ============================================================================
# Getting key statistics data from yahoo finance using webscraping
# =============================================================================

import requests
from bs4 import BeautifulSoup

tickers = ["AAPL","FB","CSCO","INFY.NS","3988.HK"]
key_statistics = {}

for ticker in tickers:
    #scraping key statistics
    url = "https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker,ticker)    
    headers = {"User-Agent" : "Chrome/96.0.4664.110"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("table" , {"class" : "W(100%) Bdcl(c)"}) #remove/add the trailing space if getting error
    
    temp_stats = {}
    for t in tabl:
        rows = t.find_all("tr")
        for row in rows:
            temp_stats[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[-1]
    
    key_statistics[ticker] = temp_stats
