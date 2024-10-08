import os
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)
import akshare as ak
from utils import *
import requests as rq
import os
import pandas as pd
from datetime import timedelta
from hot_stock import *
import time
from lhb import yyb_stocks2stock_yybs 
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.live import Live
import select  # 确保导入 select 模块
import keyboard
import tkinter as tk
from pandastable import Table as Table2
import pandas as pd
from tkinter import ttk
pd.set_option('future.no_silent_downcasting', True)

class Continuous_limit_up(DataClass):
    
    def get_data_json(self,date,filt):
        '''
            date:20240726
        '''
        url = " https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up"
        match filt:
            case 0:
                # 沪深除了创科
                filt = "HS"
            case _:
                # + 创、科创
                filt = "HS,GEM2STAR"
        params = {"filter": filt,
                "date": date}
        headers = {
            "User-Agent":getUserAgent(),
            
            
        }
        url = "https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool"
        resp = rq.get(url, params=params,headers=headers)
        res = resp.json()
        return res

    
    def get_data_df(self,date,filt):
        data = self.get_data_json(date,filt)
        if data["status_code"]:
            return pd.DataFrame()
        return data["info"]
        
class LimitUpPool(DataClass):
    '''获取涨停的股票池
    '''

    
    def __init__(self):
        super().__init__()
        self.data_json = None
        
    def get_data_json(self,date):
        
        params = {
        "page": 1,
        "limit": 200,
        "field": "199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004",
        "filter": "HS,GEM2STAR",
        "order_field": "330324",
        "order_type": 0,
        "date": date,
        "_": 1722309210154
        }
        headers = {
            "User-Agent":getUserAgent(),
            
        }
        url = "https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool"
        resp = rq.get(url, params=params,headers=headers)
        res = resp.json()
        self.data_json = res
        return res

    def get_data_df(self,date,save=True):
        data = self.get_data_json(date)["data"]
        cols_cn = {
        "open_num":"开板次数",
        "first_limit_up_time" :"首次涨停时间",
        "last_limit_up_time":"最后涨停时间",
        "code":"代码",
        "limit_up_type":'涨停形态',
        "order_volume":"封单量",
        "is_new":'新上',
        "limit_up_suc_rate":"近一年涨停封板率",
        "currency_value":"流通市值",
        "is_again_limit":"是否连板",
        "change_rate":"涨幅",
        "turnover_rate":"换手率",
        "reason_type":"涨停原因",
        "order_amount":"封单额",
        "high_days":"几天几板",
        "name":"名称",
        "change_tag":"是否回封",
        "latest":"最新",
        "time_preview":"分时预览",}

        info = data["info"]
        info_df = pd.DataFrame(info)
        info_df_cn = info_df.rename(columns=cols_cn)
        info_df_cn["首次涨停时间"] = info_df_cn["首次涨停时间"].apply(int)
        info_df_cn["最后涨停时间"] = info_df_cn["最后涨停时间"].apply(int)
        info_df_cn["首次涨停时间"] = pd.to_datetime(info_df_cn["首次涨停时间"],unit="s") +  timedelta(hours=8)
        info_df_cn["最后涨停时间"] = pd.to_datetime(info_df_cn["最后涨停时间"],unit="s") +  timedelta(hours=8)

        limit_up_count = data["limit_up_count"]
        limit_down_count = data["limit_down_count"]
        if save:
            file_name  =os.path.join(os.path.dirname(__file__) ,getStrDate(2) + "_limit_up.xlsx")
            info_df_cn.to_excel(file_name,index=False)
        return info_df_cn,limit_up_count,limit_down_count
    
    def get_data_df_fcb(self,date,save=True):
        limit_up,limit_up_count,limit_down_count  = LimitUpPool().get_data_df(date,save=False)
        lst = []
        for code in limit_up["代码"]:
            tmp = {}
            tmp["代码"] = code
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code,
                                                    period="daily", 
                                                    start_date=date, 
                                                    end_date=date, 
                                                    adjust="qfq")
            tmp["成交量"] = stock_zh_a_hist_df["成交量"].loc[0] * 100
            lst.append(tmp)
        df = pd.DataFrame(lst)
        
        df_merged = pd.merge(limit_up,df,on=["代码"])
        df_merged["封成比"] = df_merged["封单量"] / df_merged["成交量"] 
        # print(df_merged)
        
        df_merged["预测"] = df_merged["封成比"].apply(self.fcb_map)
        if save:
            file_name  =os.path.join(os.path.dirname(__file__) ,getStrDate(2) + "_limit_up_fengchengbi.xlsx")
            df_merged.to_excel(file_name,index=False)
        return df_merged
    
    
    @staticmethod
    def fcb_map(x):
        if x >= 10:
            return "涨停高开概率>70%"
        if 3 <= x < 10:
            return "明天高开在6-10%之间"
        if 1 <= x < 3:
            return "明天高开在3-6%之间" 
        if 0.5 <= x < 1:
            return "明天高开在1-3%之间" 
        return "无"
        
