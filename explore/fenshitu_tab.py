from matplotlib import pyplot as plt
import time
from matplotlib.widgets import Cursor,MultiCursor
plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题
import json
import requests
import logging
import io
import pandas as pd
import ttkbootstrap as ttk
# import ttkinter as ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import requests
import logging
import io
import pandas as pd
import json
from matplotlib import pyplot as plt
from collections import OrderedDict
from utils import is_now_break,is_now_open
import akshare as ak
import concurrent.futures
import threading
import akshare as ak
def _get_market_code(stock_code):
    """
    根据股票代码计算出市场代码。
    :param stock_code: 股票代码
    :return: 市场代码，0：深圳，1：上海，2：其他
    """
    # 获取股票代码的前缀
    code_prefix = int(stock_code[0])

    # 根据前缀判断市场[更新20240919]
    if code_prefix in [0, 2, 3,4,8]:  # 深圳股票代码前缀一般为 0、2、3
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


def get_bankuai_dapan_minute_trend2(show=False):
    import akshare as ak
    from tqdm import tqdm
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
    outer = OrderedDict()   
    outer["上证指数"] = shanghai_index_df
    outer["深证指数"] = sz_index_df
    outer["创业指数"] = chuangye_index_df
     
    inner = {}
    fig_bankuai = []
    
    for index,row in stock_board_industry_name_em_df_5.iterrows():
        # fig_bankuai = []
        print(f"updating 板块[{index + 1}]/6")
        bankuai_rank = row["排名"]
        bankuai_code = row["板块代码"]
        bankuai_name = row["板块名称"]

        ##绘图
        # fig,ax = plt.subplots(2,1)
        
        # plt.figure()
        # ax = plt.subplot(2,1,1)
        # fig.suptitle(f"分时图 rank{str(bankuai_rank)} : " + bankuai_name)
        # ax[0].set_ylabel("涨幅")
        data_test = data_to_data_frame(get_minutely_data(bankuai_code,bankuai=True))
        data_test = (data_test / data_test.iloc[0] - 1.0) * 100
        
        # ax[0].plot(data_test.index,
        #          data_test.Close,
        #          label=bankuai_name,
        #          color="red",
        #          linewidth=1)
        # ax[0].plot(shanghai_index_df.index,
        #          shanghai_index_df.Close,
        #          label="上证指数",
        #          color="green",
        #          linewidth=1)
        # ax[0].plot(sz_index_df.index,
        #          sz_index_df.Close,
        #          label="深证指数",
        #          color="blue",
        #          linewidth=1)
        # ax[0].plot(chuangye_index_df.index,
        #          chuangye_index_df.Close,
        #          label="创业指数",
        #          color="black",
        #          linewidth=1)
        # cursor = Cursor(ax[0], useblit=True, color='red', linewidth=1,linestyle='--')
        # ax[0].legend()
        # ax[0].grid()
        # ax[0].set_title("板块和指数走势")
        
        outer[bankuai_name] = [bankuai_rank,data_test]
       
        
        #找出当前板块的排行前8股票
        inner[bankuai_name] = OrderedDict()
        stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=bankuai_name).head(8)
        for index,row in stock_board_industry_cons_em_df.iterrows():
            stock_rank = row["序号"]
            stock_code = row["代码"]
            stock_name = row["名称"]
            #获取1min分时数据
            data_test_ = data_to_data_frame(get_minutely_data(stock_code,bankuai=False))
            #scale
            tmp_vol = data_test_["Volumn"]
            data_test_ = (data_test_ / data_test_.iloc[0] - 1.0) * 100
            fluid_shares = ak.stock_individual_info_em(symbol=stock_code)["流通股"]
            fluid_shares = tmp_vol / fluid_shares * 100
            data_test_["Turnover"] = fluid_shares
            # ax[1].plot(data_test_.index,
            #          data_test_.Close,
            #          label=f"rank{str(stock_rank)}: "+ stock_name,
            #          linewidth=1)
            inner[bankuai_name][stock_name] =[stock_rank,data_test_]
        # fig_bankuai.append(fig)
        # print(fig_bankuai)
        # ax[1].legend()
        # ax[1].grid()
        # ax[1].set_title("板块内股票走势")
        

    # cursor1 = Cursor(ax[1], useblit=True, color='red', linewidth=1,linestyle='--')
    if show:
        pass
        # multi = MultiCursor(fig.canvas, ax, color='r', lw=1,linestyle="--",horizOn=True, vertOn=True)
        # plt.show()
    return outer,inner


