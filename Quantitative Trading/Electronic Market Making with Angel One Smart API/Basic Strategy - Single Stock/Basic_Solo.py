"NSE Multi Thread Market Maker - Basic Strategy for Single Stock"

"Pre-Defined Functions"

# cancel_order(order_id) -> Cancels a specific order
# get_tradebook() -> Returns a List of Dictionaries of all Trades
# get_all_open_orders() -> Returns all Pending Orders as a DF
# CancelAll() -> Cancels all Pending Orders
# get_position() -> Gets the Current Position as a list of Dictionaries

"Specific Functions"

# place_buy_order(stocks, tokens, price, trade_qty) -> Places a Limit Buy Order
# place_sell_order(stocks, tokens, price, trade_qty) -> Places a Limit Sell Order
# get_ltp(stocks, tokens) -> Gets LTP of Stocks as a List
# initialize() -> Send a single buy and sell to all Stocks to initialize a position
# trade_solo() -> Performs the basic Trading Algo for NSE Market Maker. (Single Order per Cycle)
# portfolio_trade_trimmer() -> Sends cover order for the portfolio take profit margin price and net qty.
# individual_trade_trimmer() -> Sends cover order for the net qty at the last traded take profit margin price.
# average_trade_trimmer() -> Sends cover order for the net qty at the avg price & margin of net open position.
# squareoff() -> Square Offs all Open Positions at LTP. Waits 30 seconds and prints current positions.

"Multi Thread Functions"

# mt_getpos() -> Updates Current Positions every 2 seconds.
# mt_ptt() -> Repeats Portfolio Trade Trimmer every 15 seconds.
# mt_itt() -> Repeats Individual Trade Trimmer every 15 seconds.
# mt_att() -> Repeats Average Trade Trimmer every 15 seconds.


################################## Import Modules & API Login #########################################

from smartapi import SmartConnect
import os
from pyotp import TOTP
import pandas as pd
import time
from datetime import datetime
import numpy as np
import threading


key_path = r"C:\Users\ADMIN\Desktop\Angel_Smart_API_Electronic_Market_Making_Strategy"
os.chdir(key_path)
key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()


########################### Basic Functions for Algo & Order Management #################################

def cancel_order(order_id):
    params = {
        "variety": "NORMAL",
        "orderid": order_id
    }
    response = obj.cancelOrder(params["orderid"], params["variety"])
    return response

def get_tradebook():
    Trades = obj.tradeBook()['data']
    Full_Trade_Book = []
    Full_Trade_Book.append(Trades)
    return Full_Trade_Book

def get_all_open_orders():
    response = obj.orderBook()
    OpenOrders = pd.DataFrame(response['data'])
    return OpenOrders[OpenOrders["orderstatus"]=="open"]

def CancelAll():
    open_orders = get_all_open_orders()
    order_ids = open_orders["orderid"].values
    for eachOrder in order_ids:
            cancel_order(eachOrder)
    print("Pending Orders Cancelled")

current_position =  {}

def get_position():
    global current_position
    positions = obj.position()["data"]
    current_position =  {
                        "symbolname": [],
                        "exchange": [],
                        "tradingsymbol": [],
                        "symboltoken": [],
                        "netqty": [],
                        "buyqty": [],
                        "sellqty": [],
                        "buyamount": [],
                        "sellamount": [],
                        "buyavgprice": [],
                        "sellavgprice": [],
                        "ltp": [],
                        "pnl": []
                        }
    for pos in range(len(positions)):
        current_position["symbolname"].append(positions[pos]["symbolname"])
        current_position["exchange"].append(positions[pos]["exchange"])
        current_position["tradingsymbol"].append(positions[pos]["tradingsymbol"])
        current_position["symboltoken"].append(positions[pos]["symboltoken"])
        current_position["netqty"].append(int(positions[pos]["netqty"]))
        current_position["buyqty"].append(int(positions[pos]["buyqty"]))
        current_position["sellqty"].append(int(positions[pos]["sellqty"]))
        current_position["buyamount"].append(float(positions[pos]["buyamount"]))
        current_position["sellamount"].append(float(positions[pos]["sellamount"]))
        current_position["buyavgprice"].append(float(positions[pos]["buyavgprice"]))
        current_position["sellavgprice"].append(float(positions[pos]["sellavgprice"]))
        current_position["ltp"].append(float(positions[pos]["ltp"]))
        current_position["pnl"].append(float(positions[pos]["pnl"]))
    return current_position


