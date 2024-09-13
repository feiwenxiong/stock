# import akshare as ak
# stock_board_ths_df = ak.stock_board_concept_cons_ths(symbol_code="人脸识别")
# print(stock_board_ths_df)
from zhangting import BlockTop
import pandas as pd
blocks = BlockTop().get_data_json(date="20240913",filt=1)["data"]
t = []
for block in blocks:
    t.extend(block["stock_list"])
t = pd.DataFrame(t)
t["first_limit_up_time"] = t["first_limit_up_time"].map(int).map(datetime.fromtimestamp)
t["last_limit_up_time"] = t["last_limit_up_time"].map(int).map(datetime.fromtimestamp)

