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
import pandastable
from pandastable import Table as Table2
import pandas as pd
# from tkinter import ttk
import ttkbootstrap as ttk
# from ttkbootstrap.constants import *
import warnings
from zhangting import LimitUpPool,DataFramePretty
from utils import closest_trade_date
from PIL import Image, ImageTk
warnings.filterwarnings('ignore')
pd.set_option('future.no_silent_downcasting', True)


# class Table2:
#     def __init__(sefl,table):
#         self.table = table
#         self.options ={'align': 'w',
#                         'cellbackgr': '#F4F4F3',
#                         'cellwidth': 80,
#                         'floatprecision': 3,
#                         'thousandseparator': '',
#                         'font': 'Arial',
#                         'fontsize': 12,
#                         'fontstyle': '',
#                         'grid_color': '#ABB1AD',
#                         'linewidth': 1,
#                         'rowheight': 22,
#                         'rowselectedcolor': '#E4DED4',
#                         'textcolor': 'black'}
#         config.apply(self.options,self.table)
        
        
    


# class Continuous_limit_up(DataClass):
    
#     def get_data_json(self,date,filt):
#         '''
#             date:20240726
#         '''
#         url = " https://data.10jqka.com.cn/dataapi/limit_up/continuous_limit_up"
#         match filt:
#             case 0:
#                 # 沪深除了创科
#                 filt = "HS"
#             case _:
#                 # + 创、科创
#                 filt = "HS,GEM2STAR"
#         params = {"filter": filt,
#                 "date": date}
#         headers = {
#             "User-Agent":getUserAgent(),
            
            
#         }
#         url = "https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool"
#         resp = rq.get(url, params=params,headers=headers)
#         res = resp.json()
#         return res

    
#     def get_data_df(self,date,filt):
#         data = self.get_data_json(date,filt)
#         if data["status_code"]:
#             return pd.DataFrame()


        
#         return data["info"]
        
# class LimitUpPool(DataClass):
#     '''获取涨停的股票池
#     '''

    
#     def __init__(self):
#         super().__init__()
#         self.data_json = None
        
#     def get_data_json(self,date):
        
#         params = {
#         "page": 1,
#         "limit": 200,
#         "field": "199112,10,9001,330323,330324,330325,9002,330329,133971,133970,1968584,3475914,9003,9004",
#         "filter": "HS,GEM2STAR",
#         "order_field": "330324",
#         "order_type": 0,
#         "date": date,
#         "_": 1722309210154
#         }
#         headers = {
#             "User-Agent":getUserAgent(),
            
#         }
#         url = "https://data.10jqka.com.cn/dataapi/limit_up/limit_up_pool"
#         resp = rq.get(url, params=params,headers=headers)
#         res = resp.json()
#         self.data_json = res
#         return res

#     def get_data_df(self,date,save=True):
#         data = self.get_data_json(date)["data"]
#         cols_cn = {
#         "open_num":"开板次数",
#         "first_limit_up_time" :"首次涨停时间",
#         "last_limit_up_time":"最后涨停时间",
#         "code":"代码",
#         "limit_up_type":'涨停形态',
#         "order_volume":"封单量",
#         "is_new":'新上',
#         "limit_up_suc_rate":"近一年涨停封板率",
#         "currency_value":"流通市值",
#         "is_again_limit":"是否连板",
#         "change_rate":"涨幅",
#         "turnover_rate":"换手率",
#         "reason_type":"涨停原因",
#         "order_amount":"封单额",
#         "high_days":"几天几板",
#         "name":"名称",
#         "change_tag":"是否回封",
#         "latest":"最新",
#         "time_preview":"分时预览",}

#         info = data["info"]
#         info_df = pd.DataFrame(info)
#         info_df_cn = info_df.rename(columns=cols_cn)
#         info_df_cn["首次涨停时间"] = info_df_cn["首次涨停时间"].apply(int)
#         info_df_cn["最后涨停时间"] = info_df_cn["最后涨停时间"].apply(int)
#         info_df_cn["首次涨停时间"] = pd.to_datetime(info_df_cn["首次涨停时间"],unit="s") +  timedelta(hours=8)
#         info_df_cn["最后涨停时间"] = pd.to_datetime(info_df_cn["最后涨停时间"],unit="s") +  timedelta(hours=8)

