import akshare as ak
from utils import merge_df_files

if __name__ == "__main__":
    
    df_dict = {}
    #board名录
    stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    print(stock_board_industry_name_em_df)
    df_dict["板块名录"] = stock_board_industry_name_em_df
    
    #板块具体股票
    stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol="消费电子")
    print(stock_board_industry_cons_em_df)
    df_dict["消费电子板块"] = stock_board_industry_cons_em_df

    #板块排行
    stock_hsgt_board_rank_em_df = ak.stock_hsgt_board_rank_em(symbol="北向资金增持行业板块排行", 
                                                              indicator="今日")
    print(stock_hsgt_board_rank_em_df)
    df_dict["今日北向增持板块排行"] = stock_hsgt_board_rank_em_df

    merge_df_files(df_dict,"板块")
    