####################### Specific Functions for NSE Market Maker ###################################

stocks=["RELIANCE-EQ"]
tokens=["2885"]
margins= [1.9]
trade_qty=[15]


def place_buy_order(stocks, tokens, price, trade_qty):
    params = {
                "variety": "NORMAL",
                "tradingsymbol": stocks,
                "symboltoken": tokens,
                "transactiontype": "BUY",
                "exchange": "NSE",
                "ordertype": "LIMIT",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": price,
                "quantity": trade_qty
                }
    response = obj.placeOrder(params)
    return response

def place_sell_order(stocks, tokens, price, trade_qty):
    params = {
                "variety": "NORMAL",
                "tradingsymbol": stocks,
                "symboltoken": tokens,
                "transactiontype": "SELL",
                "exchange": "NSE",
                "ordertype": "LIMIT",
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": price,
                "quantity": trade_qty
                }
    response = obj.placeOrder(params)
    return response

def get_ltp(stocks, tokens):
    params = {
                "exchange": "NSE",
                "tradingsymbol": stocks,
                "symboltoken": tokens
             }
    response = obj.ltpData(params["exchange"], params["tradingsymbol"], params["symboltoken"])
    return response["data"]["ltp"]

def initialize():
    ltp=[]
    for j in range(len(stocks)):
        ltp.append(get_ltp(stocks[j],tokens[j]))
    print(stocks)
    print(ltp)
    for i in range(len(stocks)):
        place_buy_order(stocks[i], tokens[i], ltp[i], 1)
        place_sell_order(stocks[i], tokens[i], ltp[i], 1)
    print("Initial Orders Sent")


def trade_solo():
    pos=0
    Order_IDs_TF=[]
    while pos < len(stocks):
        if abs(current_position['netqty'][pos]) == 0:
            print(current_position['symbolname'][pos], ": Buy and Sell Orders : LTP :", current_position['ltp'][pos])
            Order_IDs_TF.append(place_buy_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos] - margins[pos], trade_qty[pos]))
            Order_IDs_TF.append(place_sell_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos] + margins[pos], trade_qty[pos]))
        elif current_position['netqty'][pos] > 0:
            print(current_position['symbolname'][pos], ": Sell Orders Only : LTP :", current_position['ltp'][pos])
            Order_IDs_TF.append(place_sell_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos] + margins[pos], trade_qty[pos]))
        elif current_position['netqty'][pos] < 0 :
            print(current_position['symbolname'][pos], ": Buy Orders Only : LTP :", current_position['ltp'][pos])
            Order_IDs_TF.append(place_buy_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos] - margins[pos], trade_qty[pos]))
        pos+=1
    time.sleep(45)
    for each_order in Order_IDs_TF:
        cancel_order(each_order)


def portfolio_trade_trimmer():
    pos=0
    Order_IDs_PTT = []
    while pos < len(stocks):
        if current_position['netqty'][pos] == 0:
            print(current_position['symbolname'][pos], ": Net Qty Nil")
        elif current_position['netqty'][pos] > 0:
            expected_profit = (current_position['buyqty'][pos]*(margins[pos]))
            trimmer_price = (current_position['buyamount'][pos] + expected_profit - current_position['sellamount'][pos])/abs(current_position['netqty'][pos])
            trimmer_price = round(trimmer_price * 2.0, 1) / 2.0
            Order_IDs_PTT.append(place_sell_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], trimmer_price, abs(current_position['netqty'][pos])))
            print(current_position['symbolname'][pos], ": Long Position - Sending Sell Order", trimmer_price)
        elif current_position['netqty'][pos] < 0:
            expected_profit = (current_position['sellqty'][pos] * (margins[pos]))
            trimmer_price = (current_position['sellamount'][pos] - expected_profit - current_position['buyamount'][pos]) / abs(current_position['netqty'][pos])
            trimmer_price = round(trimmer_price * 2.0, 1) / 2.0
            Order_IDs_PTT.append(place_buy_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], trimmer_price, abs(current_position['netqty'][pos])))
            print(current_position['symbolname'][pos], ": Short Position - Sending Buy Order", trimmer_price)
        pos+=1
    time.sleep(15)
    for Each_Order in Order_IDs_PTT:
            cancel_order(Each_Order)


