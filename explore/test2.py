# import akshare as ak
# stock_board_ths_df = ak.stock_board_concept_cons_ths(symbol_code="人脸识别")
# print(stock_board_ths_df)
# from zhangting import BlockTop
# import pandas as pd
# from datetime import datetime
# blocks = BlockTop().get_data_json(date="20240911",filt=1)["data"]
# print(blocks)
# t = []
# for block in blocks:
#     t.extend(block["stock_list"])
# t = pd.DataFrame(t)
# t["first_limit_up_time"] = t["first_limit_up_time"].map(int).map(datetime.fromtimestamp)
# t["last_limit_up_time"] = t["last_limit_up_time"].map(int).map(datetime.fromtimestamp)
# print(t)
# print(t.columns)
# -*- coding: utf-8 -*-
import tkinter as tk
from cefpython3 import cefpython as cef
import sys

class BrowserFrame(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.browser_frame = None
        self.browser = None
        self.create_browser()

    def create_browser(self):
        # 创建一个 Tkinter Frame 用于显示浏览器
        self.browser_frame = tk.Frame(self, bg='black')
        self.browser_frame.pack(fill='both', expand=True)
        
        # 使用 cefpython 创建浏览器
        window_info = cef.WindowUtils.CreateWindowInfo(self.browser_frame.winfo_id())
        self.browser = cef.CreateBrowserSync(window_info=window_info)
        self.browser.SetClientHandler(LoadHandler())
        
        # 访问网页
        self.browser.LoadUrl("https://q.10jqka.com.cn/")

class LoadHandler(object):
    def OnLoadingStateChange(self, is_loading, **_):
        if not is_loading:
            print("Page loaded")

def main():
    # 初始化 CEF
    cef.Initialize()

    # 创建 Tkinter 主窗口
    root = tk.Tk()
    root.title("CEF in Tkinter")

    # 创建并放置浏览器框架
    browser_frame = BrowserFrame(root)
    browser_frame.pack(fill='both', expand=True)

    # 启动 Tkinter 主循环
    root.mainloop()

    # 清理 CEF
    cef.Shutdown()

if __name__ == "__main__":
    main()

