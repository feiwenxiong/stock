import json
import os
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)
from instock.core.crawling.stock_selection import * 
import pandas as pd
import numpy as np
from datetime import datetime
import instock.core.tablestructure as tbs
import akshare as ak
# import akshare as ak
def getTodayStock(save=True) -> pd.DataFrame:
    '''
    获取股吧人气榜等数据
    '''
    table = tbs.TABLE_CN_STOCK_SELECTION
    cols = table["columns"]
    cols_cn = [ tbs.get_field_cn(x,table) for x in cols]
    save_file = os.path.join(os.path.dirname(__file__) , f"today_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
    stock_selection_df = stock_selection()
    stock_selection_df.columns = cols_cn
    if save:
        stock_selection_df.to_excel(save_file, index=False)
    return stock_selection_df

def earn_money_xiaoying():
    '''return format:
                        item                value
            0         上涨               1198.0
            1         涨停                 26.0
            2       真实涨停                 22.0
            3   st st*涨停                  1.0
            4         下跌               3879.0
            5         跌停                333.0
            6       真实跌停                268.0
            7   st st*跌停                 77.0
            8         平盘                 37.0
            9         停牌                  2.0
            10       活跃度               23.42%
            11      统计日期  2024-04-15 15:00:00
    '''
    import akshare as ak
    stock_market_activity_legu_df = ak.stock_market_activity_legu()
    # print(stock_market_activity_legu_df) 
    return stock_market_activity_legu_df



def kongpan_attention():
    from ATTENTION import ATTENTION
    from utils import get_code_name
    
    code_name_df,spot_df = get_code_name()
    
    data = pd.DataFrame()
    data["代码"] = ATTENTION
    
    trend = []
    for code in ATTENTION:
        stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol=code)
        trend.append(stock_comment_detail_zlkp_jgcyd_em_df["value"].tolist())
    
    data["近来控盘比例趋势"] = trend

    data = pd.merge(data,spot_df,left_on="代码",right_on="代码",how="left")
    # data.drop("")
    # print(data)
    return data


if __name__ == "__main__":
    # stock_selection_df = getTodayStock()
    
    
    #赚钱效应
    emx = earn_money_xiaoying()
    print(emx)
    
    #人气排名
    stock_hot_rank_em_df = ak.stock_hot_rank_em()
    print(stock_hot_rank_em_df)
    
    
    #飙升榜
    stock_hot_up_em_df = ak.stock_hot_up_em()
    print(stock_hot_up_em_df)
    
    
    #千人千评
    # stock_comment_em_df = ak.stock_comment_em()
    # print(stock_comment_em_df)
    
    
    
    
    #主力控盘
    # stocks = ["000957"，""]
    # from ATTENTION import ATTENTION
    # from utils import get_code_name
    
    # code_name_df,spot_df = get_code_name()
    
    # data = pd.DataFrame()
    # data["code"] = ATTENTION
    
    # trend = []
    # for code in ATTENTION:
    #     stock_comment_detail_zlkp_jgcyd_em_df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol=code)
    #     trend.append(stock_comment_detail_zlkp_jgcyd_em_df["value"])
    
    # data["近来控盘比例趋势"] = trend

    # data = pd.merge(data,spot_df,left_on="code",right_on="代码",how="left")
    # print(data)
    
    data = kongpan_attention()
    print(data)
        # print(stock_comment_detail_zlkp_jgcyd_em_df)
        # from matplotlib import pyplot as plt
        # plt.scatter(stock_comment_detail_zlkp_jgcyd_em_df["date"],stock_comment_detail_zlkp_jgcyd_em_df["value"])
        # plt.title("hah")
        # plt.grid()
        # plt.show()
    
   
    
    