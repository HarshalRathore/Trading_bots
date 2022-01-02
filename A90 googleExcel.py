# !pip
# install
# smartapi - python
# !pip
# install
# websocket - client
# !pip
# install - -upgrade
# gspread

import time
from datetime import datetime, date
import pytz
import requests
from smartapi import SmartConnect
# from google.colab import auth
#
# auth.authenticate_user()
# import gspread
# from oauth2client.client import GoogleCredentials

# gc = gspread.authorize(GoogleCredentials.get_application_default())

obj = SmartConnect(api_key="FJ6CpKGH")
data = obj.generateSession("R433502", "dob310584")
refreshToken = data['data']['refreshToken']
feedToken = obj.getfeedToken()

active1 = True
active2 = True
active3 = True

api_url = 'https://api.telegram.org/bot1848268001:AAGJJhQF3dgm-0cWxUlDbKDc_YWKA9V6_Bk/sendMessage?chat_id=-1001540382926&text='

now = datetime.time(datetime.now())
today3pm = now.replace(hour=15, minute=30, second=00)


def SendMessage(mark, Sum):
    text = f'{mark} has been reached.\nCurrent : {Sum:.2f}\nInstruements: NIFTY26AUG21FUT, BANKNIFTY26AUG21FUT\nTrade: N BUY\nA90'
    requests.get(api_url + text)


while datetime.time(datetime.now(pytz.timezone('Asia/Kolkata'))) < today3pm:
    # getting the live data
    nifty = obj.ltpData(exchange='NFO', tradingsymbol='NIFTY26AUG21FUT', symboltoken='49939')['data']['ltp']
    banknifty = obj.ltpData(exchange='NFO', tradingsymbol='BANKNIFTY26AUG21FUT', symboltoken='49937')['data']['ltp']

    # current time
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S')

    # opening the workbook
    masterwb = gc.open('A90 Book')

    # creating variables to access the worksheets
    masterws1 = masterwb.worksheet('N BUY')
    masterws2 = masterwb.worksheet('N SELL')

    # calculating the profit and loss for N BUY trade
    bn_pl = (float(masterws1.acell('B3').value) - banknifty) * 25
    nif_pl = (nifty - float(masterws1.acell('B2').value)) * 50
    Sum = bn_pl + nif_pl

    # Here sending the telegram message
    if max(Sum, -Sum) >= 12000 or max(Sum, -Sum) >= 18000 or max(Sum, -Sum) >= 27000:
        if max(Sum, -Sum) >= 27000 and active1:
            SendMessage(27000, Sum)
            active1 = False
        elif max(Sum, -Sum) >= 18000 and max(Sum, -Sum) < 27000 and active2:
            SendMessage(18000, Sum)
            active2 = False
        elif max(Sum, -Sum) >= 12000 and max(Sum, -Sum) < 18000 and active3:
            SendMessage(12000, Sum)
            active3 = False

    # appending data in N BUY
    masterws1.append_row([str(date.today()), str(current_time), banknifty, nifty, bn_pl, nif_pl, Sum])

    # calculating the profit and loss for N SELL trade
    bn_pl = (banknifty - float(masterws1.acell('B3').value)) * 25
    time.sleep(2)
    nif_pl = (float(masterws1.acell('B2').value) - nifty) * 50
    Sum = bn_pl + nif_pl

    time.sleep(2)
    # appending data in N SELL
    masterws2.append_row([str(date.today()), str(current_time), banknifty, nifty, bn_pl, nif_pl, Sum])

    # childws1 = gc.open("A90 Book").worksheet('N BUY')
    # childws2 = gc.open("A90 Book").worksheet('N SELL')
    # rows1 = masterws1.get_all_values()
    # rows2 = masterws2.get_all_values()

    # childws1.update(f'A1:G{len(rows1)}', rows1)
    # childws2.update(f'A1:G{len(rows2)}', rows2)

    time.sleep(1800)