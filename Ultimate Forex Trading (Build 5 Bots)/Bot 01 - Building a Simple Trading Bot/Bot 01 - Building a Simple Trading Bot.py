## import the libraries
import MetaTrader5 as mt5
import pandas as pd

## connect with python
mt5.initialize(login = 51386052, server = "ICMarketsSC-Demo", password ="8ZahZUPE")

## trading parameters
symbol = "GBPUSD"
sma_period = 14
timeframe = mt5.TIMEFRAME_M1
volume = 0.05

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
def cal_direction(symbol, sma_period, timeframe):
    candles = mt5.copy_rates_from_pos(symbol, timeframe, 1, sma_period)
    candles_df = pd.DataFrame(candles)
    ## closing price of the last candle
    last_close = candles_df.iloc[-1].close
    ## simple moving average
    sma = candles_df.close.mean()
    if last_close > sma:
        return "buy"
    if last_close < sma:
        return "sell"
    if last_close == sma:
        return "neutral"


## driver code
while True:
    direction = cal_direction(symbol, sma_period, timeframe)

    ## if direction is buy, close the sell positions and if there are no positions, we have to place a buy order
    if direction == "buy":
        for position in mt5.positions_get(symbol=symbol):
            if position.type == 1:
                close_position(position)
        if not mt5.positions_total():
            market_order(symbol, volume, direction)

    ## if direction is sell, close the buy positions and if there are no positions, we have to place a sell order
    if direction == "sell":
        for position in mt5.positions_get(symbol=symbol):
            if position.type == 0:
                close_position(position)
        if not mt5.positions_total():
            market_order(symbol, volume, direction)