#         limit_up_count = data["limit_up_count"]
#         limit_down_count = data["limit_down_count"]
#         if save:
#             file_name  =os.path.join(os.path.dirname(__file__) ,getStrDate(2) + "_limit_up.xlsx")
#             info_df_cn.to_excel(file_name,index=False)
#         return info_df_cn,limit_up_count,limit_down_count
    
#     def get_data_df_fcb(self,date,save=True):
#         limit_up,limit_up_count,limit_down_count  = LimitUpPool().get_data_df(date,save=False)
#         lst = []
#         for code in limit_up["代码"]:
#             tmp = {}
#             tmp["代码"] = code
#             stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code,
#                                                     period="daily", 
#                                                     start_date=date, 
#                                                     end_date=date, 
#                                                     adjust="qfq")
#             tmp["成交量"] = stock_zh_a_hist_df["成交量"].loc[0] * 100
#             lst.append(tmp)
#         df = pd.DataFrame(lst)
        
#         df_merged = pd.merge(limit_up,df,on=["代码"])
#         df_merged["封成比"] = df_merged["封单量"] / df_merged["成交量"] 
#         # print(df_merged)
        
#         df_merged["预测"] = df_merged["封成比"].apply(self.fcb_map)
#         if save:
#             file_name  =os.path.join(os.path.dirname(__file__) ,getStrDate(2) + "_limit_up_fengchengbi.xlsx")
#             df_merged.to_excel(file_name,index=False)
#         return df_merged
    
    
#     @staticmethod
#     def fcb_map(x):
#         if x >= 10:
#             return "涨停高开概率>70%"
#         if 3 <= x < 10:
#             return "明天高开在6-10%之间"
#         if 1 <= x < 3:
#             return "明天高开在3-6%之间" 
#         if 0.5 <= x < 1:
#             return "明天高开在1-3%之间" 
#         return "无"
        
# class BlockTop(DataClass):
#     '''
#     获取板块的信息
#     '''
#     def get_data_json(self,date,filt):
#         url = "https://data.10jqka.com.cn/dataapi/limit_up/block_top"
#         match filt:
#             case 0:
#                 # 沪深除了创科
#                 filt = "HS"
#             case _:
#                 # + 创、科创
#                 filt = "HS,GEM2STAR"
#         params = {"filter": filt,
#                 "date": date}
#         headers = {
#             "User-Agent":getUserAgent(),
            
#         }
#         resp = rq.get(url, params=params,headers=headers)
#         res = resp.json()
#         return res

    
#     def get_data_df(self, date,filt):
#         data = self.get_data_json(date,filt)
#         if data["status_code"]:
#             return pd.DataFrame()
#         df = pd.DataFrame(data["data"])
#         # df["stock_list"]

#         return df

# class DataFramePretty(object):
#     def __init__(self, df: pd.DataFrame) -> None:
#         self.data = df

#     def show(self, start_row=0, end_row=None):
#         """
#         显示指定范围的数据。

#         :param start_row: 起始行号
#         :param end_row: 结束行号
#         :return: rich 表格对象
#         """
#         table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        
#         # 复制数据以避免修改原数据
#         df = self.data.copy()
        
#         if end_row is None:
#             end_row = len(df)
#         df = df.iloc[start_row:end_row]

#         # 动态设置列宽，避免数据被截断
#         column_widths = {col: max(df[col].astype(str).map(len).max(), len(col)) for col in df.columns}
#         for col in df.columns:
#             table.add_column(col, width=column_widths[col], overflow="fold")

#         for idx, row in df.iterrows():
#             table.add_row(*row.astype(str))

#         return table


