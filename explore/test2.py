

# import akshare as ak

# stock_board_industry_hist_min_em_df = ak.stock_board_industry_hist_min_em(symbol="保险", period="1")
# print(stock_board_industry_hist_min_em_df)

# import akshare as ak

# # 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0
# stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000001", start_date="2024-09-11 09:30:00", end_date="2024-09-11 15:00:00", period="1", adjust="")
# print(stock_zh_a_hist_min_em_df)
from matplotlib import pyplot as plt
from matplotlib.widgets import Cursor,MultiCursor
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题
import json
import requests
import logging
import io
import pandas as pd
def _get_market_code(stock_code):
    """
    根据股票代码计算出市场代码。
    :param stock_code: 股票代码
    :return: 市场代码，0：深圳，1：上海，2：其他
    """
    # 获取股票代码的前缀
    code_prefix = int(stock_code[0])

    # 根据前缀判断市场
    if code_prefix in [0, 2, 3]:  # 深圳股票代码前缀一般为 0、2、3
        return 0  # 深圳市场
    elif code_prefix in [6, 9]:  # 上海股票代码前缀一般为 6、9
        return 1  # 上海市场
    else:
        return 2  # 其他市场，此处假设为北京市场


def _handle_event(event_data) -> str:
    """
    解析event数据
    :param event_data: SSE数据
    :return: 事件的数据字段
    """
    lines = event_data.strip().split('\n')
    data = ""

    for line in lines:
        if line.startswith("event:"):  # 东财分时数据的事件无event
            event_type = line.replace("event:", "").strip()
        elif line.startswith("data:"):
            data = line.replace("data:", "").strip()
    # logger.info(f"data received: {data}")
    return data

def get_minutely_data(code: str,bankuai=False,dapan=-1) -> dict:
    """
    获取最新的分时数据
    :param code: 股票代码，6位数字格式，比如：“000001”。
    :return: 数据字典
    """
    # url格式，需要调用者依次填充：市场代码（0：深圳，0：上海），股票代码，日期窗口
    url_format = "https://45.push2.eastmoney.com/api/qt/stock/trends2/sse?fields1=f1,f2,f3,f4,f5,f6,f7,f8," \
                 "f9,f10,f11,f12,f13,f14,f17&fields2=f51,f52,f53,f54,f55,f56,f57," \
                 "f58&mpi=1000&ut=fa5fd1943c7b386f172d6893dbfba10b&secid={market}.{code}" \
                 "&ndays={days}&iscr=0&iscca=0&wbp2u=1849325530509956|0|1|0|web"
    if not bankuai:
        url = url_format.format(market=_get_market_code(code), code=code, days=1)  # 请求url
    else:
        url = url_format.format(market=90, code=code, days=1) #板块
    if dapan == 0:
        url = url_format.format(market=1, code="000001", days=1) # 上证指数
    elif dapan == 1:
        url = url_format.format(market=0, code="399001", days=1) #深证指数
    elif dapan == 2:
        url = url_format.format(market=0, code="399006", days=1) #创业指数
    else:
        pass

    # print(url)
    headers = {
        "Accept": "text/event-stream"
    }

    response = requests.get(url, headers=headers, stream=True)  # 请求数据，开启流式传输

    if response.status_code == 200:
        event_data = ""
        for chunk in response.iter_content(chunk_size=None):  # 不断地获取数据
            data_decoded = chunk.decode('utf-8')  # 将字节流解码成字符串
            event_data += data_decoded
            parts = event_data.split('\n\n')
            if len(parts) > 1:  # 获取到一条完整的事件后，对数据进行解析。
                data = _handle_event(parts[0])
                return json.loads(data)



