import tkinter as tk
from pandastable import Table
import pandas as pd

# 初始化窗口
root = tk.Tk()
frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

# 创建初始 DataFrame
dfp = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

# 创建 pandastable.Table 实例
pt = Table(frame, dataframe=dfp, showtoolbar=True, showstatusbar=True, width=1080, height=520)
pt.show()

def add_column_and_update_table():
    global dfp, pt
    # 示例：添加新列
    
    import time
    time.sleep(5)
    # 刷新表格
    new_column_name = 'C'
    column_values = [7, 8, 9]
    # 向 DataFrame 添加新列
    dfp[new_column_name] = column_values
    time.sleep(2)
    pt.model.df = pd.DataFrame()  # 更新 model 中的 DataFrame
    pt.redraw()  # 重新绘制表格



# 调用函数添加新列并刷新表格
import threading

threading.Thread(target=add_column_and_update_table,).start()

root.mainloop()