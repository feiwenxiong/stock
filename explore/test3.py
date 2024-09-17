import tkinter as tk  
from tkinter import PanedWindow  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
from matplotlib.figure import Figure  
  
class MatplotlibApp:  
    def __init__(self, master=None):  
        self.master = master  
        self.master.title("Multiple Matplotlib Figures in Tkinter with PanedWindow")  
  
        # 创建一个 PanedWindow  
        self.paned_window = PanedWindow(self.master, orient=tk.VERTICAL)  
        self.paned_window.pack(fill=tk.BOTH, expand=1)  
  
        # 添加多个图表到 PanedWindow  
        for i in range(6):  
            frame = tk.Frame(self.paned_window)  
            self.paned_window.add(frame)  
  
            fig = Figure(figsize=(5, 4), dpi=100)  
            ax = fig.add_subplot(111)  
            ax.plot([1, 2, 3, 4], [i, i+1, i+2, i+3])  
  
            canvas = FigureCanvasTkAgg(fig, master=frame)  
            canvas_widget = canvas.get_tk_widget()  
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)  
  
            # 可选：添加工具栏  
            # toolbar = NavigationToolbar2Tk(canvas, frame)  
            # toolbar.pack(side=tk.BOTTOM, fill=tk.X)  
  
# 创建Tkinter主窗口并启动应用程序  
root = tk.Tk()  
app = MatplotlibApp(master=root)  
root.mainloop()