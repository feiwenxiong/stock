# import tkinter as tk
# from pandastable import Table
# import pandas as pd

# # 初始化窗口
# root = tk.Tk()
# frame = tk.Frame(root)
# frame.pack(fill="both", expand=True)

# # 创建初始 DataFrame
# dfp = pd.DataFrame({
#     'A': [1, 2, 3],
#     'B': [4, 5, 6]
# })

# # 创建 pandastable.Table 实例
# pt = Table(frame, dataframe=dfp, showtoolbar=True, showstatusbar=True, width=1080, height=520)
# pt.show()

# def add_column_and_update_table():
#     global dfp, pt
#     # 示例：添加新列
    
#     import time
#     time.sleep(5)
#     # 刷新表格
#     new_column_name = 'C'
#     column_values = [7, 8, 9]
#     # 向 DataFrame 添加新列
#     dfp[new_column_name] = column_values
#     time.sleep(2)
#     pt.model.df = pd.DataFrame()  # 更新 model 中的 DataFrame
#     pt.redraw()  # 重新绘制表格



# # 调用函数添加新列并刷新表格
# import threading

# threading.Thread(target=add_column_and_update_table,).start()

# root.mainloop()

import akshare as ak
from datetime import datetime
import pandas as pd
from utils import *

'''
测试日期套利
'''
current_date = closest_trade_date()
current_date = datetime.strptime(current_date,"%Y%m%d")
tool_trade_date_hist_df = ak.tool_trade_date_hist_sina()
tool_trade_date_hist_df["trade_date"] = pd.to_datetime(tool_trade_date_hist_df["trade_date"])
periods = [ x * 15 for x in range(1,10)]
symbol = "003021"
def get_taoli_weekday(symbol,tool_trade_date_hist_df,current_date,period):
    nearest_dates = tool_trade_date_hist_df[tool_trade_date_hist_df["trade_date"] <= current_date].iloc[-period:]
    tmp = pd.DataFrame(pd.to_datetime(nearest_dates["trade_date"])).reset_index(drop=True)
    tmp["weekday"] = tmp["trade_date"].dt.weekday + 1
    tmp["trade_date_str"] = tmp["trade_date"].dt.strftime("%Y%m%d")
    # print(tmp)
    tmp.iloc[0]
    # 设置查询的起始日期和结束日期  
    start_date = tmp["trade_date_str"].iloc[0]  # 示例起始日期  
    end_date = tmp["trade_date_str"].iloc[-1]   # 示例结束日期  
    
    # 获取沪深300指数的日K线数据  
    # stock_zh_a_hist
    # index_zh_a_hist
    df = ak.stock_zh_a_hist(symbol=symbol, 
                            period='daily', 
                            start_date=start_date, 
                            end_date=end_date)  

    df["日期"] = pd.to_datetime(df["日期"])

    df = pd.merge(tmp,df,left_on="trade_date",right_on="日期",how='left')
    # 查看数据  
    df["隔日套利"] = (df["开盘"] - df["收盘"].shift(1)) / df["收盘"].shift(1)
    df["taoli"] = df["隔日套利"].apply(lambda x: 1 if x > 0 else 0)
    df = df.fillna(0)
    # print(df.head())


    t = df.groupby("weekday")["taoli"].sum() / df.groupby("weekday")["taoli"].count()
    # t = df.groupby("weekday")["隔日套利"].sum()
    t = pd.DataFrame(t)
    t["count"] =  df.groupby("weekday")["taoli"].count()
    t["huolirate"] = df.groupby("weekday")["隔日套利"].sum()
    # print(t)
    return t

trends = {x :[] for x in range(1,6)}
trends1 = {x :[] for x in range(1,6)}
for period in periods:
    t = get_taoli_weekday(symbol,tool_trade_date_hist_df,current_date,period)
    for i in t.index:
        trends[i].append(t.loc[i]["taoli"])
        trends1[i].append(t.loc[i]["huolirate"])
    
        



import matplotlib.pyplot as plt
plt.subplot(211)
plt.title(f"code:{symbol} | sell with open price's winrate")
for weekday in trends:
    plt.plot(periods,trends[weekday],label=f"weekday: {weekday}")
plt.legend()
plt.grid()
# plt.show()
plt.subplot(212)
plt.title(f"code:{symbol} | sell with open price's huolirate")
for weekday in trends1:
    plt.plot(periods,trends1[weekday],label=f"weekday: {weekday}")
plt.legend()
plt.grid()
plt.tight_layout()

plt.show()





