import akshare as ak


if __name__ == "__main__":
    #board名录
    stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    print(stock_board_industry_name_em_df)
    
    #板块具体股票
    stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol="教育")
    print(stock_board_industry_cons_em_df)
    

    #板块排行
    stock_hsgt_board_rank_em_df = ak.stock_hsgt_board_rank_em(symbol="北向资金增持行业板块排行", 
                                                              indicator="今日")
    print(stock_hsgt_board_rank_em_df)
    
    #抱团
    stock_lh_yyb_control_df = ak.stock_lh_yyb_control()
    print(stock_lh_yyb_control_df)