## import the libraries
from binance.client import Client
import pandas as pd
import requests

## connect with python
api = '33ced6236b5dcc64077883472fd37a3aae566b82c13008468d8239bae0bd158d'
api_secret = 'e053e6ff070a9f4b6881457848b47bac4e1c03b41b9ad2f8f2fa9a7b25e81559'

client = Client(api, api_secret, tld="com", testnet=True)

## trading parameters
symbol = "BTCUSDT"
no_of_decimals = 1
volume = 0.1
proportion = 0.04
tp = 5
n = 10

## fetch current account balance
def get_balance():
    x = client.futures_account()
    df = pd.DataFrame(x['assets'])
    print(df)

## streaming price
def get_current_price(symbol):
    response = requests.get(f'https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}')
    price = float(response.json()['price'])
    return price

## placing buy limit order
def buy_limit(symbol,quantity,price):
    output = client.futures_create_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price,
    )
    print(output)

## placing sell limit order
def sell_limit(symbol,quantity,price):
    output = client.futures_create_order(
        symbol=symbol,
        side=Client.SIDE_SELL,
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=price,
    )
    print(output)

## closing all open orders
def close_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    for index in df.index:
        client.futures_cancel_order(symbol=symbol,orderId=df["orderId"][index])

## closing buy orders
def close_buy_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"]=="BUY"]
    for index in df.index:
        client.futures_cancel_order(symbol=symbol,orderId=df["orderId"][index])

## closing sell orders
def close_sell_orders(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"]=="SELL"]
    for index in df.index:
        client.futures_cancel_order(symbol=symbol,orderId=df["orderId"][index])

## getting direction of running positions
def get_direction(symbol):
    x = client.futures_position_information(symbol=symbol)
    df = pd.DataFrame(x)
    if float(df["positionAmt"].sum()) > 0:
        return "LONG"
    if float(df["positionAmt"].sum()) < 0:
        return "SHORT"
    else:
        return "FLAT"

## getting the market price
def get_mark_price(symbol):
    x = client.get_symbol_ticker(symbol=symbol)
    price = float(x["price"])
    return price

## placing orders like a grid
def draw_grid(n):
    pct_change = 1
    adj_sell = 1.2
    current_price = get_mark_price(symbol)
    for i in range(n):
        sell_price = float(round(((pct_change/100)*current_price*adj_sell*proportion) + current_price, no_of_decimals))
        sell_limit(symbol,volume,sell_price)
        pct_change += 1
        adj_sell += 0.2

    pct_change = -1
    adj_buy = 1.2
    current_price = get_mark_price(symbol)
    for i in range(n):
        buy_price = float(round(((pct_change/100)*current_price*adj_sell*proportion) + current_price, no_of_decimals))
        buy_limit(symbol,volume,buy_price)
        pct_change -= 1
        adj_buy += 0.2

## calculate take profit price
def cal_tp_level(symbol,tp):
    try:
        x = client.futures_position_information(symbol=symbol)
        df = pd.DataFrame(x)
        df = df.loc[df["positionAmt"] != "0.000"]
        t_margin = (float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0]))) / float(df["leverage"][0])
        profit = float(t_margin*tp*0.01)
        price = round((profit / float(df["positionAmt"][0])) + float(df["entryPrice"][0]), no_of_decimals)
        t_position_amt = 0
        for index in df.index:
            t_position_amt += abs(float(df["positionAmt"][index]))
        return price,t_position_amt

    except:
        pass

## placing take profit order
def place_tp_order(symbol,price,t_position_amt,direction):
    try:
        if direction == "LONG":
            sell_limit(symbol,t_position_amt,price)
        if direction == "SHORT":
            buy_limit(symbol, t_position_amt, price)
    except:
        place_tp_order(symbol, price, t_position_amt, direction)


## driver code
while True:
    x = client.futures_get_open_orders(symbol=symbol)
    df1 = pd.DataFrame(x)
    if len(df1) == 0:
        draw_grid(n)
    y = client.futures_position_information(symbol=symbol)
    df2 = pd.DataFrame(y)
    df2 = df2.loc[df2["positionAmt"] != "0.000"]
    if len(df2) > 0:
        direction = get_direction(symbol)
        try:
            if direction == "LONG":
                print("close buy")
                close_sell_orders(symbol)
            if direction == "SHORT":
                print("close sell")
                close_buy_orders(symbol)
        except:
            pass
        price0,amount0 = cal_tp_level(symbol,tp)
        place_tp_order(symbol,price0,amount0,direction)
        is_ok = True
        while is_ok:
            try:
                price1, amount1 = cal_tp_level(symbol, tp)
                if price1 != price0 or amount1 != amount0:
                    if direction == "LONG":
                        close_sell_orders(symbol)
                    if direction == "SHORT":
                        close_buy_orders(symbol)
                    place_tp_order(symbol, price1, amount1, direction)
                    price0 = price1
                    amount0 = amount1
            except:
                pass

            y = client.futures_position_information(symbol=symbol)
            df2 = pd.DataFrame(y)
            df2 = df2.loc[df2["positionAmt"] != "0.000"]
            if len(df2) == 0:
                try:
                    close_orders(symbol)
                    is_ok = False
                except:
                    pass
