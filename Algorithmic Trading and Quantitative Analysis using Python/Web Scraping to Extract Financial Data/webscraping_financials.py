# ============================================================================
# Getting financial data from yahoo finance using webscraping

# =============================================================================

import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL","FB","CSCO","INFY.NS","3988.HK"]
income_statatement_dict = {}
balance_sheet_dict = {}
cashflow_st_dict = {}

for ticker in tickers:
    #scraping income statement
    url = "https://finance.yahoo.com/quote/{}/financials?p={}".format(ticker,ticker)
    income_statement = {}
    table_title = {}
    
    headers = {"User-Agent" : "Chrome/96.0.4664.110"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div" , {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div" , {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div" , {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            income_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]

    temp = pd.DataFrame(income_statement).T
    temp.columns = table_title["Breakdown"]
    income_statatement_dict[ticker] = temp
    
    #scraping balance sheet statement
    url = "https://finance.yahoo.com/quote/{}/balance-sheet?p={}".format(ticker,ticker)
    balance_sheet = {}
    table_title = {}
    
    headers = {"User-Agent" : "Chrome/96.0.4664.110"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div" , {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div" , {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div" , {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            balance_sheet[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]

    temp = pd.DataFrame(balance_sheet).T
    temp.columns = table_title["Breakdown"]
    balance_sheet_dict[ticker] = temp
    
    #scraping cashflow statement
    url = "https://finance.yahoo.com/quote/{}/cash-flow?p={}".format(ticker,ticker)
    cashflow_statement = {}
    table_title = {}
    
    headers = {"User-Agent" : "Chrome/96.0.4664.110"}
    page = requests.get(url, headers=headers)
    page_content = page.content
    soup = BeautifulSoup(page_content,"html.parser")
    tabl = soup.find_all("div" , {"class" : "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        heading = t.find_all("div" , {"class": "D(tbr) C($primaryColor)"})
        for top_row in heading:
            table_title[top_row.get_text(separator="|").split("|")[0]] = top_row.get_text(separator="|").split("|")[1:]
        rows = t.find_all("div" , {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            cashflow_statement[row.get_text(separator="|").split("|")[0]] = row.get_text(separator="|").split("|")[1:]

    temp = pd.DataFrame(cashflow_statement).T
    temp.columns = table_title["Breakdown"]
    cashflow_st_dict[ticker] = temp
    
#converting dataframe values to numeric
for ticker in tickers:
    for col in income_statatement_dict[ticker].columns:
        income_statatement_dict[ticker][col] = income_statatement_dict[ticker][col].str.replace(',|- ','')
        income_statatement_dict[ticker][col] = pd.to_numeric(income_statatement_dict[ticker][col], errors = 'coerce')
        cashflow_st_dict[ticker][col] = cashflow_st_dict[ticker][col].str.replace(',|- ','')
        cashflow_st_dict[ticker][col] = pd.to_numeric(cashflow_st_dict[ticker][col], errors = 'coerce') 
        if col!="ttm": # yahoo has ttm column for income statement and cashflow statement only
            balance_sheet_dict[ticker][col] = balance_sheet_dict[ticker][col].str.replace(',|- ','')
            balance_sheet_dict[ticker][col] = pd.to_numeric(balance_sheet_dict[ticker][col], errors = 'coerce')
           
