## import the libraries
import MetaTrader5 as mt5
import pandas as pd

## trading parameters
n = 10
symbol = "GBPUSD"
volume = 0.01
profit_target = 2
proportion = 2  ## specific number to multiply gap between limit orders

## connect with python
mt5.initialize(login = 51386052, server = "ICMarketsSC-Demo", password ="8ZahZUPE")


## placing buy limit order
def buy_limit(symbol, volume, price):
    request = mt5.order_send({
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY_LIMIT,
        "price": price,
        "deviation": 20,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    })

    print(request)


## placing sell limit order
def sell_limit(symbol, volume, price):
    request = mt5.order_send({
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "price": price,
        "deviation": 20,
        "magic": 100,
        "comment": "python market order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    })

    print(request)

## function to calculate the total profit
def cal_profit(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    profit = float(df["profit"].sum())
    return profit

## function to calculate the total volume
def cal_volume(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    volume = float(df["volume"].sum())
    return volume

## function to calculate the profit for buy position
def cal_buy_profit(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    df = df.loc[df.type == 0]
    profit = float(df["profit"].sum())
    return profit

## function to calculate the profit for sell position
def cal_sell_profit(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    df = df.loc[df.type == 1]
    profit = float(df["profit"].sum())
    return profit

## function to calculate the total margin for buy position
def cal_buy_margin(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    df = df.loc[df.type == 0]

    sum = 0
    for i in df.index:
        volume = df.volume[i]
        open_price = df.price_open[i]
        margin = mt5.order_calc_margin(mt5.ORDER_TYPE_BUY, symbol, volume, open_price)
        sum += margin
    return sum

## function to calculate the total margin for sell position
def cal_sell_margin(symbol):
    usd_positions = mt5.positions_get(symbol = symbol)
    df = pd.DataFrame(list(usd_positions), columns = usd_positions[0]._asdict().keys())
    df['time'] = pd.to_datetime(df['time'], unit = 's')
    df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis = 1, inplace = True)
    df = df.loc[df.type == 1]

    sum = 0
    for i in df.index:
        volume = df.volume[i]
        open_price = df.price_open[i]
        margin = mt5.order_calc_margin(mt5.ORDER_TYPE_SELL, symbol, volume, open_price)
        sum += margin
    return sum

## function to calculate the percentage profit for buy position
def cal_pct_buy_profit(symbol):
    profit = cal_buy_profit(symbol)
    margin = cal_buy_margin(symbol)
    pct = (profit/margin) * 100
    return pct

## function to calculate the percentage profit for sell position
def cal_pct_sell_profit(symbol):
    profit = cal_sell_profit(symbol)
    margin = cal_sell_margin(symbol)
    pct = (profit/margin) * 100
    return pct

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

## function to close all positions
def close_all(symbol):
    positions = mt5.positions_get(symbol = symbol)
    for position in positions:
        close_position(position)

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
    orders = mt5.orders_get(symbol = symbol)
    df = pd.DataFrame(list(orders), columns = orders[0]._asdict().keys())
    df.drop(['time_done', 'time_done_msc', 'position_id', 'position_by_id', 'reason', 'volume_initial', 'price_stoplimit'], axis = 1, inplace = True)
    df['time_setup'] = pd.to_datetime(df['time_setup'], unit = 's')
    for ticket in df.ticket:
        delete_pending(ticket)

## driver code
while True:
    pct_change = 1
    tick = mt5.symbol_info_tick(symbol)
    current_price_sell = tick.bid
    adj_sell = 1.2  ## to increase gap between limit orders in each iteration

    for i in range(n):
        price = ((pct_change / (100 * 100)) * current_price_sell) * adj_sell * proportion + current_price_sell
        sell_limit(symbol, volume, price)
        pct_change += 1
        adj_sell += 0.2

    pct_change_2 = -1
    tick = mt5.symbol_info_tick(symbol)
    current_price_buy = tick.ask
    adj_buy = 1.2

    for i in range(n):
        price = ((pct_change_2/(100 * 100)) * current_price_buy) * adj_buy * proportion + current_price_buy
        buy_limit(symbol, volume, price)
        pct_change_2 -= 1
        adj_buy += 0.2

    while True:
        position = mt5.positions_get(symbol = symbol)
        if len(position) > 0:
            margin_s = cal_sell_margin(symbol)
            margin_b = cal_buy_margin(symbol)

            if margin_s > 0:
                pct_sell_profit = cal_pct_sell_profit(symbol)
                if pct_sell_profit >= profit_target:
                    close_all(symbol)

            if margin_b > 0:
                pct_buy_profit = cal_pct_buy_profit(symbol)
                if pct_buy_profit >= profit_target:
                    close_all(symbol)

            position = mt5.positions_get(symbol = symbol)
            if len(position) == 0:
                close_limit(symbol)
                break