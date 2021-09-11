import pyupbit
import pandas 
import datetime 
import time

access = "Na3YushCGAt3J38IBxYdEWRDAUwRf09jBkp62R5d"
secret = "3hodIVP9SjZGmTIgmfx4h9tVLtpjoXxY1r7hsyxl"
upbit = pyupbit.Upbit(access, secret)

def rsi(ohlc: pandas.DataFrame, period: int = 14): 
    delta = ohlc["close"].diff() 
    ups, downs = delta.copy(), delta.copy() 
    ups[ups < 0] = 0 
    downs[downs > 0] = 0 
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD 
    
    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

def buy(coin): 
    money = upbit.get_balance("KRW") 
    if money < 5000000 : 
        res = upbit.buy_market_order(coin, money) 
    elif money < 10000000: 
        res = upbit.buy_market_order(coin, money*0.4) 
    elif money < 15000000 : 
        res = upbit.buy_market_order(coin, money*0.3) 
    else : 
        res = upbit.buy_market_order(coin, money*0.2) 
    return

def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    if total < 100000000 : 
        res = upbit.sell_market_order(coin, amount) 
    else : 
        res = upbit.sell_market_order(coin, amount*0.5)
    return

item_list = pyupbit.get_tickers(fiat="KRW")
print(item_list)

for i in range(len(item_list)):
    print(i, item_list[i])
    
lower22 = [] 
higher75 = [] 

while(True): 
    for i in range(len(item_list)): 
        lower22.append(False) 
        higher75.append(False)
        data = pyupbit.get_ohlcv(ticker=item_list[i], interval="minute3") 
        now_rsi = rsi(data, 14).iloc[-1] 
        print("코인명: ", item_list[i]) 
        print("현재시간: ", datetime.datetime.now()) 
        print("RSI :", now_rsi) 
        print() 
        if now_rsi <= 22 : 
            lower22[i] = True 
        elif now_rsi >= 24 and lower22[i] == True: 
            buy(item_list[i]) 
            lower22[i] = False 
        elif now_rsi >= 73 and higher75[i] == False: 
            sell(item_list[i]) 
            higher75[i] = True 
        elif now_rsi <= 70 : higher75[i] = False
        time.sleep(0.05)