# import concurrent.futures
# import akshare as ak
# from collections import OrderedDict

def get_bankuai_data(bankuai_name, bankuai_code,bankuai_rank):
    data_test = data_to_data_frame(get_minutely_data(bankuai_code, bankuai=True))
    data_test = (data_test / data_test.iloc[0] - 1.0) * 100
    return bankuai_name, data_test,bankuai_rank

def get_bankuai_stock_data(stock_name, stock_code, stock_rank):
    tmp = get_minutely_data(stock_code, bankuai=False)
    # print(stock_code)
    data_test_ = data_to_data_frame(tmp)
    # print(data_test_)
    if data_test_ is not None:
        data_test_ = (data_test_ / data_test_.iloc[0] - 1.0) * 100
    else:
        print(stock_name, stock_code, stock_rank)
        data_test_ = pd.DataFrame()
    return stock_name, data_test_, stock_rank

def get_bankuai_dapan_minute_trend(show=False):
    import time
    s = time.time()
    shanghai_index_df = data_to_data_frame(get_minutely_data("0", bankuai=False, dapan=0))
    shanghai_index_df = (shanghai_index_df / shanghai_index_df.iloc[0] - 1.0) * 100
    sz_index_df = data_to_data_frame(get_minutely_data("0", bankuai=False, dapan=1))
    sz_index_df = (sz_index_df / sz_index_df.iloc[0] - 1.0) * 100
    chuangye_index_df = data_to_data_frame(get_minutely_data("0", bankuai=False, dapan=2))
    chuangye_index_df = (chuangye_index_df / chuangye_index_df.iloc[0] - 1.0) * 100

    stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    stock_board_industry_name_em_df_5 = stock_board_industry_name_em_df.head(6)[["排名", "板块名称", "板块代码"]]

    outer = OrderedDict()
    inner = {}
    outer["上证指数"] = shanghai_index_df
    outer["深证指数"] = sz_index_df
    outer["创业指数"] = chuangye_index_df

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for index, row in stock_board_industry_name_em_df_5.iterrows():
            bankuai_rank = row["排名"]
            bankuai_name = row["板块名称"]
            bankuai_code = row["板块代码"]
            futures.append(executor.submit(get_bankuai_data, bankuai_name, bankuai_code,bankuai_rank))

        for future in concurrent.futures.as_completed(futures):
            bankuai_name, bankuai_data,bankuai_rank = future.result()
            outer[bankuai_name] = [bankuai_rank,bankuai_data]

            # Fetch stocks for each bankuai
            stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=bankuai_name).head(8)
            inner[bankuai_name] = OrderedDict()
            stock_futures = []
            for index, row in stock_board_industry_cons_em_df.iterrows():
                stock_rank = row["序号"]
                stock_name = row["名称"]
                stock_code = row["代码"]
                stock_futures.append(executor.submit(get_bankuai_stock_data, stock_name, stock_code,stock_rank))

            for stock_future in concurrent.futures.as_completed(stock_futures):
                stock_name, stock_data, stock_rank = stock_future.result()
                # inner[bankuai_name][stock_name] = [stock_rank,data_test_]
                inner[bankuai_name][stock_name] = [stock_rank,stock_data,stock_code] #add code
    print(time.time() - s)
    return outer, inner



