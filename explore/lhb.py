import os
import sys
cpath_current = os.path.dirname(os.path.dirname(__file__))
sys.path.append(cpath_current)
import instock
from instock.core.crawling.stock_lhb_em import *
import time

if __name__ == "__main__":
    # stock_lhb_detail_em_df = stock_lhb_detail_em(
    #     start_date="20240613", end_date="20240713"
    # )
    # stock_lhb_detail_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_detail_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一月")
    # stock_lhb_stock_statistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近三月")
    # print(stock_lhb_stock_statistic_em_df)
    

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近六月")
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_stock_statistic_em_df = stock_lhb_stock_statistic_em(symbol="近一年")
    # print(stock_lhb_stock_statistic_em_df)

    # stock_lhb_jgmmtj_em_df = stock_lhb_jgmmtj_em(
    #      start_date="20240713", end_date="20240724"
    # )
    # print(stock_lhb_jgmmtj_em_df)

    # stock_lhb_jgstatistic_em_df = stock_lhb_jgstatistic_em(symbol="近一月")
    # print(stock_lhb_jgstatistic_em_df)
    # stock_lhb_jgstatistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)

    stock_lhb_hyyyb_em_df = stock_lhb_hyyyb_em(
         start_date="20240725", end_date="20240725"
    )
    stock_lhb_hyyyb_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_hyyyb_em_df)
    

    # stock_lhb_yybph_em_df = stock_lhb_yybph_em(symbol="近一月")
    # print(stock_lhb_yybph_em_df)
    # stock_lhb_yybph_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)

    # stock_lhb_traderstatistic_em_df = stock_lhb_traderstatistic_em(symbol="近一月")
    # print(stock_lhb_traderstatistic_em_df)
    # stock_lhb_traderstatistic_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)


    # stock_lhb_stock_detail_date_em_df = stock_lhb_stock_detail_date_em(symbol="002901")
    # print(stock_lhb_stock_detail_date_em_df)

    # stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
        # symbol="002901", date="20221012", flag="买入"
    # )
    # stock_lhb_stock_detail_em_df.to_excel(os.path.join(os.path.dirname(__file__), f"{time.time()}.xlsx"),index=False)
    # print(stock_lhb_stock_detail_em_df)
    

    # stock_lhb_stock_detail_em_df = stock_lhb_stock_detail_em(
    #     symbol="600016", date="20220324", flag="买入"
    # )
    # print(stock_lhb_stock_detail_em_df)