def update_data(date, attention, stock_cache_lst, dfp, poll_interval, code_name_df, indicator_lst, stop_event,pt):
    """
    更新数据的线程函数。
    """
    
    while not stop_event.is_set():
        stock_cache = stock_cache_lst[0] #获得历史数据
        stock_data = LimitUpPool().get_data_df_fcb(date, save=0) #获得当前数据
        #数据处理
        stock_data.drop("分时预览", axis=1, inplace=True)
        stock_data = pd.merge(stock_data, code_name_df, on="代码", how="left", suffixes=("", "_y"))
        stock_new = pd.merge(stock_data, stock_cache, on="代码", how="left", suffixes=("", "_y"))
        for indicator in indicator_lst:
            new_col = round((stock_new[indicator] - stock_new[indicator + "_y"]) / stock_new[indicator + "_y"], 4) * 100
            new_col = new_col.apply(lambda x: str(x) + "%")
            stock_data[indicator + "_change"] = new_col
        # print(stock_data[indicator + "_change"])
        #处理完毕更新历史数据
        stock_cache_lst[0] = stock_data.copy()
        dfp.data = stock_data.copy() #跟新dfp的数据
        print("updating zhangting data !!")
        
        pt.model.df = stock_data
        pt.redraw()
        # i += 1
        time.sleep(poll_interval)
        
def start_update(stop_event, update_thread):
    """开始更新数据"""
    stop_event.clear()
    update_thread.start()
def stop_update(stop_event):
    """停止更新数据"""
    stop_event.set()
    print("stop zhangting data !")


def start_track_stock_changes_qt():
    """
    跟踪股票变化。
    """
    print("start_track_stock_changes_qt")
    date = date_entry.get()
    attention = None
    indicator_lst = ["封单额"]
    poll_interval = int(duration_entry.get())
    
    code_name_df, _ = get_code_name()
    if attention:
        code_name_df = code_name_df[code_name_df["code"].isin(attention)]
    #初始化
    code_name_df = code_name_df.rename(columns={"code": "代码", "name": "名称"})
    stock_cache = LimitUpPool().get_data_df_fcb(date, save=0)
    stock_cache.drop("分时预览", axis=1, inplace=True)
    stock_cache = pd.merge(stock_cache, code_name_df, on="代码", how="left", suffixes=("", "_y"))
    
    dfp = DataFramePretty(stock_cache)
    stock_cache_lst = [stock_cache]
    
    pt = Table2(table_frame, dataframe=dfp.data, showtoolbar=True, showstatusbar=True,
                 width=1080,height=520)
    pt.show()
    
    
    # 启动数据更新线程
    update_thread = threading.Thread(target=update_data, 
                                     args=(date, attention, 
                                           stock_cache_lst, 
                                           dfp, 
                                           poll_interval, 
                                           code_name_df, 
                                           indicator_lst, 
                                           stop_event,
                                           pt))
    update_thread.daemon = True
    # update_thread.start()
    start_update(stop_event,update_thread)
    print("updating thread started!")
    
    


