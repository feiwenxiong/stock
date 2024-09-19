import tkinter as tk
from tkinter import ttk
import requests
from fake_useragent import UserAgent
import json
from datetime import datetime
'''
测试金十数据app
'''
class Jin10App:
    def __init__(self, notebook_frame):
        # notebook_frame 是 Notebook 中的一个选项卡
        self.notebook_frame = notebook_frame
        self.root = notebook_frame.master  # 获取主窗口（Tk 实例）

        # 创建框架用于包含文本框和滚动条
        frame = tk.Frame(self.notebook_frame)
        frame.pack(fill="both", expand=True)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # 创建文本框用于展示新闻内容
        self.text_area = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set, height=25, width=75)
        self.text_area.pack(pady=10, padx=10, fill="both", expand=True)
        
        # 将滚动条与文本框连接
        scrollbar.config(command=self.text_area.yview)

        # 配置标签颜色
        self.text_area.tag_configure("new", foreground="red")  # 新文本红色
        self.text_area.tag_configure("normal", foreground="black")  # 旧文本黑色

        # 用于存储已经展示过的新闻
        self.displayed_news_ids = set()

        # 获取并展示一次初始数据
        self.update_news()

    def get_jin10_data2(self):
        url = "https://flash-api.jin10.com/get_flash_list"
        headers = {
            "x-app-id": "SO1EJGmNgCtmpcPF",
            "x-version": "1.0.0",
        }
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        queryParam = {
            "max_time": current_time,
            "channel": "-8200",
        }
        headers["User-Agent"] =  UserAgent().random
        resp = requests.get(url, headers=headers, params=queryParam)
        data = resp.json()['data']
        content_list = []
        for item in data:
            news_id = item["id"]
            content = {
                "内容": item["data"]["content"],
                "时间": item["time"],
                "id": news_id  # 记录新闻的唯一 ID
            }
            content_list.append(content)

        # 按时间倒序排列（数据已经是从最新到最旧，插入时保持这个顺序）
        return content_list    

    def update_news(self):
        # 获取新闻数据
        news_data = self.get_jin10_data2()
        print(f"\n资讯直播： {news_data[0]}\n")
        # 逆序处理，以确保最旧的新闻在底部
        for item in reversed(news_data):
            news_id = item["id"]
            if news_id not in self.displayed_news_ids:
                self.displayed_news_ids.add(news_id)
                news_text = f"【{item['时间']}】 - {item['内容']}\n\n"
                # 插入新内容到顶部
                self.text_area.insert("1.0", news_text)
                # 给新插入的内容加上"new"标签
                self.text_area.tag_add("new", "1.0", f"1.{len(news_text)}")
                # 设置光标到最顶端
                self.text_area.see("1.0")
        
        # 设置已展示的新闻为正常颜色
        self.text_area.tag_configure("normal", foreground="black")
        # 确保之前的内容仍然是黑色
        self.text_area.tag_add("normal", "2.0", tk.END)

        # 继续定时更新
        self.root.after(5000, self.update_news)  # 每5秒更新一次

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jin10 新闻展示")
    root.geometry("600x400")

    # 创建 Notebook 组件
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # 创建一个选项卡并将 Jin10App 的内容添加到选项卡中
    news_frame = tk.Frame(notebook)
    notebook.add(news_frame, text="最新新闻")
    
    # 初始化 Jin10App 并将其绑定到 Notebook 的选项卡中
    app = Jin10App(news_frame)

    root.mainloop()
