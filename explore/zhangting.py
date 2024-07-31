import akshare as ak
from utils import *
import requests as rq
import os
import pandas as pd
from datetime import timedelta
from hot_stock import *
import time



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
        save_file = os.path.join(os.path.dirname(__file__) , f"limit_up_pool_detail_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
        limit_up_detail.to_excel(save_file)
    return limit_up_detail

 
if __name__ == "__main__":
    # s = time.time()
    
    
    # date = getStrDate(1)
    # # Continuous_limit_up().get_data_df("20240730",0)
    # # block_top("20240730",1)
    # # BlockTop().get_data_df("20240730",1)
    # # date = "20240730"
    # #涨停板数据简报
    # limig_up_pool_df = LimitUpPool().get_data_df_fcb(date,save=False)
    # #全部股票详报
    # # stock_selection_df = getTodayStock(save=False)

    # stock_selection_df =getTodayStock,save=False
    # #涨停股票详报
    # limit_up_detail = pd.merge(limig_up_pool_df,stock_selection_df,on=["代码","名称"],how="left",suffixes=("","_y"))
    # limit_up_detail.drop(["换手率_y","成交量_y"],axis=1,inplace=True)
    # save_file = os.path.join(os.path.dirname(__file__) , f"limit_up_pool_detail_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
    # limit_up_detail.to_excel(save_file)
    
    
    
    # # import akshare as ak
    # # stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20240528', adjust="qfq")
    # # print(stock_zh_a_hist_df)
    
    
    # # stock_zt_pool_em_df = ak.stock_zt_pool_em(date=date)
    # # print(stock_zt_pool_em_df)
    # # print("\ncost: ",time.time() -s )
    
    time_diplayer(today_limit_up_pool_detail,save=True)

    