from datetime import datetime
from  fake_useragent import UserAgent
from abc import ABC, abstractmethod
import threading
import time 
import os
import glob
import pandas as pd

# import time
# import threading

class DataClass(ABC):
    '''
    base class:用来限定处理数据步骤
    '''
    def __init__(self,headers=None):
        # self._url = url
        self.headers = headers
        if self.headers is None:
            self.headers = {"User-Agent":getUserAgent()} 
    @abstractmethod
    def get_data_json(self,*args,**kwargs):
        pass
    
    def get_data_df(self,*args,**kwargs):
        pass

def getStrDate(mode):
    '''
    时间格式string生成
    '''
    match mode:
        case 0:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M-%S')}"
        case 1:
            return f"{datetime.today().strftime('%Y%m%d')}"
        case _:
            return f"{datetime.today().strftime('%Y-%m-%d-%H-%M')}"

def getUserAgent():
    return UserAgent().random

def time_diplayer(func, *args, **kwargs):
    '''
    用来展示消耗时间的工具
    '''
    event = threading.Event()
    s = time.time()
    def timer(event,s):
        try:
            while not event.is_set():
                # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                current_time = str(round(time.time() -s,3)) 
                print("\r" + current_time + " s", end='', flush=True)
                time.sleep(1)
        except Exception as e:
            raise e
    
    t = threading.Thread(target=timer, args=(event,s))
    t.start()
    try:
        ret = func(*args, **kwargs)
    except Exception as e:
        ret = None
        pass
    event.set()
    t.join()
    return ret


    
def get_code_name():
    import akshare as ak
    # 获取所有 A 股股票的实时行情数据
    stock_zh_a_spot_em = ak.stock_zh_a_spot_em()

    # 提取代码和名称列
    df = stock_zh_a_spot_em[["代码", "名称"]]

    # 重命名列
    df.columns = ["code", "name"]  
    return df,stock_zh_a_spot_em
    

def merge_excel_files(directory):
    # 指定包含Excel文件的目录
    # directory = 'path/to/excel/files'
    # 获取当前日期
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 创建一个空的ExcelWriter对象
    with pd.ExcelWriter(f'merged_excel_{current_date}.xlsx', engine='openpyxl') as writer:
        # 遍历目录中的所有Excel文件
        for file_path in glob.glob(os.path.join(directory, '*.xlsx')):
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 获取文件名（不包括路径和扩展名）
            sheet_name = os.path.splitext(os.path.basename(file_path))[0]
            
            # 将DataFrame写入Excel文件的新工作表中
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def merge_df_files(df_dict,prefix):
    '''
    df_dict:{"sheet_name":someDataframe,...}
    '''
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 创建一个空的ExcelWriter对象
    dest = os.path
    with pd.ExcelWriter(prefix + f'_{current_date}.xlsx', engine='openpyxl') as writer:
        # 遍历
        for sheet_name,df in df_dict.items():
            # 获取文件名（不包括路径和扩展名）
            sheet_name = sheet_name
            # 将DataFrame写入Excel文件的新工作表中
            df.to_excel(writer, sheet_name=sheet_name, index=False)


def add_charts(df):
    import pandas as pd
    import matplotlib.pyplot as plt
    from openpyxl import Workbook,load_workbook
    from openpyxl.utils.dataframe import dataframe_to_rows
    from openpyxl.chart import ScatterChart, Reference, Series
    from openpyxl.drawing.image import Image
    from openpyxl.utils import get_column_letter
    import os

    # 生成走势图并保存为图片
    def plot_trend(code, trend_data):
        plt.figure(figsize=(10, 2))
        plt.plot(trend_data)
        plt.title(f'Control Trend for {code}')
        plt.xlabel('Time')
        plt.ylabel('Percentage')
        plt.grid(True)
        
        # 保存图片
        filename = f'{code}_trend.png'
        filepath = os.path.join('trends', filename)
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        return filepath

    # 创建目录以保存图片
    if not os.path.exists('trends'):
        os.makedirs('trends')

    # 为每个 code 生成走势图
    df['Trend_Plot'] = df.apply(lambda row: plot_trend(row['代码'], row['近来控盘比例趋势']), axis=1)

    # 创建一个新的工作簿
    wb = Workbook()
    

    # 获取默认的工作表
    ws = wb.active

    
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True)):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx + 1, column=c_idx, value=str(value))

    # 添加图片到 Excel 文件
    for idx, row in df.iterrows():
        img = Image(row['Trend_Plot'])
        # 假设图片放置在每行的末尾
        col_img = len(df.columns) + 1
        row_img = idx + 2  # 行号，从第二行开始
        ws.add_image(img, f"{get_column_letter(col_img)}{row_img}")

    # 保存 Excel 文件
    output_file = 'output_with_trends.xlsx'
    wb.save(output_file)


# if __name__ == "__main__":
#     add_charts(r"C:\Users\Feiwen.Xiong\Desktop\extraPrograms\stock\市场热点+个人关注控盘_2024-08-07.xlsx",
#                )