class BlockTop(DataClass):
    '''
    获取板块的信息
    '''
    def get_data_json(self,date,filt):
        url = "https://data.10jqka.com.cn/dataapi/limit_up/block_top"
        match filt:
            case 0:
                # 沪深除了创科
                filt = "HS"
            case _:
                # + 创、科创
                filt = "HS,GEM2STAR"
        params = {"filter": filt,
                "date": date}
        headers = {
            "User-Agent":getUserAgent(),
            
        }
        resp = rq.get(url, params=params,headers=headers)
        res = resp.json()
        return res

    
    def get_data_df(self, date,filt):
        data = self.get_data_json(date,filt)
        if data["status_code"]:
            return pd.DataFrame()
        df = pd.DataFrame(data["data"])
        # df["stock_list"]

        return df

# def limit_up_pool(date,save=True):
#     params = {
#     "page": 1,
#     "limit": 200,
#     "field": "199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004",
#     "filter": "HS,GEM2STAR",
#     "order_field": "330324",
#     "order_type": 0,
#     "date": date,
#     "_": 1722309210154
#     }
#     headers = {
#         "User-Agent":getUserAgent(),
        
        
#     }
#     url = "https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool"
#     resp = rq.get(url, params=params,headers=headers)
#     res = resp.json()
#     # pages = res.
#     data = res["data"]
#     cols_cn = {
#     "open_num":"开板次数",
#     "first_limit_up_time" :"首次涨停时间",
#     "last_limit_up_time":"最后涨停时间",
#     "code":"代码",
#     "limit_up_type":'涨停形态',
#     "order_volume":"封单量",
#     "is_new":'新上',
#     "limit_up_suc_rate":"近一年涨停封板率",
#     "currency_value":"流通市值",
#     "is_again_limit":"是否连板",
#     "change_rate":"涨幅",
#     "turnover_rate":"换手率",
#     "reason_type":"涨停原因",
#     "order_amount":"封单额",
#     "high_days":"几天几板",
#     "name":"名称",
#     "change_tag":"是否回封",
#     "latest":"最新",
#     "time_preview":"分时预览",}

#     info = data["info"]
#     info_df = pd.DataFrame(info)
#     info_df_cn = info_df.rename(columns=cols_cn)
#     info_df_cn["首次涨停时间"] = info_df_cn["首次涨停时间"].apply(int)
#     info_df_cn["最后涨停时间"] = info_df_cn["最后涨停时间"].apply(int)
#     info_df_cn["首次涨停时间"] = pd.to_datetime(info_df_cn["首次涨停时间"],unit="s") +  timedelta(hours=8)
#     info_df_cn["最后涨停时间"] = pd.to_datetime(info_df_cn["最后涨停时间"],unit="s") +  timedelta(hours=8)

#     limit_up_count = data["limit_up_count"]
#     limit_down_count = data["limit_down_count"]
#     if save:
#         file_name  =os.path.join(os.path.dirname(__file__) ,getStrDate(2) + "_limit_up.xlsx")
#         info_df_cn.to_excel(file_name,index=False)
    
#     # print(res)
#     return info_df_cn,limit_up_count,limit_down_count

