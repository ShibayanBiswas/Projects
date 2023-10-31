"Saving Intraday Data, Generating Intraday Charts, Back Testing & Trade Simulation"

"Specific Functions"

# trade_data(token) -> Returns Intraday One Minute Candle data for specified Token on specified date.
# get_all_data() -> Writes Intraday One Minute Candle data to a file for all stocks specified on specified date.
# intraday_chart(token) -> Generates Intraday Chart for specified Token on specified date.

from SmartApi.smartConnect import SmartConnect
import os
import datetime as dt
from pyotp import TOTP
from matplotlib import pyplot as plt

key_path = r"C:\Users\SHIBAYAN BISWAS\Desktop\Angel_Smart_API_Electronic_Market_Making_Strategy"
os.chdir(key_path)
key_secret = open("key.txt","r").read().split()

obj=SmartConnect(api_key=key_secret[0])
data = obj.generateSession(key_secret[2],key_secret[3],TOTP(key_secret[4]).now())
feed_token = obj.getfeedToken()

#############################################################################################################
########################################## Generating Candle Data ###########################################
# Candle Data Format = [Time Stamp, Open, High, Low, Close, Volume]
# [['09:15', 853.65, 853.7, 850.05, 853.55, 242224], ['09:16', 853.45, 853.75, 852.25, 853.5, 139378],...]


stocks=["AXISBANK-EQ", "HDFCBANK-EQ", "ICICIBANK-EQ", "INFY-EQ", "ITC-EQ", "RELIANCE-EQ", "SBIN-EQ", "TATAMOTORS-EQ"]
tokens=["5900","1333","4963","1594","1660","2885","3045","3456"]

interval = "ONE_MINUTE"
start_date = "2023-04-13 09:15"  #Update to Intended Date & Start Time in the Format of "YYYY-MM-DD HH:MM"
end_date = "2023-04-13 15:29"    #Update to Intended Date & End Time in the Format of "YYYY-MM-DD HH:MM"

def trade_data(token):
    final_data=[]
    params = {
             "exchange": "NSE",
             "symboltoken": token,
             "interval": interval,
             "fromdate": start_date,
             "todate": end_date
             }
    candle_data = obj.getCandleData(params)
    final_data.append(candle_data["data"])
    final_data = final_data[0]
    pos = 0
    while pos< len(final_data):
        final_data[pos][0] = final_data[pos][0][11:]
        final_data[pos][0] = final_data[pos][0][:-9]
        pos+=1
    return final_data

print(trade_data(5900))


def get_all_data():
    for each_token in tokens:
        stock_pos = tokens.index(each_token)
        stock = stocks[stock_pos]
        final_data = trade_data(each_token)
        F_Name = f"{start_date[0:10]}"+".txt"
        File_Name = f"C:\\Users\\SHIBAYAN BISWAS\\Desktop\\Angel_Smart_API_Electronic_Market_Making_Strategy\{F_Name}"
        File = open(File_Name, "a+")
        File.write("--------------------------------------------------------------------------------")
        File.write("\n")
        File.write(str(start_date))
        File.write("\n")
        File.write(str(stock))
        File.write(":")
        File.write(str(each_token))
        File.write("\n")
        File.write(str(final_data))
        File.write("\n")
        File.write("--------------------------------------------------------------------------------")
        File.write("\n")
        File.write("\n")
        File.close()
        print("File Updated with Trade Data for", stock, ":", each_token, " : ", start_date)

get_all_data()


#########################################################################################
################################### Intraday Charts #####################################

def intraday_chart(token):
    stock_pos = tokens.index(token)
    stock = stocks[stock_pos]
    Trade_Data = trade_data(token)
    High_Low = []
    for each_candle in Trade_Data:
        Temp_High_Low=[]
        Temp_High_Low.append(each_candle[0])
        Temp_High_Low.append(each_candle[2])
        Temp_High_Low.append(each_candle[3])
        High_Low.append(Temp_High_Low)
    Mid_Price =[]
    for each_high_low in High_Low:
        Temp_Mid_Price=[]
        Temp_Mid_Price.append(each_high_low[0])
        each_mid_price = (each_high_low[1]+each_high_low[2])/2
        each_mid_price = round(each_mid_price * 2.0, 1) / 2.0
        Temp_Mid_Price.append(each_mid_price)
        Mid_Price.append(Temp_Mid_Price)
    Time = range(len(Mid_Price))
    Price = [y for x, y in Mid_Price]
    plt.plot(Time, Price)
    plt.xlabel('One Minute Candles')
    plt.ylabel('Stock Price')
    plt.title('Intraday Chart for: '+str(stock)+' : '+str(start_date[8:10])+str(start_date[4:8])+str(start_date[0:4]))
    plt.show()

intraday_chart('5900')


#####################################################################################################
######################################### Trade Simulator ###########################################

token = "5900"  # NEEDS INPUT
stock_pos = tokens.index(token)
stock = stocks[stock_pos]

Trade_Data = trade_data(token)

