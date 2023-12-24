## import the libraries
from binance.client import Client
import pandas as pd
import requests

## connect with python
api = '33ced6236b5dcc64077883472fd37a3aae566b82c13008468d8239bae0bd158d'
api_secret = 'e053e6ff070a9f4b6881457848b47bac4e1c03b41b9ad2f8f2fa9a7b25e81559'

client = Client(api,api_secret,tld="com",testnet=True)


class Bot:
    def __init__(self,symbol,volume,no_of_decimals,no_of_cycles,initial_deviation,step,no_of_safty_orders,volume_multiplier,direction,tp):
        self.symbol = symbol
        self.volume = volume
        self.no_of_decimals = no_of_decimals
        self.no_of_cycles = no_of_cycles
        self.initial_deviation = initial_deviation
        self.step = step
        self.no_of_safty_orders = no_of_safty_orders
        self.volume_multiplier = volume_multiplier
        self.direction = direction
        self.tp = tp

    ## fetch current account balance
    def get_balance(self):
        x = client.futures_account()
        df = pd.DataFrame(x['assets'])
        print(df)

    ## placing market orders
    def market_order(self,symbol,side,quantity):
        if side == "LONG":
            output = client.futures_create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(output)

        if side == "SHORT":
            output = client.futures_create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
            print(output)

    def get_market_price(self,symbol):
        response = requests.get(f'https://testnet.binancefuture.com/fapi/v1/ticker/price?symbol={symbol}')
        price = float(response.json()['price'])
        return price

    ## streaming price (when trading with real account)
    def get_market_price_real(self,symbol):
        price = client.get_symbol_ticker(symbol=symbol)
        return float(price["price"])

    ## calcutating the Price Deviation
    def cal_deviation(self,direction, intial_price, current_price):
        dev = ((current_price - intial_price) / intial_price) * 100
        if direction == "LONG":
            return dev
        if direction == "SHORT":
            return dev * -1

    ## placing buy limit order
    def buy_limit(self,symbol,quantity,price):
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
    def sell_limit(self,symbol,quantity,price):
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
    def cal_tp_level(self,symbol,tp,no_of_decimals):
        try:
            x = client.futures_position_information(symbol=symbol)
            df = pd.DataFrame(x)
            df = df.loc[df["positionAmt"] != "0.000"]
            t_margin = (float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0]))) / float(df["leverage"][0])
            profit = float(t_margin * tp * 0.01)
            price = round((profit / float(df["positionAmt"][0])) + float(df["entryPrice"][0]), no_of_decimals)
            t_position_amt = 0
            for index in df.index:
                t_position_amt += abs(float(df["positionAmt"][index]))
            return price, t_position_amt

        except:
            pass

    ## placing take profit order
    def place_tp(self,symbol,price,t_position_amt,direction):
        try:
            if direction == "LONG":
                self.sell_limit(symbol, t_position_amt, price)
            if direction == "SHORT":
                self.buy_limit(symbol, t_position_amt, price)
        except:
            self.place_tp(symbol, price, t_position_amt, direction)

    ## closing buy limit orders
    def close_buy_limit(self,symbol):
        x = client.futures_get_open_orders(symbol=symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "BUY"]
        for index in df.index:
            client.futures_cancel_order(symbol=symbol, orderId=df["orderId"][index])

    ## closing sell limit orders
    def close_sell_limit(self,symbol):
        x = client.futures_get_open_orders(symbol=symbol)
        df = pd.DataFrame(x)
        df = df[df["side"] == "SELL"]
        for index in df.index:
            client.futures_cancel_order(symbol=symbol, orderId=df["orderId"][index])

    ## driver code
    def run(self):
        for i in range(self.no_of_cycles):
            is_ok = True
            while is_ok:
                self.market_order(self.symbol,self.direction,self.volume)
                initial_price = self.get_market_price(self.symbol)
                x = client.futures_position_information(symbol=self.symbol)
                df = pd.DataFrame(x)
                t_margin = float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0])) / float(df["leverage"][0])

                if t_margin < 0 or t_margin > 0:
                    curr_no_of_safty_orders = 0
                    multiplied_volume = self.volume * self.volume_multiplier
                    deviation = self.initial_deviation
                    next_price_level = self.initial_deviation

                    price0, amount0 = self.cal_tp_level(self.symbol,self.tp,self.no_of_decimals)
                    self.place_tp(self.symbol, price0, amount0, self.direction)

                    while is_ok:
                        curr_price = self.get_market_price(self.symbol)
                        curr_deviation = self.cal_deviation(self.direction, initial_price, curr_price)
                        if curr_deviation <= next_price_level:
                            if curr_no_of_safty_orders < self.no_of_safty_orders:
                                self.market_order(self.symbol, self.direction, multiplied_volume)
                                multiplied_volume *= self.volume_multiplier
                                deviation *= self.step
                                next_price_level += deviation
                                curr_no_of_safty_orders += 1

                        try:
                            price1, amount1 = self.cal_tp_level(self.symbol,self.tp,self.no_of_decimals)
                            x = client.futures_get_open_orders(symbol=self.symbol)
                            df = pd.DataFrame(x)
                            if len(df) == 0:
                                self.place_tp(self.symbol, price1, amount1, self.direction)
                            if price1 != price0 or amount1 != amount0:
                                if self.direction == "LONG":
                                    self.close_sell_limit(self.symbol)
                                if self.direction == "SHORT":
                                    self.close_buy_limit(self.symbol)
                                self.place_tp(self.symbol, price1, amount1, self.direction)
                                price0 = price1
                                amount0 = amount1
                        except:
                            pass

                        x = client.futures_position_information(symbol=self.symbol)
                        df = pd.DataFrame(x)
                        t_margin = float(df["entryPrice"][0]) * abs(float(df["positionAmt"][0])) / float(df["leverage"][0])
                        if t_margin == 0:
                            is_ok = False