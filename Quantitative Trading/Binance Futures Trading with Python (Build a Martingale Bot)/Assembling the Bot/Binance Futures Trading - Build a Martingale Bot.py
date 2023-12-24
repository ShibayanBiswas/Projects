## import the libraries
from binance.client import Client
import pandas as pd
import requests

## connect with python
api = '33ced6236b5dcc64077883472fd37a3aae566b82c13008468d8239bae0bd158d'
api_secret = 'e053e6ff070a9f4b6881457848b47bac4e1c03b41b9ad2f8f2fa9a7b25e81559'

client = Client(api, api_secret, tld="com", testnet=True)

## trading parameters (optimal)
symbol = "BTCUSDT"
volume = 0.01
no_of_decimals = 1
no_of_cycles = 10
initial_deviation = -0.05
step = 1.2
no_of_safty_orders = 6
volume_multiplier = 2
direction = "LONG"
tp = 3

## fetch current account balance
def get_balance():
    x = client.futures_account()
    df = pd.DataFrame(x['assets'])
    print(df)

## placing market orders
def market_order(symbol,side,quantity):
    if side == "LONG":
        output=client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(output)

    if side == "SHORT":
        output=client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print(output)

def get_market_price(symbol):
    response = requests.get(f'https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}')
    price = float(response.json()['price'])
    return price

## streaming price (when trading with real account)
def get_market_price_real(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    return float(price["price"])

## calcutating the Price Deviation
def cal_deviation(direction,intial_price,current_price):
    dev = ((current_price-intial_price)/intial_price)*100
    if direction == "LONG":
        return dev
    if direction == "SHORT":
        return dev * -1

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

## calculate take profit price
def cal_tp_level(symbol,tp,no_of_decimals):
    try:
        ## details of all running positions
        x = client.futures_position_information(symbol=symbol)
        df = pd.DataFrame(x)
        
        ## remove the null positions
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
def place_tp(symbol,price,t_position_amt,direction):
    try:
        if direction == "LONG":
            sell_limit(symbol,t_position_amt,price)
        if direction == "SHORT":
            buy_limit(symbol, t_position_amt, price)
    except:
        place_tp(symbol, price, t_position_amt, direction)

## closing buy limit orders
def close_buy_limit(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"] == "BUY"]
    for index in df.index:
        client.futures_cancel_order(symbol=symbol,orderId = df["orderId"][index])

## closing sell limit orders
def close_sell_limit(symbol):
    x = client.futures_get_open_orders(symbol=symbol)
    df = pd.DataFrame(x)
    df = df[df["side"] == "SELL"]
    for index in df.index:
        client.futures_cancel_order(symbol=symbol,orderId = df["orderId"][index])

## driver code
for i in range(no_of_cycles):
    is_ok = True
    while is_ok:
        market_order(symbol,direction,volume)
        initial_price = get_market_price(symbol)
        x = client.futures_position_information(symbol=symbol)
        df = pd.DataFrame(x)
        t_margin = float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0])) / float(df["leverage"][0])

        if t_margin < 0 or t_margin > 0:
            curr_no_of_safty_orders = 0
            multiplied_volume = volume * volume_multiplier
            deviation = initial_deviation
            next_price_level = initial_deviation

            price0,amount0 = cal_tp_level(symbol,tp,no_of_decimals)
            place_tp(symbol,price0,amount0,direction)

            while is_ok:
                curr_price = get_market_price(symbol)
                curr_deviation = cal_deviation(direction,initial_price,curr_price)
                if curr_deviation <= next_price_level:
                    if curr_no_of_safty_orders < no_of_safty_orders:
                        market_order(symbol,direction,multiplied_volume)
                        multiplied_volume *= volume_multiplier
                        deviation *= step
                        next_price_level += deviation
                        curr_no_of_safty_orders += 1

                try:
                    price1, amount1 = cal_tp_level(symbol, tp, no_of_decimals)
                    x = client.futures_get_open_orders(symbol=symbol)
                    df = pd.DataFrame(x)
                    if len(df) == 0:
                        place_tp(symbol, price1, amount1, direction)
                    if price1 != price0 or amount1 != amount0:
                        if direction == "LONG":
                            close_sell_limit(symbol)
                        if direction == "SHORT":
                            close_buy_limit(symbol)
                        place_tp(symbol, price1, amount1, direction)
                        price0 = price1
                        amount0 = amount1
                except:
                    pass

                x = client.futures_position_information(symbol=symbol)
                df = pd.DataFrame(x)
                t_margin = float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0])) / float(df["leverage"][0])
                if t_margin == 0:
                    is_ok = False
