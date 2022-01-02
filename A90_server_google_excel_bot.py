import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
import pytz
import requests
from smartapi import SmartConnect

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("keys.json",scope)
client = gspread.authorize(creds)


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

checking = obj.ltpData(exchange='NFO', tradingsymbol='NIFTY26AUG21FUT', symboltoken='49939')['data']['ltp']

while datetime.time(datetime.now(pytz.timezone('Asia/Kolkata'))) < today3pm:
    time.sleep(1800)
    # getting the live data
    nifty = obj.ltpData(exchange='NFO', tradingsymbol='NIFTY26AUG21FUT', symboltoken='49939')['data']['ltp']
    time.sleep(1)
    banknifty = obj.ltpData(exchange='NFO', tradingsymbol='BANKNIFTY26AUG21FUT', symboltoken='49937')['data']['ltp']

    if checking == nifty:
        break

    # current time
    current_time = datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%I:%M:%S')

    nbuy_sheet = client.open("A90 Book").worksheet('N BUY')
    nsell_sheet = client.open("A90 Book").worksheet('N SELL')

    bn_pl = (float(nbuy_sheet.cell(3, 2).value) - banknifty) * 25
    nif_pl = (nifty - float(nbuy_sheet.cell(2, 2).value)) * 50
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
    nbuy_sheet.append_row([str(date.today()), str(current_time), banknifty, nifty, bn_pl, nif_pl, Sum])

    # calculating the profit and loss for N SELL trade
    bn_pl = (banknifty - float(nsell_sheet.cell(3, 2).value)) * 25
    nif_pl = (float(nsell_sheet.cell(2, 2).value) - nifty) * 50
    Sum = bn_pl + nif_pl

    # appending data in N SELL
    nsell_sheet.append_row([str(date.today()), str(current_time), banknifty, nifty, bn_pl, nif_pl, Sum])





