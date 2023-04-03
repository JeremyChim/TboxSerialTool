import ttkbootstrap as ttk
from ttkbootstrap.constants import *
#导入第三方库

import ui.window as ui
#导入自定义函数

app = ttk.Window("TBOX串口工具", "minty")
ui.TboxSerialTool(app)

version = ttk.Label(app, text="版本：v1.0")
version.pack(side=RIGHT, padx=15, pady=1)

app.place_window_center()    #让显现出的窗口居中
app.resizable(False,False)   #让窗口不可更改大小

app.mainloop()