High_Low = []
for each_candle in Trade_Data:
    Temp_High_Low=[]
    Temp_High_Low.append(each_candle[0])
    Temp_High_Low.append(each_candle[2])
    Temp_High_Low.append(each_candle[3])
    High_Low.append(Temp_High_Low)

High = []
for each_candle in Trade_Data:
    Temp_High=[]
    Temp_High.append(each_candle[0])
    Temp_High.append(each_candle[2])
    High.append(Temp_High)

Low = []
for each_candle in Trade_Data:
    Temp_Low=[]
    Temp_Low.append(each_candle[0])
    Temp_Low.append(each_candle[3])
    Low.append(Temp_Low)

Mid_Price =[]
for each_high_low in High_Low:
    Temp_Mid_Price=[]
    Temp_Mid_Price.append(each_high_low[0])
    each_mid_price = (each_high_low[1]+each_high_low[2])/2
    each_mid_price = round(each_mid_price * 2.0, 1) / 2.0
    Temp_Mid_Price.append(each_mid_price)
    Mid_Price.append(Temp_Mid_Price)

Range = []
for each_range in High_Low:
    Temp_Range=[]
    Temp_Range.append(each_range[0])
    current_range = each_range[1]-each_range[2]
    current_range = round(current_range * 2.0, 1) / 2.0
    Temp_Range.append(current_range)
    Range.append(Temp_Range)

print(Trade_Data)
print(High_Low)
print(High)
print(Low)
print(Mid_Price)
print(Range)

sum = 0
for each in Range:
    sum = sum + each[1]
mean_range = sum / len(Range)
mean_range = round(mean_range * 2.0, 1) / 2.0
print('Mean Range Per Minute: ',mean_range)


"""
Algo Trade Simulation Code Below.
"""

Buy_Profit_Trades = 0
Sell_Profit_Trades = 0
Net_Position = 0
Flag = 0
pos = 0

Trade_Margin = 0.7  # NEEDS INPUT
Buy_Trade_Book =[]
Sell_Trade_Book= []

### Buy Trades Simulation

pos=0  # NEEDS INPUT -> Used to Define Algo Simulation Start Time
while pos < len(High_Low)-1:
    if Net_Position == 0 and Flag == 0:
        Buy_Price = Mid_Price[pos][1]-Trade_Margin
        Buy_Price = round(Buy_Price * 2.0, 1) / 2.0
        Sell_Price = Mid_Price[pos][1]+Trade_Margin
        Sell_Price = round(Sell_Price * 2.0, 1) / 2.0
        Flag = 1
    elif Net_Position == 0 and Flag == 1:
        if Low[pos][1] <= Buy_Price:
            Trade_Msg = " Buy Trade at: " +" "+  Low[pos][0] +" "+ str(Buy_Price)
            Buy_Trade_Book.append(Trade_Msg)
            Net_Position = 1
            Sell_Price = 0
            Take_Profit_Sell_Price = Buy_Price+Trade_Margin
            Flag = 2
    elif Net_Position == 1 and Flag == 2:
        if High[pos][1] >= Take_Profit_Sell_Price:
            Trade_Msg = " Take Profit Sell Executed at: " +" "+ High[pos][0] +" "+ str(Take_Profit_Sell_Price)
            Buy_Trade_Book.append(Trade_Msg)
            Net_Position = 0
            Buy_Profit_Trades += 1
            Take_Profit_Sell_Price = 0
            Flag = 0
    pos+=1


### Sell Trades Simulation
pos=0  # NEEDS INPUT -> Used to Define Algo Simulation Start Time
while pos < len(High_Low)-1:
    if Net_Position == 0 and Flag == 0:
        Buy_Price = Mid_Price[pos][1]-Trade_Margin
        Buy_Price = round(Buy_Price * 2.0, 1) / 2.0
        Sell_Price = Mid_Price[pos][1]+Trade_Margin
        Sell_Price = round(Sell_Price * 2.0, 1) / 2.0
        Flag = 1
    elif Net_Position == 0 and Flag == 1:
        if High[pos][1] >= Sell_Price:
            Trade_Msg = " Sell Trade at: " +" "+ High[pos][0] +" "+ str(Sell_Price)
            Sell_Trade_Book.append(Trade_Msg)
            Net_Position = -1
            Buy_Price = 0
            Take_Profit_Buy_Price = Sell_Price - Trade_Margin
            Flag = 2
    elif Net_Position == -1 and Flag == 2:
        if Low[pos][1] <= Take_Profit_Buy_Price:
            Trade_Msg = " Take Profit Buy Executed at: " +" "+ Low[pos][0] +" "+ str(Take_Profit_Buy_Price)
            Sell_Trade_Book.append(Trade_Msg)
            Net_Position = 0
            Sell_Profit_Trades += 1
            Take_Profit_Buy_Price = 0
            Flag = 0
    pos+=1


print("************************ Trade Simulation Results *********************************")

print('Total Profitable Buy Trades for: ',stock,": ",Buy_Profit_Trades)
print('Total Profitable Sell Trades for: ',stock,": ",Sell_Profit_Trades)
print(Buy_Trade_Book)
print(Sell_Trade_Book)

print("******************************* End of File ***************************************")
