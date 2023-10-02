## import the libraries
import MetaTrader5 as mt5
import pandas as pd

## trading parameters
symbol = "GBPUSD"
volume = 0.01
profit_target = 2
no_of_safty_orders = 3
direction = "sell"

## connect with python
mt5.initialize(login = 51386052, server = "ICMarketsSC-Demo", password ="8ZahZUPE")

## placing market orders
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

## function to calculate the percentage profit
def cal_pct_profit(symbol):
    total_profit = cal_profit(symbol)
    buy_margin = cal_buy_margin(symbol)
    sell_margin = cal_sell_margin(symbol)
    total_margin = buy_margin + sell_margin
    pct_profit = (total_profit/total_margin) * 100
    return pct_profit

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

## function to calculate current price deviation
def cal_curr_price_deviation(symbol):
    positions = mt5.positions_get(symbol = symbol)
    position = positions[len(positions) - 1]
    initial_price = position.price_open
    current_price = mt5.symbol_info_tick(symbol).ask
    deviation = ((current_price - initial_price)/initial_price) * 100 * 100
    if direction == "buy":
        return deviation
    if direction == "sell":
        return deviation * -1

## driver code
while True:
    market_order(symbol, volume, direction)
    pos = mt5.positions_get(symbol = symbol)
    if len(pos) > 0:
        curr_no_of_safty_orders = 0
        multiplied_volume = volume * 2
        deviation = -1
        next_price_level = -1

        is_ok = True
        while is_ok:
            curr_price_deviation = cal_curr_price_deviation(symbol)
            if curr_price_deviation <= next_price_level:
                if curr_no_of_safty_orders < no_of_safty_orders:
                    market_order(symbol, multiplied_volume, direction)
                    multiplied_volume *= 2
                    deviation *= 2
                    next_price_level += deviation
                    curr_no_of_safty_orders += 1

            pct_profit = cal_pct_profit(symbol)
            if pct_profit >= profit_target:
                close_all(symbol)
                is_ok = False