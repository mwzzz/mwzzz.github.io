import os
import time
import tkinter as tk
from tkinter import filedialog, ttk


# 获取当前工作目录os.path.dirname(os.path.abspath(__file__))
current_path = os.getcwd()
summary_file = current_path + '/汛情模板3.0.xlsx'
summary_filtered_file = current_path + '/汛情模板_地市筛选后.xlsx'


def check_path():
    path = current_path
    files_list = ['/lowcode_original_files', '/gzzx_original_files', '/filtered_files']
    for file in files_list:
        if not os.path.exists(path + file):
            os.mkdir(path + file)


def export_to_excel():
    print("导出到Excel")



def export_to_word():
    app.status_label.config(text=f'正在生成彩信word模版到{current_path}...')
    app.progress['value'] = 50
    app.progress.update()
    app.status_label.update()
    app.progress['value'] = 100
    app.status_label.config(text=f'生成彩信word模版到{current_path}完成')


def export_to_word1():
    app.status_label.config(text=f'正在生成彩信word模版到{current_path}...')
    app.progress['value'] = 50
    app.progress.update()
    app.status_label.update()
    app.progress['value'] = 100
    app.status_label.config(text=f'生成彩信word模版到{current_path}完成')


def clear_run():
    app.status_label.config(text='正在清空模版数据...')
    for i in range(100):
        time.sleep(0.1)
        app.progress['value'] = i
        app.status_label.update()
    app.status_label.config(text='清空模版数据完成')


class FileSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("汛情报送助手v3.0")

        # 获取屏幕的宽度和高度
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()

        # 计算窗口左上角的坐标，使窗口居中显示
        x = int(screenwidth / 2 - 1060 / 2)
        y = int(screenheight / 2 - 600 / 2)

        # 设置窗口大小和位置
        size = '{}x{}+{}+{}'.format(1060, 600, x, y)
        self.root.geometry(size)

        # 创建主要的框架
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        # 创建进度条
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=1000, mode="determinate")
        self.progress.pack(side=tk.BOTTOM)

        # 创建状态标签
        self.status_label = ttk.Label(self.root, text="等待操作...", background='green', foreground='white',
                                      font=("Helvetica", 16))
        self.status_label.pack(side=tk.BOTTOM)

        # 初始化文件路径和选项变量
        self.file_paths = [tk.StringVar(value=current_path) for _ in range(7)]
        self.selected_options = [tk.StringVar(value="指定本地路径") for _ in range(7)]

        # 创建文件路径输入框、浏览按钮和选项按钮
        self.button_texts = ["基站退服", "OLT退服", "局房动环", "基站停电", "安全类告警", "省干传输", "地市传输"]
        for i, text in enumerate(self.button_texts):
            label = ttk.Label(self.frame, text=f"{text}文件路径:")
            label.grid(row=i, column=0, sticky='w')

            entry = ttk.Entry(self.frame, textvariable=self.file_paths[i], width=50)
            entry.grid(row=i, column=1, sticky='ew')

            browse_btn = ttk.Button(self.frame, text="浏览", command=lambda t=i: self.browse_file(t))
            browse_btn.grid(row=i, column=2, sticky='e')

            options = ["指定本地路径", "故障中心自动下载", "低代码平台自动下载"]
            for j, option in enumerate(options):
                rb = ttk.Radiobutton(self.frame, text=f"选项{j + 1}: {option}", variable=self.selected_options[i],
                                     value=option)
                rb.grid(row=i, column=3 + j, sticky='w')

        # 创建控制按钮框架
        self.control_frame = ttk.Frame(self.frame)
        self.control_frame.grid(row=7, column=0, columnspan=10, sticky='ew', pady=(10, 0), rowspan=5)
        self.control_frame2 = ttk.Frame(self.frame)
        self.control_frame2.grid(row=12, column=0, columnspan=10, sticky='ew', pady=(10, 0), rowspan=1)
        export_filtered_excel_btn = ttk.Button(self.control_frame2, text="2.导出Excel汛情模板-筛选地市后（基于汛情模板筛选）")
        export_filtered_word_btn = ttk.Button(self.control_frame2, text="一键生成Word报告-筛选地市后", command=export_to_word1)

        # 创建控制按钮
        fullscreen_btn = ttk.Button(self.control_frame, text="全屏", command=self.toggle_fullscreen)
        clear_excel_btn = ttk.Button(self.control_frame, text="清空模版数据", command=clear_run)
        export_excel_btn = ttk.Button(self.control_frame2, text="1.导出Excel汛情模板", command=export_to_excel)
        export_word_btn = ttk.Button(self.control_frame2, text="一键生成Word报告", command=export_to_word)

        select_option1_btn = ttk.Button(self.control_frame, text="选项1全选",
                                        command=lambda: self.select_all_options(options[0]))
        select_option2_btn = ttk.Button(self.control_frame, text="选项2全选",
                                        command=lambda: self.select_all_options(options[1]))
        select_option3_btn = ttk.Button(self.control_frame, text="选项3全选",
                                        command=lambda: self.select_all_options(options[2]))

        exit_btn = ttk.Button(self.control_frame, text="退出", command=self.root.quit)

        # 将按钮放入控制框架
        buttons = [fullscreen_btn, exit_btn, clear_excel_btn, select_option1_btn,
                   select_option2_btn, select_option3_btn]
        for button in buttons:
            button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        buttons1 = [export_excel_btn, export_filtered_excel_btn, export_word_btn, export_filtered_word_btn]
        for button in buttons1:
            button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

        self.fullscreen = False

        # 创建控制按钮框架
        self.control_frame1 = ttk.Frame(self.frame)
        self.control_frame1.grid(row=13, column=0, columnspan=10, sticky='ew', pady=(10, 0), rowspan=5)
        self.create_table_sections()

    # 创建表单部分的函数
    def create_table_sections(self):
        self.table1_all_select_var, self.table1_cities_vars = self.create_table_section(
            self.control_frame1, "表1 停电退服情况 地市筛选：（已默认选择汛情期地市）",
            ["黄山", "池州", "安庆", "宣城", "六安", "合肥", "淮北", "宿州", "阜阳", "芜湖", "全省"]
        )
        self.table2_all_select_var, self.table2_cities_vars = self.create_table_section(
            self.control_frame1, "表2 光缆中断情况 地市筛选：（已默认选择汛情期地市）",
            ["黄山", "池州", "安庆", "宣城", "六安", "全省"]
        )
        self.table3_all_select_var, self.table3_cities_vars = self.create_table_section(
            self.control_frame1, "表3 高温水浸情况 地市筛选：（已默认选择汛情期地市）",
            ["黄山", "池州", "安庆", "宣城", "六安", "合肥", "淮北", "宿州", "阜阳", "芜湖", "全省"]
        )

    # 创建表单部分的辅助函数
    def create_table_section(self, parent, title_text, default_selected):
        section_frame = ttk.Frame(parent)
        section_frame.pack(fill='x', pady=5)

        # 添加标题
        title_label = ttk.Label(section_frame, text=title_text)
        title_label.pack(side='top')

        # 创建全选按钮
        all_select_var = tk.IntVar()
        all_select_button = ttk.Checkbutton(
            section_frame, text="全（不）选（√上全省）", variable=all_select_var,
            command=lambda: self.select_all_cities(all_select_var, cities_vars)
        )
        all_select_button.pack(side='top', anchor='w')

        # 城市列表
        cities = ["安庆", "蚌埠", "亳州", "池州", "滁州", "阜阳", "合肥", "淮北", "淮南", "黄山",
                  "六安", "马鞍山", "铜陵", "芜湖", "宿州", "宣城", "全省"]
        cities_vars = []

        # 创建复选框，并横向排列
        checkbutton_frame = ttk.Frame(section_frame)
        checkbutton_frame.pack(side='top', fill='x')

        for city in cities:
            var = tk.IntVar(value=city in default_selected)
            checkbutton = ttk.Checkbutton(checkbutton_frame, text=city, variable=var)
            checkbutton.pack(side='left', anchor='w', expand=True)
            cities_vars.append(var)

        return all_select_var, cities_vars

    # 选择所有城市的函数
    def select_all_cities(self, all_select_var, cities_vars):
        select_value = bool(all_select_var.get())
        for var in cities_vars:
            var.set(select_value)

    # 切换全屏模式
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    # 浏览文件
    def browse_file(self, index):
        filename = filedialog.askopenfilename(initialdir=current_path, title="选择文件",
                                              filetypes=(("all files", "*.*"), ("text files", "*.txt")))
        if filename:
            self.file_paths[index].set(filename)

    # 全选选项
    def select_all_options(self, option):
        for var in self.selected_options:
            var.set(option)


if __name__ == "__main__":
    check_path()
    root = tk.Tk()
    app = FileSelectorApp(root)
    root.mainloop()

