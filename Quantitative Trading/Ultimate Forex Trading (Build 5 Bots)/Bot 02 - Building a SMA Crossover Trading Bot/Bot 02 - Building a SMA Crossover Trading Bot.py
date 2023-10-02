## import the libraries
import MetaTrader5 as mt5
import pandas as pd

## trading parameters
symbol = "EURUSD"
sma_preiod_1 = 14
sma_period_2 = 20
timeframe = mt5.TIMEFRAME_M1
volume = 0.05

## connect with python
mt5.initialize(login = 51386052, server = "ICMarketsSC-Demo", password ="8ZahZUPE")

## function to place market order
def market_order(symbol, volume, order_type):
    tick = mt5.symbol_info_tick(symbol)
    order_dict = {'buy': 0, 'sell': 1}
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "deviation": 20,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    order_result = mt5.order_send(request)
    print(order_result)
    return order_result

## function to close a position
def close_position(position):
    tick = mt5.symbol_info_tick(position.symbol)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position.ticket,
        "symbol": position.symbol,
        "volume": position.volume,
        "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
        "price": tick.ask if position.type == 1 else tick.bid,
        "deviation": 20,
        "magic": 100,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    return result

## function to calculate the direction
def cal_direction(symbol, sma_period_1, sma_period_2, timeframe):
    candles1 = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period_1)
    candles_df_1 = pd.DataFrame(candles1)
    candles2 = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period_2)
    candles_df_2 = pd.DataFrame(candles2)
    sma1 = candles_df_1.close.mean()
    sma2 = candles_df_2.close.mean()
    if sma1 > sma2:
        return "buy"
    if sma1 < sma2:
        return  "sell"
    if sma1 == sma2:
        return "neutral"


## driver code
while True:
    direction = cal_direction(symbol, sma_preiod_1, sma_period_2, timeframe)
    if direction == "buy":
        for position in mt5.positions_get(symbol=symbol):
            if position.type == 1:
                close_position(position)
        if not mt5.positions_total():
            market_order(symbol, volume, direction)

    if direction == "sell":
        for position in mt5.positions_get(symbol=symbol):
            if position.type == 0:
                close_position(position)
        if not mt5.positions_total():
            market_order(symbol, volume, direction)