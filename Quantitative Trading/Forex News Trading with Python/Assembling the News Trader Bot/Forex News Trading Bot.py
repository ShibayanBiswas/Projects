## import the libraries
import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime

## connect with python
mt5.initialize(login = 51465332, server = "ICMarketsSC-Demo", password ="DjENd7ch")

## trading parameters
symbol = "EURUSD"
volume = 0.5
gap = 1.2
tp = 10
sl = 0.75
set = datetime(2024,1,3,20,30,0,100000)
timestamp_set = datetime.timestamp(set)

## placing buy stop orders with Take Profit and Stop Loss
def buy_stop(symbol,volume,price,tp,sl):
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY_STOP,
        "price":price,
        "deviation": 20,
        "tp":tp,
        "sl":sl,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    output = mt5.order_send(request)
    print(output)

## placing sell stop orders with Take Profit and Stop Loss
def sell_stop(symbol,volume,price,tp,sl):
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL_STOP,
        "price":price,
        "deviation": 20,
        "magic": 100,
        "tp":tp,
        "sl":sl,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    output = mt5.order_send(request)
    print(output)

def cal_levels(symbol,tp,gap):
    symbol_tick = mt5.symbol_info_tick(symbol)
    bid = symbol_tick.bid
    ask = symbol_tick.ask
    O = (bid+ask)/2
    H = ((ask * 1)/(100*100))*gap + ask
    L = ((bid * -1)/(100*100))*gap + bid
    sell_tp = O - tp * 0.0001
    buy_tp = O + tp * 0.0001
    return O,H,L,sell_tp,buy_tp

## calculating new stop loss
def cal_new_sl(symbol,initial_distance,buy_tp,sell_tp):
    positions = mt5.positions_get(symbol=symbol)
    position = positions[0]
    position_type = position.type
    price_current = position.price_current

    if position_type == 0:
        new_sl = price_current - initial_distance
        return new_sl,buy_tp
    if position_type == 1:
        new_sl = price_current + initial_distance
        return new_sl,sell_tp

def trail(symbol,initial_distance,new_sl,tp):
    positions = mt5.positions_get(symbol=symbol)
    position = positions[0]
    price_current = position.price_current

    current_sl = position.sl
    current_distance = abs(round(price_current - current_sl,6))

    if current_distance > initial_distance:
        request = {
            'action': mt5.TRADE_ACTION_SLTP,
            'position': position.ticket,
            'sl': new_sl,
            'tp': tp,
        }
        mt5.order_send(request)

## function to delete pending orders
def delete_pending(ticket):
    close_request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
    result = mt5.order_send(close_request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
            result_dict = result._asdict()
            print(result_dict)
    else:
        print('Delete complete...')

## function to close limit orders
def close_limit(symbol):
    orders = mt5.orders_get(symbol=symbol)
    df = pd.DataFrame(list(orders), columns=orders[0]._asdict().keys())
    df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial',
                 'price_stoplimit'], axis=1, inplace=True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit='s')
    for ticket in df.ticket:
        delete_pending(ticket)

## driver code
is_ok = True
while is_ok:
    now = datetime.now()
    timestamp_now = datetime.timestamp(now)
    if timestamp_now >= timestamp_set:
        orders = mt5.orders_get(symbol=symbol)
        if len(orders) == 0:
            O, H, L, sell_tp, buy_tp = cal_levels(symbol, tp, gap)
            sell_stop(symbol,volume,L,sell_tp,O + sl * (O - L))
            buy_stop(symbol,volume,H,buy_tp,O - sl * (O - L))

    positions = mt5.positions_get(symbol=symbol)
    if len(positions) > 0:
        positions = mt5.positions_get(symbol=symbol)
        position = positions[0]
        price_current = position.price_current

        current_sl = position.sl
        initial_distance = abs(round(price_current - current_sl, 6))
        orders = mt5.orders_get(symbol=symbol)
        if len(orders) > 0:
            close_limit(symbol)
        while True:
            positions = mt5.positions_get(symbol=symbol)
            if len(positions) > 0:
                new_sl,tp = cal_new_sl(symbol,initial_distance,buy_tp,sell_tp)
                trail(symbol,initial_distance,new_sl,tp)

            positions = mt5.positions_get(symbol=symbol)
            if len(positions) == 0:
                is_ok = False
                break