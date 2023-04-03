from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import function.tbox_serial as ts
import threading

class TboxSerialTool(ttk.Frame):
    '''TBOX串口工具'''

    def __init__(self, master):
        super().__init__(master, padding=15)
        self.pack(fill=BOTH, expand=YES)

        self.menu_row = ttk.Frame(self)
        self.menu_row.pack(fill=X, expand=YES, pady=(0,15))

        com_text = '串口配置'
        self.com_lf = ttk.Labelframe(self, text=com_text, padding=15)
        self.com_lf.pack(fill=X, expand=YES, anchor=N)

        cmd_text = '控制台'
        self.cmd_lf = ttk.Labelframe(self, text=cmd_text, padding=15)
        self.cmd_lf.pack(fill=X, expand=YES, anchor=N, pady=(15,0))

        self.create_menu_row()
        self.create_com_row()
        self.create_cmd_row()

    def create_menu_row(self):
        '''菜单行'''
        _style = ttk.Style()
        _theme_name = _style.theme_names()

        about_btn = ttk.Button(
            master=self.menu_row,
            text='关于',
            command=self.about,
            width=8,
            bootstyle=OUTLINE
        )
        about_btn.pack(side=LEFT)

        theme_lbl = ttk.Label(master=self.menu_row,
                        text='主题：')

        self.theme_cb = ttk.Combobox(master=self.menu_row,
                               values=_theme_name,
                               width=10)

        theme_btn = ttk.Button(master=self.menu_row,
                         text='应用',
                         command=self.change_theme
                         )

        theme_btn.pack(side=RIGHT, padx=(15,5))
        self.theme_cb.pack(side=RIGHT)
        theme_lbl.pack(side=RIGHT)

        self.theme_cb.current(_theme_name.index(_style.theme.name)) # 将初始主题名索引

    def create_com_row(self):
        '''串口配置行'''
        com_row = ttk.Frame(self.com_lf)
        com_row.pack(fill=X, expand=YES)

        port_lbl = ttk.Label(com_row, text='端口号：')
        port_lbl.pack(side=LEFT, padx=5)
        self.port_ent = ttk.Entry(com_row)
        self.port_ent.pack(side=LEFT, fill=X, expand=YES, padx=(0,5))

        baudrate_lbl = ttk.Label(com_row, text='波特率：')
        baudrate_lbl.pack(side=LEFT, padx=5)
        self.baudrate_cb = ttk.Combobox(com_row,values=[115200,230400])
        self.baudrate_cb.pack(side=LEFT, fill=X, expand=YES , padx=(0,5))

        open_btn = ttk.Button(
            master=com_row,
            text='打开串口',
            command=self.open_com,
            width=8,
        )
        open_btn.pack(side=LEFT, padx=(10,0))

        close_btn = ttk.Button(
            master=com_row,
            text='关闭串口',
            command=self.close_com,
            width=8,
        )
        close_btn.pack(side=LEFT, padx=(10,0))

    def create_cmd_row(self):
        '''控制台配置行'''
        cmd_row = ttk.Frame(self.cmd_lf)
        cmd_row.pack(fill=X, expand=YES)

        print_log_Thread_start_btn = ttk.Button(
            master=cmd_row,
            text='开启打印',
            command=self.print_log_Thread_start
        )
        print_log_Thread_start_btn.pack(side=LEFT, padx=(0,5), expand=YES, fill=X)

        print_log_Thread_stop_btn = ttk.Button(
            master=cmd_row,
            text='停止打印',
            command=self.print_log_Thread_stop
        )
        print_log_Thread_stop_btn.pack(side=LEFT, padx=(0,5), expand=YES, fill=X)

        save_log_Thread_start_btn = ttk.Button(
            master=cmd_row,
            text='开始保存',
            command=self.save_log_Thread_start
        )
        save_log_Thread_start_btn.pack(side=LEFT, padx=(0,5), expand=YES, fill=X)

        save_log_Thread_stop_btn = ttk.Button(
            master=cmd_row,
            text='停止保存',
            command=self.save_log_Thread_stop
        )
        save_log_Thread_stop_btn.pack(side=LEFT, padx=(0,5), expand=YES, fill=X)

    #

    def open_com(self):
        baudrate = int(self.baudrate_cb.get())
        self.com = ts.tbox_serial(port=self.port_ent.get(), baudrate=baudrate)

    def close_com(self):
        self.com.serial_close()

    #

    def print_log(self):
        while self.t1Flag:
            self.com.print_log()

    def print_log_Thread_start(self):
        self.t1Flag = True
        self.com.split_line('开启打印')
        t1 = threading.Thread(target=self.print_log)
        t1.start()

    def print_log_Thread_stop(self):
        self.t1Flag = False
        self.com.split_line('停止打印')

    #

    def save_log(self):
        while self.t2Flag:
            self.com.save_log()

    def save_log_Thread_start(self):
        self.t2Flag = True
        self.com.split_line('开始保存')
        t2 = threading.Thread(target=self.save_log)
        t2.start()

    def save_log_Thread_stop(self):
        self.t2Flag = False
        self.com.split_line('停止保存')

    #

    def about(self):
        tk.messagebox.showinfo('关于 TBOX串口工具',
                               '作者：Jer小铭\n'
                               '版本：v1.0\n'
                               '时间：2023-03-30\n'
                               '思路提供：Mavis\n'
                               '技术支持：孟桂大神\n'
                               '\n特别鸣谢大神对本程序的大力支持')

    def change_theme(self):
        '''获取theme_cb的值（主题名），并应用主题'''
        print(f'正在应用主题：{self.theme_cb.get()}')
        t = self.theme_cb.get()
        ttk.Style().theme_use(t)

if __name__ == '__main__':

    app = ttk.Window('TBOX串口工具', 'minty')
    TboxSerialTool(app)
    version = ttk.Label(app, text='版本：v1.0')
    version.pack(side=RIGHT, padx=15)
    app.place_window_center()    #让显现出的窗口居中
    app.resizable(False,False)   #让窗口不可更改大小
    app.mainloop()