def time_func(time_str):
    return datetime.strptime(time_str, '%H:%M:%S').time()


def individual_trade_trimmer():
    Full_Trade_Book = obj.tradeBook()['data']
    pos = 0
    Order_IDs_ITT=[]
    while pos<len(stocks):
        Trades=[]
        for each_trade in Full_Trade_Book:
            if each_trade['tradingsymbol'] == stocks[pos]:
                Trades.append(each_trade)
        Trades = sorted(Trades, key=lambda x: time_func(x['filltime']))
        Buy_Trades=[]
        Sell_Trades=[]
        for each_stock_trade in Trades:
            if each_stock_trade['transactiontype'] == 'BUY':
                Buy_Trades.append(int(each_stock_trade['fillsize']))
            elif each_stock_trade['transactiontype'] == 'SELL':
                Sell_Trades.append(int(each_stock_trade['fillsize']))
        Total_Buy_Qty = sum(Buy_Trades)
        Total_Sell_Qty = sum(Sell_Trades)
        Net_Qty = Total_Buy_Qty - Total_Sell_Qty
        Trade_Price = float(Trades[-1]['fillprice'])
        Trade_Price = round(Trade_Price * 2.0, 1) / 2.0
        if Net_Qty == 0:
            print(stocks[pos],": Net Positon = 0")
        elif Net_Qty > 0:
            print(stocks[pos], "Sell Order for Qty", abs(Net_Qty))
            Order_IDs_ITT.append(place_sell_order(stocks[pos], tokens[pos], Trade_Price+margins[pos], abs(Net_Qty)))
            print(stocks[pos], tokens[pos], Trade_Price+margins[pos], abs(Net_Qty))
        elif Net_Qty < 0:
            print(stocks[pos], "Buy Order for Qty", abs(Net_Qty))
            Order_IDs_ITT.append(place_buy_order(stocks[pos], tokens[pos], Trade_Price-margins[pos], abs(Net_Qty)))
            print(stocks[pos], tokens[pos], Trade_Price-margins[pos], abs(Net_Qty))
        pos+=1
    print(Order_IDs_ITT)
    time.sleep(15)
    for Each_Order in Order_IDs_ITT:
            cancel_order(Each_Order)


