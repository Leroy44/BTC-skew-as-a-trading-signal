import requests
import json
import pandas as pd
import datetime
from pathlib import Path

#open bitcoin spot data file, add headers, make into df
csv_path=Path(r"C:\Users\Ling Zhou\Desktop\project2data\BTC_1hour.txt")
btc_df=pd.read_csv(csv_path, index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","btc_close", "btc_volume"])


#open spot data other files + add headers. open/high/low columns will be dropped so no need for unique identifiers, make into df
eth_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\ETH_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","eth_close", "eth_volume"])
dxy_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\eth_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","dxy_close", "dxy_volume"])
es_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\ES_continuous_adjusted_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","es_close", "es_volume"])
gc_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\GC_continuous_adjusted_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","gc_close", "gc_volume"])
nq_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\NQ_continuous_adjusted_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","nq_close", "nq_volume"])
us_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\US_continuous_adjusted_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","us_close", "us_volume"])
#eth_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\eth_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","close", "volume"])
#eth_df=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\eth_1hour.txt"), index_col= "date", infer_datetime_format= True, parse_dates=True,names=["date", "open", "high","low","close", "volume"])

#open vol/skew data, make into df
btc_skew=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\btc_skew_1hr.csv"), index_col= "date", infer_datetime_format= True, parse_dates=True)
btc_vol=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\btc_vol_1hr.csv"), index_col= "date", infer_datetime_format= True, parse_dates=True)
eth_skew=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\eth_skew_1hr.csv"), index_col= "date", infer_datetime_format= True, parse_dates=True)
eth_vol=pd.read_csv(Path(r"C:\Users\Ling Zhou\Desktop\project2data\eth_vol_1hr.csv"), index_col= "date", infer_datetime_format= True, parse_dates=True)

#create dictionary and add all spot data
df_dict=[]
df_dict.append(btc_df)
df_dict.append(eth_df)
df_dict.append(dxy_df)
df_dict.append(es_df)
df_dict.append(gc_df)
df_dict.append(us_df)

#create main_df used to aggregate all data
main_df= pd.DataFrame()

#loop through dictionary, deleting open, high, low columns. Join using "outer" (union) so that no data is lost.

for df in df_dict:
    del df["open"]
    del df["high"]
    del df["low"]
    main_df=main_df.join(df,how="outer")

#rename vol/skew data to differentiate between btc/eth data
btc_skew.columns = ["btc_"+col_name for col_name in btc_skew.columns]
btc_vol.columns = ["btc_"+col_name for col_name in btc_vol.columns]
eth_skew.columns = ["eth_"+col_name for col_name in eth_skew.columns]
eth_vol.columns = ["eth_"+col_name for col_name in eth_vol.columns]

#join vol/skew dfs to main_df. 
main_df=main_df.join(btc_skew,how="outer")
main_df=main_df.join(btc_vol,how="outer")
main_df=main_df.join(eth_skew,how="outer")
main_df=main_df.join(eth_vol,how="outer")

#save main_df as csv
main_df.to_csv(Path(r"C:\Users\Ling Zhou\Desktop\all_data.csv"))
