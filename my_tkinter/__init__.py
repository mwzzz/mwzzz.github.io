import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 示例")
root.geometry("400x400")  # 设置窗口大小


# 定义一个函数来处理按钮点击事件
def on_button_click():
    name = entry_name.get()
    if name:
        messagebox.showinfo("问候", f"你好，{name}!")
    else:
        messagebox.showwarning("警告", "请输入你的名字")


# 定义一个函数来处理复选框状态变化
def on_checkbox_change():
    if var_check.get():
        label_status.config(text="复选框已选中")
    else:
        label_status.config(text="复选框未选中")


# 定义一个函数来启动进度条
def start_progress(button):
    button.config(state=tk.DISABLED)  # 禁用按钮
    progress['value'] = 0
    for i in range(101):
        progress['value'] = i
        root.update_idletasks()  # 更新界面
        time.sleep(0.05)  # 模拟耗时操作
    messagebox.showinfo("完成", "下载已完成")
    button.config(state=tk.NORMAL)  # 重新启用按钮


# 定义一个函数来在新线程中启动进度条
def start_progress_thread(button):
    thread = threading.Thread(target=start_progress, args=(button,))
    thread.start()


# 创建并放置标签
label_name = tk.Label(root, text="请输入你的名字:")
label_name.pack(pady=10)

# 创建并放置输入框
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

# 创建并放置按钮
button_greet = tk.Button(root, text="打招呼", command=on_button_click)
button_greet.pack(pady=10)

# 创建并放置复选框
var_check = tk.IntVar()
checkbox = tk.Checkbutton(root, text="选择我", variable=var_check, command=on_checkbox_change)
checkbox.pack(pady=5)

# 创建并放置状态标签
label_status = tk.Label(root, text="复选框未选中")
label_status.pack(pady=5)

# 创建并放置列表框
listbox = tk.Listbox(root, height=4)
listbox.pack(pady=5)

# 向列表框中添加一些项目
for item in ["苹果", "香蕉", "橙子", "葡萄", "橘子"]:
    listbox.insert(tk.END, item)

# 创建并放置滚动条
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# 创建并放置进度条
progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress.pack(pady=10)

# 创建并放置启动进度条的按钮
button_start_progress = tk.Button(root, text="下载xx文件", command=lambda: start_progress_thread(button_start_progress))
button_start_progress.pack(pady=10)

# 运行主循环
root.mainloop()