if __name__ == "__main__":
    #global variable
    stop_event = threading.Event()
    nearest_trade_date = closest_trade_date()
    
    #start tkinter
    # root = tk.Tk() #创建window
    root = ttk.Window(themename="minty")
    style = ttk.Style()
    theme_names = style.theme_names()#以列表的形式返回多个主题名
    print("themes: ",theme_names)
    root.geometry("1480x820")  

  
    wwidth = 1480 #1080
    wheight = 820 #780
    
    
    # 将窗口放置在屏幕中央  
    screen_width = root.winfo_screenwidth()  # 获取屏幕宽度 
    screen_height = root.winfo_screenheight()  # 获取屏幕高度  
    x = (screen_width  - wwidth ) // 2
    y = (screen_height  - wheight ) // 2
    root.geometry(f"{wwidth}x{wheight}+{x}+{y}")  
    # root.resizable(False, False)  # 禁止窗口伸缩 
    root.title('myStock')
    frame = tk.Frame(root) #创建frame
    frame.pack(fill='both', expand=True)
    
    #自定义notebook
    # notebook = MultiRowNotebook(frame)
    notebook = ttk.Notebook(frame) # 绑定notebook到frame上
    notebook.pack(fill='both', expand=True) #填充方式
    
    # 自定义样式
    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Arial', 12))  # 设置选项卡字体大小

    if 1 :
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="涨停池[实时]")
        duration_label = tk.Label(tab1, text="间隔时间: ",justify="right")  
        date_label = tk.Label(tab1, text="日期: ",justify="right")  
        
        # 创建输入框
        date_var = tk.StringVar()  
        # date = time.strftime("%Y%m%d")
        date_var.set(nearest_trade_date)
        date_entry = tk.Entry(tab1, textvariable=date_var)  


        # 创建输入框，数据类型是int，预填值为100  
        duration_var = tk.IntVar()
        duration_var.set(1)
        duration_entry = tk.Entry(tab1,textvariable=duration_var)    

        
        start_button = ttk.Button(tab1, text="start", 
                                  command=lambda: threading.Thread(target=start_track_stock_changes_qt).start())
        stop_button = ttk.Button(tab1, text="stop", 
                                 command=lambda: stop_update(stop_event))
        
        date_label.grid(row=0, column=0,sticky="E",pady=5)  # 行和列从0开始计数  
        date_entry.grid(row=0, column=1,sticky="E",columnspan=2) 
        duration_label.grid(row=1, column=0,sticky="E",pady=5,)  # 行和列从0开始计数  
        duration_entry.grid(row=1, column=1,sticky=tk.E,columnspan=2)  
        
        start_button.grid(row=2, column=1,ipadx=30)  # 行和列从0开始计数，columnspan使按钮跨越两列  
        stop_button.grid(row=2, column=2,ipadx=30)
        
        
        table_frame = tk.Frame(tab1, 
                            bg="green",
                            )
        table_frame.place(x=20,y=150) 
        # table_frame.pack(side="top", fill="both", expand=True)
    


    if 5:
        tab5 = ttk.Frame(notebook)#board名录
        notebook.add(tab5, text="东财板块总体[实时]")
        from utils import is_now_open,is_now_break
        def f5():
            while 1:
                if is_now_open():
                    if not is_now_break():
                        stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
                        pt5.model.df = stock_board_industry_name_em_df.copy()
                        pt5.redraw()
                        #3.5s更新一次
                        print("updating 板块总体!")
                    else:
                        pass
                time.sleep(3.5)
        #初始化
        stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
        pt5 = Table2(tab5, dataframe=stock_board_industry_name_em_df, showtoolbar=True, showstatusbar=True,
                    )
        # tab6.pack(fill="both", expand=True)
        pt5.show()
        thread5 = threading.Thread(target=f5)
        thread5.damon = True
        thread5.start()
    
    if 6:
        def f6():
            print("start 板块个股 ")
            bankuai_str = bankuai_var.get()
            stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=bankuai_str)
            pt6 = Table2(tab_frame6, dataframe=stock_board_industry_cons_em_df, showtoolbar=True, showstatusbar=True,
                    )
            pt6.show()
        
        
        #添加tab frame
        tab6 = ttk.Frame(notebook)
        notebook.add(tab6, text="东财板块成分")
        #添加entry和绑定变量
        bankuai_var = tk.StringVar()  
        bankuai_var.set("消费电子")
        bankuai_entry = tk.Entry(tab6, textvariable=bankuai_var)  
        bankuai_entry.pack()
        
        update_button6 = ttk.Button(tab6, 
                            text="start", 
                            command=lambda:threading.Thread(target=f6).start())
        update_button6.pack()
        
        tab_frame6 = tk.Frame(tab6) # 创建一个table容器
        tab_frame6.pack(fill='both', expand=True)
      
    if 9:
        def dapan():
            print("start dapan !!!")
            from hot_stock import earn_money_xiaoying
            from zhangting import Continuous_limit_up,BlockTop
        
            emx = pd.DataFrame(earn_money_xiaoying())
            
            pt91.model.df = emx
            pt91.redraw()
            
            #######
            js_data = Continuous_limit_up().get_data_json(date=nearest_trade_date,filt=1)
            t = js_data["data"]
            t_name = t["trade_status"]["name"]
            t_data = pd.DataFrame(t["limit_up_count"]).reset_index()
            #update table
            pt92.model.df = t_data
            # mask = df['A'] > 4
            # mask = t_data["today"] > t_data["yesterday"]
            # pt92.setColorByMask('today', mask, 'red')
            # pt92.setColorByMask('today', ~mask, 'green')
            pt92.redraw()
            #############
            
            bt = BlockTop().get_data_df(date=nearest_trade_date,filt=1).drop("stock_list",axis=1)
            #update table
            pt93.model.df = bt
            pt93.redraw()
            ########
            while str(t_name) == "交易中":
                print("    大盘趋势循环更新")
                emx = pd.DataFrame(earn_money_xiaoying())
                js_data = Continuous_limit_up().get_data_json(date=nearest_trade_date,filt=1)
                t =js_data["data"]
                t_name = t["trade_status"]["name"]
                t_data = pd.DataFrame(t["limit_up_count"]).reset_index()
                bt = BlockTop().get_data_df(date=nearest_trade_date,filt=1).drop("stock_list",axis=1)
                
                pt91.model.df = emx
                pt92.model.df = t_data
                pt93.model.df = bt
                
                pt91.redraw()
                
                
                # mask = t_data["today"] > t_data["yesterday"]
                # # mask = df['A'] > 4
                # pt92.setColorByMask('today', mask, 'red')
                # pt92.setColorByMask('today', ~mask, 'green')
                pt92.redraw()
                pt93.redraw()
                
                time.sleep(3)
        
        
        tab9 = ttk.Frame(notebook)
        notebook.add(tab9, text="ths板块趋势[实时]")  
        button_9 = ttk.Button(tab9, 
                            text="start", 
                            command=lambda:threading.Thread(target=dapan).start())
        # button_9.pack()
        button_9.grid(row=0, column=0, pady=(5, 0))
        table_frame91 = ttk.Frame(tab9)
        table_frame92 = ttk.Frame(tab9)
        table_frame93 = ttk.Frame(tab9)
        
        
        pt91 = Table2(table_frame91, 
                        dataframe=pd.DataFrame(), 
                        showtoolbar=True, 
                        showstatusbar=True,
                )
        pt91.show()
        pt92 = Table2(table_frame92, 
                        dataframe=pd.DataFrame(), 
                        showtoolbar=True, 
                        showstatusbar=True,
                )
        # options = {'colheadercolor':'green','floatprecision': 5}
        # pandastable.config.apply_options(options, pt92)
        pt92.show()
        pt93 = Table2(table_frame93, 
                            dataframe=pd.DataFrame(), 
                            showtoolbar=True, 
                            showstatusbar=True,
                            )
        pt93.show()
        
        
       
        # 使用 grid 布局来分配表格位置
        table_frame91.grid(row=1, column=0, sticky='nsew')
        table_frame92.grid(row=1, column=1, sticky='nsew')
        table_frame93.grid(row=2, column=0, columnspan=2, sticky='nsew')

        # 设置列和行权重以适应窗口变化
        tab9.columnconfigure(0, weight=1)
        tab9.columnconfigure(1, weight=1)
        tab9.rowconfigure(1, weight=12) #奇怪
        tab9.rowconfigure(2, weight=1)
    
    if 11:
        from zhangting import BlockTop,Continuous_limit_up
        def f11_1(blocks):
            t = []
            for block in blocks:
                t.extend(block["stock_list"])
            t = pd.DataFrame(t)
            t["first_limit_up_time"] = t["first_limit_up_time"].map(int).map(datetime.fromtimestamp)
            t["last_limit_up_time"] = t["last_limit_up_time"].map(int).map(datetime.fromtimestamp)
            return t
        
        def dapan_chengfengu():
            print("start 同花顺热点板块成分股 ！")
            bt = BlockTop().get_data_json(date=nearest_trade_date,filt=1)["data"]
            bt = f11_1(bt)
            pt11.model.df = bt
            pt11.redraw()
            
            js_data = Continuous_limit_up().get_data_json(date=nearest_trade_date,filt=1)
            t = js_data["data"]
            t_name = t["trade_status"]["name"]
            
            while str(t_name) == "交易中":
                print("    热点板块个股循环更新")
                js_data = Continuous_limit_up().get_data_json(date=nearest_trade_date,filt=1)
                t =js_data["data"]
                t_name = t["trade_status"]["name"]
            
                bt = BlockTop().get_data_json(date=nearest_trade_date,filt=1)["data"]
                bt = f11_1(bt)
                
                pt11.model.df = bt
                
                pt11.redraw()
                
                time.sleep(3)
        
        tab11 = ttk.Frame(notebook)
        notebook.add(tab11, text="ths板块个股趋势[实时]")  
        
        
        button_11 = ttk.Button(tab11, 
                            text="start", 
                            command=lambda:threading.Thread(target=dapan_chengfengu).start())
        button_11.pack()
        table_frame11 = ttk.Frame(tab11)
        table_frame11.pack(fill='both', expand=True)
        
        pt11 = Table2(table_frame11, 
                            dataframe=pd.DataFrame(), 
                            showtoolbar=True, 
                            showstatusbar=True,
                            )
        pt11.show()
        
        
    if 8:
        from hot_stock import getTodayStock
        def get_stock_selection_df():
            print("start stock selection!")
            stock_selection_df = getTodayStock(save=0)
            pt8.model.df = stock_selection_df
            pt8.redraw()
            
             
        tab8 = ttk.Frame(notebook)
        notebook.add(tab8, text="选股")    
        start_button_8 = ttk.Button(tab8, 
                            text="start", 
                            command=lambda:threading.Thread(target=get_stock_selection_df).start())
        start_button_8.pack()
        tab_frame8 = tk.Frame(tab8)
        tab_frame8.pack(fill='both', expand=True)
        
        pt8 = Table2(tab_frame8, 
                         dataframe=pd.DataFrame(), 
                         showtoolbar=True, 
                         showstatusbar=True,
                    )
        pt8.show()
        

        
    if 3:
        def f3():
            print("start stock2yyb")
            from lhb import yyb_stocks2stock_yybs
            # from utils import getStrDate
            # date = getStrDate(1)
            # print(date)
            ##构建营业部和股票的关系图
            # lhb_yyb_stock_daily_work(start_date="20240731", end_date="20240731")
            youzi_file = os.path.join(os.path.dirname(__file__),"swim_cash3.json")
            # stock2yyb = yyb_stocks2stock_yybs(date,youzi_file)
            
            try:
                stock2yyb = yyb_stocks2stock_yybs(nearest_trade_date,youzi_file)#可能没更新
            except:
                stock2yyb = pd.DataFrame()
            
            pt3.model.df = stock2yyb
            pt3.redraw()
            
        
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="龙虎榜和营业部")
        update_button3 = ttk.Button(tab3, 
                            text="start", 
                            command=lambda:threading.Thread(target=f3).start())
        update_button3.pack()
        tab_frame3 = tk.Frame(tab3) # 创建一个table容器
        tab_frame3.pack(fill='both', expand=True)
        pt3 = Table2(tab_frame3, dataframe=pd.DataFrame(), showtoolbar=True, showstatusbar=True,
                    )
        pt3.show()
    
    if 4:
        def f4():
            print("start today_limit_up_pool_detail_in_longhubang")
            from zhangting import today_limit_up_pool_detail_in_longhubang
            limit_up_detail,_ = today_limit_up_pool_detail_in_longhubang()
            
            p4.model.df = limit_up_detail
            pt4.redraw()
            
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="今日涨停池[+龙虎榜信息]")
        update_button4 = ttk.Button(tab4, 
                            text="start", 
                            command=lambda:threading.Thread(target=f4).start())
        update_button4.pack()
        tab_frame4 = tk.Frame(tab4) # 创建一个table容器
        tab_frame4.pack(fill='both', expand=True)
        pt4 = Table2(tab_frame4, dataframe=pd.DataFrame(), showtoolbar=True, showstatusbar=True,
                    )
        pt4.show()
    
    
    if 7:
        tab7 = ttk.Frame(notebook)
        notebook.add(tab7, text="关注列表")
        from ATTENTION import ATTENTION
        df = pd.DataFrame(ATTENTION)
        df.columns = ["代码"]
        pt7 = Table2(tab7, dataframe=df, showtoolbar=True, showstatusbar=True,
                    )
        # tab6.pack(fill="both", expand=True)
        pt7.show()
    
    
    if 2:
        
        def kongpan_qt():
            print("start kongpan_attention")
            data = kongpan_attention()
            # stock_selection_df = getTodayStock(save=False)
            # data = pd.merge(data[["代码","近来控盘比例趋势"]],
            #                 stock_selection_df,
            #                 left_on="代码",
            #                 right_on="代码",
            #                 how="left")
            pt2 = Table2(tab_frame2, dataframe=data, showtoolbar=True, showstatusbar=True,
                             )
            pt2.show()
                
            
        from hot_stock import kongpan_attention
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="关注控盘")
        update_button2 = ttk.Button(tab2, 
                            text="start", 
                            command=lambda:threading.Thread(target=kongpan_qt).start())
        update_button2.pack()
        
        tab_frame2 = tk.Frame(tab2)
        tab_frame2.pack(fill='both', expand=True)
    
    
    
    if 10:   
        
        my_images = []
        def f10():
            images_folder = folder_var.get()

            # 检查文件夹是否存在
            if os.path.exists(images_folder):
                # 如果存在，则删除文件夹
                import shutil
                shutil.rmtree(images_folder)
                print(f"已删除并重新创建文件夹: {images_folder}")

            os.makedirs(images_folder, exist_ok=True)
            print(f"已创建文件夹: {images_folder}")

            #业务逻辑
            attention_kongpan(images_folder)
            
            
            # # 清空img_frame
            # for widget in img_frame.winfo_children():
            #     widget.destroy()
            
            # 遍历文件夹中的图片
            # row = 0
            # column = 0
            # max_columns = 3  # 每行最多展示3张图片
            cols = 1
            x_offset = 0
            y_offset = 0
            for i,img_path in enumerate(os.listdir(images_folder)):
                row = i // cols
                col = i % cols
                if img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 加载图片并调整大小
                    img = Image.open(os.path.join(images_folder, img_path))
                    if i == 0:
                        image_width = img.width
                        image_height = img.height

                    
                    # 计算图片位置  
                    x = x_offset + col * image_width  
                    y = y_offset + row * image_height
                    
        
                    img_tk = ImageTk.PhotoImage(img)
                    image_id = canvas.create_image(x, y, image=img_tk, anchor='nw')
                    my_images.append(img_tk)

            canvas.config(scrollregion=canvas.bbox("all"))
            
        from utils import attention_kongpan
        tab10 = ttk.Frame(notebook)
        notebook.add(tab10, text="关注列表-今日K线")
        # 创建输入框
        folder_var = tk.StringVar()  
        # date = time.strftime("%Y%m%d")
        folder_var.set("trends")
        folder_entry = tk.Entry(tab10, textvariable=folder_var)  
        # date_label = tk.Label(tab1, text="日期: ",justify="right")  
        folder_entry.pack()
        button10 = ttk.Button(tab10, 
                            text="start", 
                            command=lambda:threading.Thread(target=f10).start())
        button10.pack()

        # 创建img_frame
        img_frame = ttk.Frame(tab10)
        img_frame.pack(fill='both', expand=True)
        
    

     
        # 创建Canvas和vsb
        canvas = tk.Canvas(img_frame, borderwidth=1, bg="#ffffff")
        vsb = tk.Scrollbar(img_frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set) 
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  
        

    root.mainloop() 