class MatplotlibTab:
    def __init__(self, notebook, datas=None,tab_name="Matplotlib Charts"):
        # 创建Tab
        self.frame = ttk.Frame(notebook)
        self.canvas = tk.Canvas(self.frame)
        self.scroll_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        # 在Canvas上创建一个Frame来放置图表
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # 将Tab添加到notebook中
        notebook.add(self.frame, text=tab_name)

        # 绑定滚轮事件
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)
     
        #初始化数据
        self.datas = datas
        if not self.datas:
            self.outer,self.inner = None,None
        else:
            self.outer,self.inner = self.datas
        self.notify = threading.Event()
        # self.outer,self.inner= get_bankuai_dapan_minute_trend()  # 更新图表数据
        # self.create_charts()
        # 绘制图表
        self.figure_to_canvas = []
        # self.figs = figs
        # self.update_thread = threading.Thread(target=self.update_data,)
        # self.update_thread.daemon = True
        # self.update_thread.start()
        self.update_button = ttk.Button(self.frame, text="Update Charts", command=lambda:threading.Thread(target=self.update_data,).start())
        self.update_button.pack(pady=10,)
        # self.frame.after(5000, self.create_charts)  # 每隔（5秒）更新一次
        self.frame.after(10, self.create_charts)
    def update_data(self,):
        print("更新分时图数据中！")
        #预先更新数据
        outer,inner = get_bankuai_dapan_minute_trend()  # 更新图表数据
        print("更新分时图完毕！")
        self.datas = outer,inner
        self.outer = outer
        self.inner = inner
        # self.create_charts()
        self.notify.set()
        print(f"请求更新界面！{self.notify.is_set()}")
        time.sleep(50)
        while is_now_open():
            outer,inner = get_bankuai_dapan_minute_trend()  # 更新图表数据
            self.datas = outer,inner
            self.outer = outer
            self.inner = inner
            # self.create_charts()
            time.sleep(50)
    def create_charts(self):
        """ 在Scrollable Frame中绘制6张图表 """
        if 1:
            if not self.datas:
                #没有数据就直接返回
                # print("no self.datas")
                pass
            if self.notify.is_set():
                # print("等待更新信号")
                print("接收到信号，更新图表中！")
                self.figure_to_canvas = []  # 记录每个图表和其canvas
                self.cross_lines = []  # 记录所有子图的十字线
                outer = self.outer #板块
                inner = self.inner #各版块的个股
                outer = list(outer.items())
                # inner = list(inner.items())
                shanghai_index_df = outer[0][1]
                sz_index_df = outer[1][1]
                chuangye_index_df = outer[2][1]
                #[上证，深圳，]
                for i in range(3,len(outer)):
                    #添加十字线
                    fig,ax = plt.subplots(3,1,
                                          figsize=(8,12), 
                                          sharex=False)
                    
                    
                    bankuai_name = outer[i][0]
                    bankuai_rank = outer[i][1][0]
                    # print(outer,len(outer))
                    bankuai_data = outer[i][1][1]
                    
                    # fig.suptitle(f"分时图 rank{str(bankuai_rank)} : " + bankuai_name)
                    
                    if 1:
                        #板块与指数叠加
                        ax[0].plot(bankuai_data.index,
                            bankuai_data.Close,
                            label=bankuai_name,
                            color="red",
                            linewidth=1)
                        ax[0].plot(shanghai_index_df.index,
                                shanghai_index_df.Close,
                                label=outer[0][0],
                                color="green",
                                linewidth=1)
                        ax[0].plot(sz_index_df.index,
                                sz_index_df.Close,
                                label=outer[1][0],
                                color="blue",
                                linewidth=1)
                        ax[0].plot(chuangye_index_df.index,
                                chuangye_index_df.Close,
                                label=outer[2][0],
                                color="black",
                                linewidth=1)
                        ax[0].set_ylabel("板块涨幅")
                        ax[0].set_title(f"分时图 rank{str(bankuai_rank)} : " + bankuai_name)
                        ax[0].grid()
                        ax[0].legend()
                        # ax[0].tight_layout()
                        
                        #板块内个股分时图叠加
                        for stock_name,item in inner[bankuai_name].items():
                            # （name,[rank,data]）
                            # item = list(item.items())
                            item = list(item)
                            # stock_name = item[0]
                            stock_rank = item[0]
                            stock_data = item[1]
                            stock_code = item[2]
                            # print(stock_data)
                            ax[1].plot(stock_data.index,
                                    stock_data.Close,
                                    label=f"{stock_rank}_{stock_name}",
                                    linewidth=1)
                            
                            #添加turnober
                            
                            tmp_vol = stock_data["Volume"]
                            fluid_shares = ak.stock_individual_info_em(symbol=stock_code).iloc[7]["value"]
                            fluid_shares = tmp_vol * 100 / fluid_shares * 100
                            stock_data["Turnover"] = fluid_shares
                           
                            ax[2].plot(stock_data.index,
                                    stock_data.Turnover,
                                    label=f"{stock_rank}_{stock_name}",
                                    linewidth=1)
                        ax[1].legend()
                        ax[1].grid()
                        ax[1].set_ylabel("个股票涨幅%")
                        # ax[1].tight_layout()
                        
                        ax[2].legend()
                        ax[2].grid()
                        ax[2].set_ylabel("个股换手率%")
                        # ax[2].tight_layout()
                        # plt.tight_layout()
                    
                    #添加十字线
                    fig = self.create_chart(fig)
                    
                    #创建图表
                    canvas_fig = FigureCanvasTkAgg(fig, self.scrollable_frame)
                    canvas_fig.get_tk_widget().grid(row=(bankuai_rank - 1) // 2, column=(bankuai_rank - 1) % 2, padx=10, pady=10, sticky="ew")
                    canvas_fig.draw()  # 手动刷新每个图表
                    
                    # 记录图表和canvas
                    self.figure_to_canvas.append((fig, canvas_fig))
                    
                    # 确保FigureCanvas的事件绑定
                    canvas_fig.mpl_connect('motion_notify_event', self.on_mouse_move)
                #更新完毕，清楚待更新标志
                self.notify.clear()
                print("更新分时图表完成！！")
            self.frame.after(10, self.create_charts)
            # self.frame.after(5000, self.create_charts)  # 每隔（5秒）更新一次
    def create_chart(self, some_fig):
        """ 创建一个包含两个子图的图表，并自定义十字线 """       
        ax = some_fig.axes
        # 初始化十字线
        for axis in ax:
            hline, = axis.plot([], [], color='r', linestyle='--', linewidth=1)  # 横线
            vline, = axis.plot([], [], color='r', linestyle='--', linewidth=1)  # 竖线
            self.cross_lines.append((hline, vline, axis))

        return some_fig
    def on_mouse_move(self, event):
        """ 处理鼠标移动事件，以更新十字线 """
        from matplotlib.dates import num2date

        if event.inaxes is not None:  # 确保事件发生在一个子图中
            for hline, vline, axis in self.cross_lines:
                if event.inaxes == axis:
                    
                    
                    
                    x, y = event.xdata, event.ydata
                    x_datetime = num2date(x).strftime("%Y-%m-%d %H:%M:%S")
                    # 更新十字线的坐标
                    hline.set_data([axis.get_xlim()[0], axis.get_xlim()[1]], [y, y])
                    vline.set_data([x, x], [axis.get_ylim()[0], axis.get_ylim()[1]])
                    
                    # if hasattr(self, 'annot'):
                    #     self.annot.remove()

                    # # 添加新的坐标注释
                    # self.annot = axis.annotate(f'x={x:.2f}, y={y:.2f}', 
                    #                            xy=(x, y), 
                    #                            xytext=(x + 1, y + 1),  # 注释在交点的偏移位置
                    #                            fontsize=3,
                    #                            textcoords="offset points", 
                    #                            bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="lightyellow"),
                    #                            arrowprops=dict(arrowstyle="->", color="black"))
                    # # 使用 draw_idle 进行高效更新
                    # print(x,y)
                    
                    # 在左上角显示坐标
                    # axis.texts.clear()  # 清除之前的文本
                    for txt in axis.texts:
                        txt.remove()
                    axis.text(0.02, 0.98, f"X: {x_datetime}, Y: {y:.2f}", transform=axis.transAxes, 
                            fontsize=10, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

                    # 使用 draw_idle 进行高效更新
                    event.inaxes.figure.canvas.draw_idle()
                    event.inaxes.figure.canvas.draw_idle()

    def on_mouse_wheel(self, event):
        """ 鼠标滚轮事件处理，控制滚动 """
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")




if __name__ == "__main__":  # 测试代码
    print(get_bankuai_dapan_minute_trend(show=True))
    # print(data_to_data_frame(get_minutely_data("603660", bankuai=False)))
    # #上证
    # 1.000001#上证
    # 0.399001#深圳
    # 0.399006#创业板
    # import akshare as ak
    # shanghai_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=0))
    # shanghai_index_df = (shanghai_index_df / shanghai_index_df.iloc[0] - 1.0) * 100
    # sz_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=1))
    # sz_index_df = (sz_index_df / sz_index_df.iloc[0] - 1.0) * 100
    # chuangye_index_df = data_to_data_frame(get_minutely_data("0",bankuai=False,dapan=2))
    # chuangye_index_df = (chuangye_index_df / chuangye_index_df.iloc[0] - 1.0) * 100

    # stock_board_industry_name_em_df = ak.stock_board_industry_name_em()
    # stock_board_industry_name_em_df_5 = stock_board_industry_name_em_df.head(6)[["排名","板块名称","板块代码"]]
    # # print(stock_board_industry_name_em_df_5)
    # # import akshare as ak
    # # fig,axes = plt.sublots(5)
    # fig_bankuai = []
    # for index,row in stock_board_industry_name_em_df_5.iterrows():
    #     # fig_bankuai = []
    #     bankuai_rank = row["排名"]
    #     bankuai_code = row["板块代码"]
    #     bankuai_name = row["板块名称"]

    #     ##绘图
    #     fig,ax = plt.subplots(2,1)
        
    #     # plt.figure()
    #     # ax = plt.subplot(2,1,1)
    #     fig.suptitle(f"分时图 rank{str(bankuai_rank)} : " + bankuai_name)
    #     ax[0].set_ylabel("涨幅")
    #     data_test = data_to_data_frame(get_minutely_data(bankuai_code,bankuai=True))
    #     data_test = (data_test / data_test.iloc[0] - 1.0) * 100
    #     ax[0].plot(data_test.index,
    #              data_test.Close,
    #              label=bankuai_name,
    #              color="red",
    #              linewidth=1)
    #     ax[0].plot(shanghai_index_df.index,
    #              shanghai_index_df.Close,
    #              label="上证指数",
    #              color="green",
    #              linewidth=1)
    #     ax[0].plot(sz_index_df.index,
    #              sz_index_df.Close,
    #              label="深证指数",
    #              color="blue",
    #              linewidth=1)
    #     ax[0].plot(chuangye_index_df.index,
    #              chuangye_index_df.Close,
    #              label="创业指数",
    #              color="black",
    #              linewidth=1)
    #     # cursor = Cursor(ax[0], useblit=True, color='red', linewidth=1,linestyle='--')
    #     ax[0].legend()
    #     ax[0].grid()
    #     ax[0].set_title("板块和指数走势")
    #     #找出当前板块的排行前8股票
    #     stock_board_industry_cons_em_df = ak.stock_board_industry_cons_em(symbol=bankuai_name).head(8)
    #     for index,row in stock_board_industry_cons_em_df.iterrows():
    #         stock_rank = row["序号"]
    #         stock_code = row["代码"]
    #         stock_name = row["名称"]
    #         #获取1min分时数据
    #         data_test_ = data_to_data_frame(get_minutely_data(stock_code,bankuai=False))
    #         #scale
    #         data_test_ = (data_test_ / data_test_.iloc[0] - 1.0) * 100
    #         ax[1].plot(data_test_.index,
    #                  data_test_.Close,
    #                  label=f"rank{str(stock_rank)}: "+ stock_name,
    #                  linewidth=1)
    #     fig_bankuai.append(fig)
    #     print(fig_bankuai)
    #     ax[1].legend()
    #     ax[1].grid()
    #     ax[1].set_title("板块内股票走势")
    #     multi = MultiCursor(fig.canvas, ax, color='r', lw=1,linestyle="--",horizOn=True, vertOn=True)

    #     # cursor1 = Cursor(ax[1], useblit=True, color='red', linewidth=1,linestyle='--')
    #     plt.show()


