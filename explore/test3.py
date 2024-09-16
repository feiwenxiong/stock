# import requests
# from utils import getUserAgent
# import re
# import json
# import pandas as pd
# from matplotlib import pyplot as plt
# import time
# from datetime import datetime
# # import httpx
# import execjs 
# # from playwright.sync_api import sync_playwright 
# # class Ths:
# #     def __init__(self,headers,js_file):
# #         # self.cookies= cookies
# #         self.headers= headers
# #         with open(js_file,"r",encoding="utf-8") as f:
# #             js_code = f.read()
# #         print(js_code)
# #         self.ctx = execjs.compile(js_code)
    
# #     def get_page_data(self,url):
# #         time.sleep(1)
# #         url = "https://d.10jqka.com.cn/v4/time/bk_881156/last.js"
# #         self.headers["v"] = self.ctx.call("getV")
# #         print(self.headers["v"])
# #         resp = requests.get(url=url,headers=self.headers)
# #         print(resp.text)
# #         return resp.text
# # # explore\ths.js
# with open(r"explore\ths.js",encoding="utf-8") as f:
#     js_func = execjs.compile(f.read())
# print(js_func)
# v = js_func.call("get_cookie")
# # print(v)
# # cookies = { "v":v}
# headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#            "referer":"https://q.10jqka.com.cn/",
#            "host":"d.10jqka.com.cn",
#            "Connection":"keep-alive",
#            "Cache-Control":"max-age=0","v":v}
# # headers["cookie"] = "v=AyqrJjzuOAN6J7RvTyj4sRv-e5vJm671oB8imbTj1n0I58SFnCv-BXCvcquH"
# # Ths(headers,"explore/ths.js")
# # print(resp.text)

import akshare as ak
# print(ak.stock_board_industry_name_em())
stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
print(stock_board_industry_name_em_df)

stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol="保险")
print(stock_board_industry_cons_em_df)


stock_board_industry_hist_min_em_df = ak.stock_board_industry_hist_min_em(symbol="保险", period="1")
print(stock_board_industry_hist_min_em_df)


# 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0
stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001", start_date="2024-09-13 09:30:00", end_date="2024-09-13 15:00:00", period="1", adjust="")
print(stock_zh_a_hist_min_em_df)

