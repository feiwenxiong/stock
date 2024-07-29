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
from  fake_useragent import UserAgent

def zt_pool(date="20240729"):
    """
    东方财富-ETF 实时行情
    https://quote.eastmoney.com/center/gridlist.html#fund_etf
    :return: ETF 实时行情
    :rtype: pandas.DataFrame
    """
    headers = {"User-Agent":UserAgent().random}
    url = "https://push2ex.eastmoney.com/getTopicZTPool"
    params = {
        "cb" : "callbackdata5037106",
        # "ut" : "7eea3edcaed734bea9cbfc24409ed989",
        # "dpt": "wz.ztzt",
        "Pageindex":0,
        "pagesize": 200,
        # "sort":"fbt%3Aasc",
        "_" : 172224521174,
    }
    r = requests.get(url, headers=headers,  params=params)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["pool"])
    
    

if __name__ == "__main__":
    
    zt_pool()
    
    
    table = tbs.TABLE_CN_STOCK_SELECTION
    cols = table["columns"]
    cols_cn = [ tbs.get_field_cn(x,table) for x in cols]
    save_file = os.path.join(os.path.dirname(__file__) , f"today_{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}.xlsx")
    stock_selection_df = stock_selection()
    stock_selection_df.columns = cols_cn
    
    stock_selection_df.to_excel(save_file, index=False)