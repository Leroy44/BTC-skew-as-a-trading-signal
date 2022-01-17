import requests
import json
import pandas as pd
import datetime
import time
from datetime import date
from pathlib import Path

#Data is limited to 30 requests per second (can only ping 30 days per second)
#Symbol: BTC (BTC/ETH)
#Interval: "1 minute" (5 minute, 15 minute, 30 minute , 1 hour, 4 hour, 12 hour, 1 day, 1 week) 

def gvol_delta_skew(ticker, interval):

  url = "https://app.pinkswantrading.com/graphql"

  #read secret key
  dfx=pd.read_csv(Path(r"C:\Users\zhoul\Desktop\Python Code\Keys\genesis.txt"), names=["key"])
  secretkey= dfx["key"][0]

  headers = {
    'x-oracle': secretkey,
    'Content-Type': 'application/json',
    'accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9'
  }

  #date in m/d/y format
  start = date.today() - datetime.timedelta(days=14)
  end = date.today()

  #set main_df to empty dataframe
  main_df= pd.DataFrame()

  #use loops to avoid hitting the data request limit
  for i in range(1000):

    if i == 0:
      startdate= start.strftime("%m/%d/%y")
      enddate=end.strftime("%m/%d/%y")
    else:
      end=start-datetime.timedelta(days=1)
      start=end-datetime.timedelta(days=14)
      startdate= start.strftime("%m/%d/%y")
      enddate=end.strftime("%m/%d/%y")

    #query sent to API
    payload="{\"query\":\"query ConstantMaturitySkew1Min($symbol: BTCOrETHEnumType, $dateStart: String, $dateEnd: String $interval: String){\\n  ConstantMaturitySkew1Min(symbol:$symbol, dateStart:$dateStart, dateEnd: $dateEnd interval: $interval) {\\n    date\\n    thirtyFiveDelta7DayExp\\n    twentyFiveDelta7DayExp\\n    fifteenDelta7DayExp\\n    fiveDelta7DayExp\\n    thirtyFiveDelta30DayExp\\n    twentyFiveDelta30DayExp\\n    fifteenDelta30DayExp\\n    fiveDelta30DayExp\\n    thirtyFiveDelta60DayExp\\n    twentyFiveDelta60DayExp\\n    fifteenDelta60DayExp\\n    fiveDelta60DayExp\\n    thirtyFiveDelta90DayExp\\n    twentyFiveDelta90DayExp\\n    fifteenDelta90DayExp\\n    fiveDelta90DayExp\\n    thirtyFiveDelta180DayExp\\n    twentyFiveDelta180DayExp\\n    fifteenDelta180DayExp\\n    fiveDelta180DayExp\\n }\\n}\\n\",\"variables\":{\"symbol\":\"" + ticker +"\",\"dateStart\":\" "+ startdate +"\",\"dateEnd\":\"" + enddate + "\",\"interval\":\""+ interval +"\"}}"

    response = requests.request("GET", url, headers=headers, data=payload)

    raw_data =response.json()
    #print(response.text)

    df= raw_data["data"]["ConstantMaturitySkew1Min"]
    df=pd.DataFrame(df)

    if df.empty:
      break

    #transform dates into correct format
    for i in range(len(df)):
      df["date"][i]=datetime.datetime.fromtimestamp(int(df["date"][i])/1000)

    df=df.set_index("date")
    main_df = pd.concat([main_df,df])

    time.sleep(1.5)

  return main_df

#Data is limited to 30 requests per second (can only ping 30 days per second)
#Symbol: BTC (BTC/ETH)
#Interval: "1 minute" (5 minute, 15 minute, 30 minute , 1 hour, 4 hour, 12 hour, 1 day, 1 week) 

def gvol_atm_vol(ticker, interval):

  url = "https://app.pinkswantrading.com/graphql"

  #read secret key
  dfx=pd.read_csv(Path(r"C:\Users\zhoul\Desktop\Python Code\Keys\genesis.txt"), names=["key"])
  secretkey= dfx["key"][0]

  headers = {
    'x-oracle': secretkey,
    'Content-Type': 'application/json',
    'accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9'
  }

  #date in m/d/y format
  start = date.today() - datetime.timedelta(days=14)
  end = date.today()

  #set main_df to empty dataframe
  main_df= pd.DataFrame()

  #use loops to avoid hitting the data request limit
  for i in range(1000):

    if i == 0:
      startdate= start.strftime("%m/%d/%y")
      enddate=end.strftime("%m/%d/%y")
    else:
      end=start-datetime.timedelta(days=1)
      start=end-datetime.timedelta(days=14)
      startdate= start.strftime("%m/%d/%y")
      enddate=end.strftime("%m/%d/%y")

    #query sent to API
    payload="{\"query\":\"query ConstantMaturityAtm1Min($symbol: BTCOrETHEnumType, $dateStart: String, $dateEnd: String $interval: String){\\n  ConstantMaturityAtm1Min(symbol:$symbol, dateStart:$dateStart, dateEnd: $dateEnd interval: $interval) {\\n    date\\n    atm7\\n    atm30\\n    atm60\\n    atm90\\n    atm180\\n }\\n}\\n\",\"variables\":{\"symbol\":\"" + ticker +"\",\"dateStart\":\" "+ startdate +"\",\"dateEnd\":\"" + enddate + "\",\"interval\":\""+ interval +"\"}}"
    
    response = requests.request("GET", url, headers=headers, data=payload)

    raw_data =response.json()
    #print(response.text)

    df= raw_data["data"]["ConstantMaturityAtm1Min"]
    df=pd.DataFrame(df)

    if df.empty:
      break

    #transform dates into correct format
    for i in range(len(df)):
      df["date"][i]=datetime.datetime.fromtimestamp(int(df["date"][i])/1000)

    df=df.set_index("date")
    main_df = pd.concat([main_df,df])

    time.sleep(1.5)

  return main_df