def today_limit_up_pool_detail(save=True):
    '''
    融合选股信息和涨停信息
    '''
    date = getStrDate(1)
    #涨停板数据简报
    limig_up_pool_df = LimitUpPool().get_data_df_fcb(date,save=False)
    #全部股票详报
    stock_selection_df = getTodayStock(save=False)
    # stock_selection_df =getTodayStock,save=False
    #涨停股票详报
    limit_up_detail = pd.merge(limig_up_pool_df,stock_selection_df,on=["代码","名称"],how="left",suffixes=("","_y"))
    limit_up_detail.drop(["换手率_y","成交量_y"],axis=1,inplace=True)
    if save:
        save_file = os.path.join(os.path.dirname(__file__) ,"send", f"limit_up_pool_detail_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
        limit_up_detail.to_excel(save_file)
    return limit_up_detail

def today_limit_up_pool_detail_in_longhubang(save=True):
    '''
    一般是大盘结束运行后一个小时运行
    '''
    from instock.lib.trade_time import get_trade_date_last
    date,_ = get_trade_date_last()
    date_str = date.strftime("%Y%m%d")
    stock_lhb_detail_em_df = ak.stock_lhb_detail_em(start_date=date_str, end_date=date_str)
    #lhb机构席位数
    stock_lhb_jgmmtj_em_df = ak.stock_lhb_jgmmtj_em(start_date=date_str, end_date=date_str)
    stock_lhb_jgmmtj_em_df_columns = ['代码', '名称','买方机构数', '卖方机构数','机构买入总额', '机构卖出总额','机构买入净额', '市场总成交额', '机构净买额占总成交额比']
    stock_lhb_jgmmtj_em_df = stock_lhb_jgmmtj_em_df[stock_lhb_jgmmtj_em_df_columns]
    #merge ->[个股 - 机构数]
    stock_lhb_detail_em_df = pd.merge(stock_lhb_detail_em_df,stock_lhb_jgmmtj_em_df,on=["代码","名称"],how="left",suffixes=("","_y"))
    youzi_file = os.path.join(os.path.dirname(__file__),"swim_cash3.json")
    #添加营业部和游资信息
    stock2yyb = yyb_stocks2stock_yybs(date_str,youzi_file)
    stock_lhb_detail_em_df_yyb = pd.merge(stock_lhb_detail_em_df,
                                        stock2yyb,
                                        on="名称",
                                        how="left",
                                        suffixes=("","_y"))
    # stock_lhb_detail_em_df_yyb.drop(["名称_y"],inplace=True)
    
    
    ######################################################################

    #具体人气等信息
    limit_up_detail = today_limit_up_pool_detail(save=False)
    limit_up_detail = pd.merge(limit_up_detail,stock_lhb_detail_em_df_yyb,on=["代码","名称"],how="left",suffixes=("","_y"))
    limit_up_detail.drop(["流通市值_y","换手率_y","涨跌幅_y"],axis=1,inplace=True)
  
    # #再merge
    # limit_up_lhb = pd.merge(limit_up_lhb,stock_lhb_jgmmtj_em_df,on=["代码","名称"],how="left",suffixes=("","_y"))
    
    if save:
        save_file = os.path.join(os.path.dirname(__file__) ,"send", f"limit_up_pool_detail+lhb+yyb_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
        limit_up_detail.to_excel(save_file)
    
    return limit_up_detail,stock_lhb_detail_em_df_yyb
    
class DataFramePretty(object):
    def __init__(self, df: pd.DataFrame) -> None:
        self.data = df

    def show(self, start_row=0, end_row=None):
        """
        显示指定范围的数据。

        :param start_row: 起始行号
        :param end_row: 结束行号
        :return: rich 表格对象
        """
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        
        # 复制数据以避免修改原数据
        df = self.data.copy()
        
        if end_row is None:
            end_row = len(df)
        df = df.iloc[start_row:end_row]

        # 动态设置列宽，避免数据被截断
        column_widths = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
        for col in df.columns:
            table.add_column(col, width=column_widths[col], overflow="fold")

        for idx, row in df.iterrows():
            table.add_row(*row.astype(str))

        return table

def track_stock_changes_cmd(date="20240906", poll_interval=5, attention=None):
    """
    跟踪股票变化并处理分页显示。

    :param date: 日期
    :param poll_interval: 刷新间隔
    :param attention: 关注的股票代码
    """
    console = Console()
    code_name_df, _ = get_code_name()
    if attention:
        code_name_df = code_name_df[code_name_df["code"].isin(attention)]

    code_name_df = code_name_df.rename(columns={"code": "代码", "name": "名称"})
    stock_cache = LimitUpPool().get_data_df_fcb(date, save=0)
    stock_cache.drop("分时预览", axis=1, inplace=True)
    stock_cache = pd.merge(stock_cache, code_name_df, on="代码", how="left", suffixes=("", "_y"))

    indicator_lst = ["封单额"]
    rows_per_page = 10  # 每页显示的行数
    page = 0
    stop_event = threading.Event()

    dfp = DataFramePretty(stock_cache)

    # 启动数据更新线程
    update_thread = threading.Thread(target=update_data, args=(date, attention, stock_cache, dfp, poll_interval, code_name_df, indicator_lst, stop_event))
    update_thread.daemon = True
    update_thread.start()

    total_pages = (len(stock_cache) + rows_per_page - 1) // rows_per_page

     # 显示帮助信息
    console.print("\n使用说明：")
    console.print("w - 上一页")
    console.print("s - 下一页")
    console.print("q - 退出")
    
    with Live(console=console, refresh_per_second=1) as live:
        while not stop_event.is_set():
            start_row = page * rows_per_page
            end_row = min(start_row + rows_per_page, len(dfp.data))

            table = dfp.show(start_row=start_row, end_row=end_row)
            live.update(table)

            # console.print("update")
            # 监听用户输入
            while True:
                if keyboard.is_pressed('s'):
                    if page < total_pages - 1:
                        page += 1
                    else:
                        console.print("已经是最后一页。", style="bold red")
                    break
                elif keyboard.is_pressed('w'):
                    if page > 0:
                        page -= 1
                    else:
                        console.print("已经是第一页。", style="bold red")
                    break
                elif keyboard.is_pressed('q'):
                    stop_event.set()
                    break

            time.sleep(0.1)  # 继续短暂停顿以保持实时刷新

    update_thread.join()
    
def update_data(date, attention, stock_cache, dfp, poll_interval, code_name_df, indicator_lst, stop_event):
    """
    更新数据的线程函数。
    """
    while not stop_event.is_set():
        stock_data = LimitUpPool().get_data_df_fcb(date, save=0)
        stock_data.drop("分时预览", axis=1, inplace=True)
        stock_data = pd.merge(stock_data, code_name_df, on="代码", how="left", suffixes=("", "_y"))
        
        stock_new = pd.merge(stock_data, stock_cache, on="代码", how="left", suffixes=("", "_y"))
        for indicator in indicator_lst:
            new_col = round((stock_new[indicator] - stock_new[indicator + "_y"]) / stock_new[indicator + "_y"], 4) * 100
            new_col = new_col.apply(lambda x: str(x) + "%")
            stock_data[indicator + "_change"] = new_col

        stock_cache.update(stock_data)
        dfp.data = stock_data.copy()

        time.sleep(poll_interval)

def track_stock_changes_qt(root, frame, date="20240906", poll_interval=5, attention=None):
    """
    跟踪股票变化。
    """
    code_name_df, _ = get_code_name()
    if attention:
        code_name_df = code_name_df[code_name_df["code"].isin(attention)]

    code_name_df = code_name_df.rename(columns={"code": "代码", "name": "名称"})
    stock_cache = LimitUpPool().get_data_df_fcb(date, save=0)
    stock_cache.drop("分时预览", axis=1, inplace=True)
    stock_cache = pd.merge(stock_cache, code_name_df, on="代码", how="left", suffixes=("", "_y"))

    indicator_lst = ["封单额"]
    dfp = DataFramePretty(stock_cache)

    # # 启动数据更新线程
    # update_thread = threading.Thread(target=update_data, args=(date, attention, stock_cache, dfp, poll_interval, code_name_df, indicator_lst, stop_event))
    # update_thread.daemon = True
    # update_thread.start()

    # pt = Table2(frame, dataframe=dfp.data, showtoolbar=True, showstatusbar=True)
    # pt.show()

def start_update(stop_event, update_thread):
    """开始更新数据"""
    stop_event.clear()
    update_thread.start()

def stop_update(stop_event):
    """停止更新数据"""
    stop_event.set()

# def qt_main_for_stock_changes(date=None, poll_interval=5, attention=None):
#     """
#     主函数用于启动图形界面。
#     """
#     if not date:
#         date = time.strftime("%Y%m%d")

#     root = tk.Tk() #创建window
#     # root.geometry("540x360")  
#     wwidth = 1120 #1080
#     wheight = 840 #780
    
#     # 将窗口放置在屏幕中央  
#     screen_width = root1.winfo_screenwidth()  # 获取屏幕宽度 
#     screen_height = root1.winfo_screenheight()  # 获取屏幕高度  
#     x = (screen_width  - wwidth ) // 2
#     y = (screen_height  - wheight ) // 2
#     root1.geometry(f"{wwidth}x{wheight}+{x}+{y}")  
#     # root1.resizable(False, False)  # 禁止窗口伸缩 
#     root.title('zhangting')

#     frame = tk.Frame(root) #创建frame
#     frame.pack(fill='both', expand=True)
    
#     notebook = ttk.Notebook(frame) # 绑定notebook到frame上
#     notebook.pack(fill='both', expand=True) #填充方式

#     tabs = []
#     for i in range(3):
#         tab = ttk.Frame(notebook)
#         notebook.add(tab, text=f"Tab {i+1}")
#         tabs.append(tab)


    
    
#     # 创建按钮并绑定事件
#     for tab in enumerate(tabs):
#         if i == 0:
#             start_button = ttk.Button(tab, text="开始", command=lambda: start_update(stop_event, threading.Thread(target=update_data, args=(date, attention, None, None, poll_interval, None, None, stop_event))))
#             start_button.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.05)

#             stop_button = ttk.Button(tab, text="终止", command=lambda: stop_update(stop_event))
#             stop_button.place(relx=0.17, rely=0.05, relwidth=0.1, relheight=0.05)

#     # 使用 grid 布局管理器显示表格
#     for i, tab in enumerate(tabs):
#         if i == 0:
#             track_stock_changes_qt(root, tab, date=date, poll_interval=poll_interval, attention=attention)
#         # pt = Table2(tab, dataframe=pd.DataFrame(), showtoolbar=True, showstatusbar=True)
#         # pt.grid(row=1, column=0, columnspan=2, sticky='nsew')

#     root.mainloop()

    
def task_for_this_file():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    print(cur_path)
    time_diplayer(today_limit_up_pool_detail_in_longhubang,save=True)



if __name__ == "__main__":
    # cur_path = os.path.abspath(os.path.dirname(__file__))
    # print(cur_path)
    # time_diplayer(today_limit_up_pool_detail_in_longhubang,save=True)
    # stock_data = LimitUpPool().get_data_df_fcb("20240906",save=0)
    
    # print(stock_data)
    js_data = Continuous_limit_up().get_data_json(date="20240911",filt=1)
    print(js_data["data"]["trade_status"]["name"])
    t = pd.DataFrame(js_data["data"]["limit_up_count"])
    print(t.reset_index())
    # emx = earn_money_xiaoying()
    # print(pd.DataFrame(earn_money_xiaoying()))
    
    
    
    # print(BlockTop().get_data_df(date="20240901",filt=1))
    pass
    
    
    # track_stock_changes_cmd(date="20240909")
    # stop_event = threading.Event()
    # qt_main_for_stock_changes(poll_interval=2 )
  
    

    
    # try:
    #     time_diplayer(today_limit_up_pool_detail_in_longhubang,save=True)
    # except Exception as e:
    #     print(e)
    #     time_diplayer(today_limit_up_pool_detail,save=True) 
        
    # stock_lhb_detail_daily_sina_df = ak.stock_lhb_detail_em(start_date="20240801",end_date="20240801")
    # print(stock_lhb_detail_daily_sina_df)

    
    # import akshare as ak
    # stock_lhb_jgmmtj_em_df = ak.stock_lhb_jgmmtj_em(start_date="20240417", end_date="20240430")
    # stock_lhb_jgmmtj_em_df_columns = ['代码', '名称','买方机构数', '卖方机构数','机构买入总额', '机构卖出总额','机构买入净额', '市场总成交额', '机构净买额占总成交额比']
    # stock_lhb_jgmmtj_em_df[stock_lhb_jgmmtj_em_df_columns]
    # print(stock_lhb_jgmmtj_em_df.columns)
    
    