def average_trade_trimmer():
    Trade_Book = obj.tradeBook()['data']
    pos = 0
    Order_IDs_ATT = []
    for stock in stocks:
        All_Trades = []
        for each_trade in Trade_Book:
            if each_trade['tradingsymbol'] == stock:
                All_Trades.append(each_trade)
        All_Trades = sorted(All_Trades, key=lambda x: time_func(x['filltime']))
        All_Trades = list(reversed(All_Trades))
        Total_Net_Qty = current_position['netqty'][pos]
        if Total_Net_Qty == 0:
            print('ATT Net Position Zero for', stock)
        elif Total_Net_Qty > 0:
            print(stock, 'ATT Sell Order')
            Remaining_Net_Qty = abs(Total_Net_Qty)
            total_value = 0.0
            for each_trade in All_Trades:
                if each_trade['transactiontype']=='BUY':
                    Last_Trade_Qty = int(each_trade['fillsize'])
                    Last_Trade_Price = float(each_trade['fillprice'])
                    if Remaining_Net_Qty > abs(Last_Trade_Qty):
                        total_value += Last_Trade_Qty * Last_Trade_Price
                        Remaining_Net_Qty -= abs(Last_Trade_Qty)
                    else:
                        total_value += Remaining_Net_Qty * Last_Trade_Price
                        Remaining_Net_Qty = 0
            ATT_Price = total_value / abs(Total_Net_Qty)
            ATT_Price = round(ATT_Price * 2.0, 1) / 2.0
            print('ATT Price for', stock, '=', ATT_Price)
            print(stocks[pos], "Sell Order for Total_Net_Qty", abs(Total_Net_Qty))
            Order_IDs_ATT.append(place_sell_order(stocks[pos], tokens[pos], ATT_Price+margins[pos], abs(Total_Net_Qty)))
            print(stocks[pos], tokens[pos], ATT_Price+margins[pos], abs(Total_Net_Qty))
        elif Total_Net_Qty < 0:
            print(stock, 'ATT Buy Order')
            Remaining_Net_Qty = abs(Total_Net_Qty)
            total_value = 0.0
            for each_trade in All_Trades:
                if each_trade['transactiontype']=='SELL':
                    Last_Trade_Qty = int(each_trade['fillsize'])
                    Last_Trade_Price = float(each_trade['fillprice'])
                    if Remaining_Net_Qty > abs(Last_Trade_Qty):
                        total_value += Last_Trade_Qty * Last_Trade_Price
                        Remaining_Net_Qty -= abs(Last_Trade_Qty)
                    else:
                        total_value += Remaining_Net_Qty * Last_Trade_Price
                        Remaining_Net_Qty = 0
            ATT_Price = total_value / abs(Total_Net_Qty)
            ATT_Price = round(ATT_Price * 2.0, 1) / 2.0
            print('ATT Price for', stock, '=', ATT_Price)
            print(stocks[pos], "Buy Order for Total_Net_Qty", abs(Total_Net_Qty))
            Order_IDs_ATT.append(place_buy_order(stocks[pos], tokens[pos], ATT_Price-margins[pos], abs(Total_Net_Qty)))
            print(stocks[pos], tokens[pos], ATT_Price-margins[pos], abs(Total_Net_Qty))
        pos += 1
    time.sleep(15)
    for Each_ATT_Order in Order_IDs_ATT:
            cancel_order(Each_ATT_Order)


def squareoff():
    CancelAll()
    pos = 0
    while pos < len(current_position['symbolname']):
        if current_position['netqty'][pos] == 0:
            print(current_position['symbolname'][pos], "Net Positon = 0")
        elif current_position['netqty'][pos] > 0:
            print(current_position['symbolname'][pos], "Sell Order for Qty", abs(current_position['netqty'][pos]))
            place_sell_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos], abs(current_position['netqty'][pos]))
        elif current_position['netqty'][pos] < 0:
            print(current_position['symbolname'][pos], "Buy Order for Qty", abs(current_position['netqty'][pos]))
            place_buy_order(current_position['tradingsymbol'][pos], current_position['symboltoken'][pos], current_position['ltp'][pos], abs(current_position['netqty'][pos]))
        pos += 1
    time.sleep(30)
    print(current_position['symbolname'])
    print("Net Positions:", current_position['netqty'])
    print("PNL:", current_position['pnl'])


################################ Multi Thread Functions ######################################

def mt_getpos():
    while True:
        get_position()
        print("Get Position Updated")
        print(current_position)
        time.sleep(2)

def mt_itt():
    while True:
        individual_trade_trimmer()
        print("Individual Trade Trimmer Sent")

def mt_ptt():
    while True:
        portfolio_trade_trimmer()
        print("Portfolio Trade Trimmer Sent")

def mt_att():
    while True:
        average_trade_trimmer()
        print("Average Trade Trimmer Sent")

print('Good Luck!')


###################### "NSE Multi Thread Market Maker Starts" #########################################

"NSE Multi Thread Market Maker Starts"

initialize()
time.sleep(5)
get_position()
squareoff()
get_position()
squareoff()
get_position()
print("----Algo Initialisation Complete-----")
time.sleep(30)


thr1 = threading.Thread(target=mt_getpos)
thr2 = threading.Thread(target=mt_itt)
thr3 = threading.Thread(target=mt_ptt)
thr4 = threading.Thread(target=mt_att)

thr1.start()
time.sleep(2)
thr2.start()
time.sleep(2)
thr3.start()
time.sleep(2)
thr4.start()
time.sleep(2)

pos=0
while pos<5:
    print("-----------------------------------------------------------------------------------")
    print(time.ctime(), "Iteration No:", pos+1)
    trade_solo()
    pos+=1

CancelAll()
squareoff()
squareoff()
squareoff()



