## import the libraries
from binance.client import Client
import pandas as pd
import requests

## connect with python
api = '33ced6236b5dcc64077883472fd37a3aae566b82c13008468d8239bae0bd158d'
api_secret = 'e053e6ff070a9f4b6881457848b47bac4e1c03b41b9ad2f8f2fa9a7b25e81559'

client = Client(api,api_secret,tld="com",testnet=True)


class Bot:
    def __init__(self,symbol,no_of_decimals,volume,proportion,tp,n):
        self.symbol = symbol
        self.no_of_decimals = no_of_decimals
        self.volume = volume
        self.proportion = proportion
        self.tp = tp
        self.n = n

    ## fetch current account balance
    def get_balance(self):
        x = client.futures_account()
        df = pd.DataFrame(x['assets'])
        print(df)

    ## streaming price
    def get_current_price(self,symbol):
        response = requests.get(f'https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}')
        price = float(response.json()['price'])
        return price

    ## placing sell limit order
    def sell_limit(self,symbol,volume,price):
        output = client.futures_create_order(

            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=volume,
            price=price,
        )
        print(output)

    ## placing buy limit order
    def buy_limit(self,symbol,volume,price):
        output = client.futures_create_order(

            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=volume,
            price=price,
        )
        print(output)

    ## closing all open orders
    def close_orders(self,symbol):
        x = client.futures_get_open_orders(symbol=symbol)
        df = pd.DataFrame(x)
        for index in df.index:
            client.futures_cancel_order(symbol=symbol, orderId=df["orderId"][index])

    ## closing buy orders
    def close_buy_orders(self,symbol):
        x = client.futures_get_open_orders(symbol=symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "BUY"]
        for index in df.index:
            client.futures_cancel_order(symbol=symbol, orderId=df["orderId"][index])

    ## closing sell orders
    def close_sell_orders(self,symbol):
        x = client.futures_get_open_orders(symbol=symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "SELL"]
        for index in df.index:
            client.futures_cancel_order(symbol=symbol, orderId=df["orderId"][index])

    ## getting direction of running positions
    def get_direction(self,symbol):
        x = client.futures_position_information(symbol=symbol)
        df = pd.DataFrame(x)
        if float(df["positionAmt"].sum()) > 0:
            return "LONG"
        if float(df["positionAmt"].sum()) < 0:
            return "SHORT"
        else:
            return "FLAT"

    ## getting the market price
    def get_mark_price(self,symbol):
        x = client.get_symbol_ticker(symbol=symbol)
        price = float(x["price"])
        return price

    ## placing orders like a grid
    def draw_grid(self,n):
        pct_change = 1
        adj_sell = 1.2
        current_price = self.get_mark_price(self.symbol)
        for i in range(n):
            sell_price = float(
                round(((pct_change / 100) * current_price * adj_sell * self.proportion) + current_price, self.no_of_decimals))
            self.sell_limit(self.symbol, self.volume, sell_price)
            pct_change += 1
            adj_sell += 0.2

        pct_change = -1
        adj_buy = 1.2
        current_price = self.get_mark_price(self.symbol)
        for i in range(n):
            buy_price = float(
                round(((pct_change / 100) * current_price * adj_sell * self.proportion) + current_price, self.no_of_decimals))
            self.buy_limit(self.symbol, self.volume, buy_price)
            pct_change -= 1
            adj_buy += 0.2

    ## calculate take profit price
    def cal_tp_level(self,symbol,tp):
        try:
            x = client.futures_position_information(symbol=symbol)
            df = pd.DataFrame(x)
            df = df.loc[df["positionAmt"] != "0.000"]
            t_margin = (float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0]))) / float(df["leverage"][0])
            profit = float(t_margin * tp * 0.01)
            price = round((profit / float(df["positionAmt"][0])) + float(df["entryPrice"][0]), self.no_of_decimals)
            t_position_amt = 0
            for index in df.index:
                t_position_amt += abs(float(df["positionAmt"][index]))
            return price, t_position_amt

        except:
            pass

    ## placing take profit order
    def place_tp_order(self,symbol,price,t_position_amt,direction):
        try:
            if direction == "LONG":
                self.sell_limit(symbol,t_position_amt,price)
            if direction == "SHORT":
                self.buy_limit(symbol,t_position_amt,price)
        except:
            self.place_tp_order(symbol,price,t_position_amt,direction)


    def run(self):
        while True:
            x = client.futures_get_open_orders(symbol=self.symbol)
            df1 = pd.DataFrame(x)
            if len(df1) == 0:
                self.draw_grid(self.n)
            y = client.futures_position_information(symbol=self.symbol)
            df2 = pd.DataFrame(y)
            df2 = df2.loc[df2["positionAmt"] != "0.000"]
            if len(df2) > 0:
                direction = self.get_direction(self.symbol)
                try:
                    if direction == "LONG":
                        print("close buy")
                        self.close_sell_orders(self.symbol)
                    if direction == "SHORT":
                        print("close sell")
                        self.close_buy_orders(self.symbol)
                except:
                    pass
                price0, amount0 = self.cal_tp_level(self.symbol, self.tp)
                self.place_tp_order(self.symbol, price0, amount0, direction)
                is_ok = True
                while is_ok:
                    try:
                        price1, amount1 = self.cal_tp_level(self.symbol, self.tp)
                        if price1 != price0 or amount1 != amount0:
                            if direction == "LONG":
                                self.close_sell_orders(self.symbol)
                            if direction == "SHORT":
                                self.close_buy_orders(self.symbol)
                            self.place_tp_order(self.symbol, price1, amount1, direction)
                            price0 = price1
                            amount0 = amount1
                    except:
                        pass

                    y = client.futures_position_information(symbol=self.symbol)
                    df2 = pd.DataFrame(y)
                    df2 = df2.loc[df2["positionAmt"] != "0.000"]
                    if len(df2) == 0:
                        try:
                            self.close_orders(self.symbol)
                            is_ok = False
                        except:
                            pass