def data_to_data_frame(data: dict) -> pd.DataFrame:
    try:
        trends = data["data"]["trends"]
        trends_str = json.dumps(trends)
        trend_csv_content = 'Time,Open,Close,High,Low,Volume,Amount,Average\n'
        trend_csv_content += trends_str.replace("\", \"", "\n").strip("\"[]")
        # logger.info(f"trends_str:\n{trend_csv_content}")

        type_mapping = {
            "Open": float,
            "High": float,
            "Low": float,
            "Close": float,
            "Volume": float,
            "Amount": float,
            "Average": float
        }
        df_data = pd.read_csv(
            io.StringIO(trend_csv_content), delimiter=',', dtype=type_mapping,
            parse_dates=['Time'], index_col='Time')
        # logger.info(f"df_data: {df_data}")
        return df_data
    except Exception as e:
        logging.error(f"异常：{e}")
        return None

if __name__ == "__main__":  # 测试代码

    #上证
    1.000001#上证
    0.399001#深圳
    0.399006#创业板
    import akshare as ak
    shanghai_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=0))
    shanghai_index_df = (shanghai_index_df / shanghai_index_df.iloc[0] - 1.0) * 100
    sz_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=1))
    sz_index_df = (sz_index_df / sz_index_df.iloc[0] - 1.0) * 100
    chuangye_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=2))
    chuangye_index_df = (chuangye_index_df / chuangye_index_df.iloc[0] - 1.0) * 100

    stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    stock_board_industry_name_em_df_5 = stock_board_industry_name_em_df.head(6)[["排名","板块名称","板块代码"]]
    # print(stock_board_industry_name_em_df_5)
    # import akshare as ak
    # fig,axes = plt.sublots(5)
    for index,row in stock_board_industry_name_em_df_5.iterrows():
        bankuai_rank = row["排名"]
        bankuai_code = row["板块代码"]
        bankuai_name = row["板块名称"]

        ##绘图
        fig,ax = plt.subplots(1,2)
        # plt.figure()
        # ax = plt.subplot(2,1,1)
        fig.suptitle(f"分时图 rank{str(bankuai_rank)} : " + bankuai_name)
        ax[0].set_ylabel("涨幅")
        data_test = data_to_data_frame(get_minutely_data(bankuai_code,bankuai=True))
        data_test = (data_test / data_test.iloc[0] - 1.0) * 100
        ax[0].plot(data_test.index,
                 data_test.Close,
                 label=bankuai_name,
                 color="red",
                 linewidth=1)
        ax[0].plot(shanghai_index_df.index,
                 shanghai_index_df.Close,
                 label="上证指数",
                 color="green",
                 linewidth=1)
        ax[0].plot(sz_index_df.index,
                 sz_index_df.Close,
                 label="深证指数",
                 color="blue",
                 linewidth=1)
        ax[0].plot(chuangye_index_df.index,
                 chuangye_index_df.Close,
                 label="创业指数",
                 color="black",
                 linewidth=1)
        # cursor = Cursor(ax[0], useblit=True, color='red', linewidth=1,linestyle='--')
        ax[0].legend()
        ax[0].grid()
        ax[0].set_title("板块和指数走势")
        #找出当前板块的排行前8股票
        stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=bankuai_name).head(8)
        for index,row in stock_board_industry_cons_em_df.iterrows():
            stock_rank = row["序号"]
            stock_code = row["代码"]
            stock_name = row["名称"]
            #获取1min分时数据
            data_test_ = data_to_data_frame(get_minutely_data(stock_code,bankuai=False))
            #scale
            data_test_ = (data_test_ / data_test_.iloc[0] - 1.0) * 100
            ax[1].plot(data_test_.index,
                     data_test_.Close,
                     label=f"rank{str(stock_rank)}: "+ stock_name,
                     linewidth=1)
        ax[1].legend()
        ax[1].grid()
        ax[1].set_title("板块内股票走势")
        multi = MultiCursor(fig.canvas, ax, color='r', lw=1,linestyle="--",horizOn=True, vertOn=True)

        # cursor1 = Cursor(ax[1], useblit=True, color='red', linewidth=1,linestyle='--')
        plt.show()


