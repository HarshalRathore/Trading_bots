from smartapi import SmartConnect
from datetime import datetime
import time


def square_off_time_formatter():
    time = input("Enter square off time in HH:MM:SS format example 9:15:00 , 14:30:00\ndefault is 15:15:00.000.").split(':')
    now = datetime.time(datetime.today())
    a = int(time[0])
    b = int(time[1])
    c = int(time[2])
    if time:
        return now.replace(a, b, c, 0)
    else:
        return now.replace(15, 15, 00, 0)



if __name__ == '__main__':
    api_key = input("ENTER YOUR API KEY\t")
    user_id = input("ENTER YOUR CLIENT_ID\t")
    pwd = input("ENTER YOUR PASSWORD\t")

    angel = SmartConnect(api_key=api_key)
    time.sleep(1)
    data = angel.generateSession(user_id, pwd)
    time.sleep(1)
    refreshToken = angel.refresh_token
    time.sleep(1)
    feedToken = angel.getfeedToken()

    time.sleep(1)
    APT1 = angel.position()['data'][0]['avgnetprice']
    time.sleep(1)
    APT2 = angel.position()['data'][1]['avgnetprice']
    print(f'PREMIUM OF TRADE1 {APT1}\nPREMIUM OF TRADE2 {APT2}')
    time.sleep(1)
    Exchange = angel.position()['data'][0]['exchange']
    time.sleep(1)
    TradingSymbl1 = angel.position()['data'][0]['tradingsymbol']
    time.sleep(1)
    TradingSymbl2 = angel.position()['data'][1]['tradingsymbol']
    time.sleep(1)
    Token1 = angel.position()['data'][0]['symboltoken']
    time.sleep(1)
    Token2 = angel.position()['data'][1]['symboltoken']
    time.sleep(1)
    ProductType = angel.position()['data'][0]['producttype']

    print(f"TRACKING STRADELL OF INSTRUEMENT SYMBOL {angel.position()['data'][0]['tradingsymbol']} & {angel.position()['data'][1]['tradingsymbol']}")

    time.sleep(1)
    SLOT = angel.position()['data'][0]['lotsize'] * 25
    print(f'\nTOTAL SHORTED QUANTITY OF THE INSTRUMENT: {SLOT * 25}')

    TAP = APT1 + APT2
    print(f"\nCOMBINED PREMIUM OF THE TRADE IS: {TAP}")

    SL_PERCENTAGE = int(input('\nEnter stoploss percentage'))
    SL_TRAIL = int(input('\nEnter point for stop loss trailing'))
    SQ_TIME = square_off_time_formatter()
    SQ_PROFIT = int(input('\nEnter you\'r square off profit\nOtherwise Enter \'None\''))
    SL = (TAP * (SL_PERCENTAGE / 100) + TAP)


    while True:
        LTP_T1 = angel.ltpData(exchange=Exchange, tradingsymbol=TradingSymbl1, symboltoken=Token1)
        time.sleep(1)
        LTP_T2 = angel.ltpData(exchange=Exchange, tradingsymbol=TradingSymbl2, symboltoken=Token2)

        REL = LTP_T2 + LTP_T1

        if REL < TAP and TAP - REL >= SL_TRAIL:
            SL = (REL * (SL_PERCENTAGE / 100) + REL)
            print(f'current stoploss is at {SL}')

        if TAP - REL > 0:
            temp = TAP - REL
            PROFIT = temp * SLOT
            LOSS = 0
        else:
            temp = REL - TAP
            LOSS = temp * SLOT
            PROFIT = 0

        if SQ_TIME == datetime.time(datetime.now()) or SQ_PROFIT == PROFIT or REL == SL:
            if ProductType == "INTRADAY":
                orderparams1 = {
                    "variety": "NORMAL",
                    "tradingsymbol": TradingSymbl1,
                    "symboltoken": Token1,
                    "transactiontype": "BUY",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "quantity": SLOT,
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "price": "",
                    "squareoff": "0",
                    "stoploss": "0",
                }
                orderparams2 = {
                    "variety": "NORMAL",
                    "tradingsymbol": TradingSymbl2,
                    "symboltoken": Token2,
                    "transactiontype": "BUY",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "quantity": SLOT,
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "price": "",
                    "squareoff": "0",
                    "stoploss": "0",
                }
                order_id_1 = angel.placeOrder(orderparams1)
                time.sleep(1)
                order_id_2 = angel.placeOrder(orderparams2)
            if ProductType == "CARRYFORWARD":
                orderparams1 = {
                    "variety": "NORMAL",
                    "tradingsymbol": TradingSymbl1,
                    "symboltoken": Token1,
                    "transactiontype": "BUY",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "quantity": SLOT,
                    "producttype": "CARRYFORWARD",
                    "duration": "DAY",
                    "price": "",
                    "squareoff": "0",
                    "stoploss": "0",
                }
                orderparams2 = {
                    "variety": "NORMAL",
                    "tradingsymbol": TradingSymbl2,
                    "symboltoken": Token2,
                    "transactiontype": "BUY",
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "quantity": SLOT,
                    "producttype": "CARRYFORWARD",
                    "duration": "DAY",
                    "price": "",
                    "squareoff": "0",
                    "stoploss": "0",
                }
                order_id_1 = angel.placeOrder(orderparams1)
                time.sleep(1)
                order_id_2 = angel.placeOrder(orderparams2)
            if order_id_1 and order_id_2:
                print(datetime.time(datetime.now()))
                print(f'successfully placed sell orders for order ids {order_id_2} and {order_id_1}')
                print(f'calculated profit {PROFIT}\ncalculated loss {LOSS}')
            break
