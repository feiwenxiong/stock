# import akshare as ak
# stock_board_ths_df = ak.stock_board_concept_cons_ths(symbol_code="人脸识别")
# print(stock_board_ths_df)
# from zhangting import BlockTop
# import pandas as pd
# from datetime import datetime
# blocks = BlockTop().get_data_json(date="20240911",filt=1)["data"]
# print(blocks)
# t = []
# for block in blocks:
#     t.extend(block["stock_list"])
# t = pd.DataFrame(t)
# t["first_limit_up_time"] = t["first_limit_up_time"].map(int).map(datetime.fromtimestamp)
# t["last_limit_up_time"] = t["last_limit_up_time"].map(int).map(datetime.fromtimestamp)
# print(t)
# print(t.columns)
# -*- coding: utf-8 -*-
import requests
from utils import getUserAgent
import re
import json

url = f"https://d.10jqka.com.cn/v4/time/bk_885595/last.js"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
           "referer":"https://q.10jqka.com.cn/"}
headers["User-Agent"] = getUserAgent()

resp = requests.get(url,headers=headers)
print(resp.status_code)
if resp.status_code == 200:
    print(resp.text)

match = re.search(r'\((.*)\)', resp.text)

# 如果有匹配项，则提取括号内的内容
if match:
    params = match.group(1)
    print(f"括号内的内容: {params}")
else:
    print("没有找到匹配项")
    
t = json.loads(params)
print(t)
print(t["bk_885595"]["data"])