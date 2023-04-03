# encoding=utf-8

import serial
import datetime
import time

class tbox_serial():
    """参考丽敏同学写的一个tbox串口函数，可以用来实现log打印，log关键字搜索等等"""

    def __init__(self, port:str , baudrate:int):
        """
        打开串口\n
        :param port: 串口的端口号
        :param baudrate: 串口的波特率, mcu是230400, mpu是115200
        """

        self.com = serial.Serial(port=port, baudrate=baudrate)
        self.split_line(f'连接串口中，端口号：{port}，波特率：{baudrate}')

        if self.com.isOpen():
            self.split_line(f'串口连接成功！')
        else:
            self.split_line(f'串口连接失败，请检查端口是否被占用！')

    def serial_close(self):
        self.com.close()
        self.split_line('串口断开连接')

    def print_log(self):
        """打印一行带时间戳的串口数据，配合while True函数可以实现一直打印"""
        data = self.com.readline() # 读取一行数据
        log = f'[{datetime.datetime.now()}] {data}' # 增加时间戳
        print(log)

    def save_log(self, log_name:str = 'log'):
        """
        保存log到本地\n
        :param log_name: log的名字
        """
        data = self.com.readline() # 读取一行数据
        log = f'[{datetime.datetime.now()}] {data}' # 增加时间戳
        f = open(f'./{log_name}.txt', 'a') #
        print(log,file=f)

    def login_mpu(self,
                  user_name:str = 'root',
                  password:str = 'bdstar2022*'):
        """
        输入第一次进入mpu串口时，所需的用户名和密码\n
        :param user_name: 用户名
        :param password: 密码
        """

        user_name1 = user_name + '\r\n'
        password1 = password + '\r\n'

        self.com.write(user_name1.encode("utf-8")) # 输入utf-8格式的指令
        self.split_line(f'正在输入用户名：{user_name},等待1秒...')
        time.sleep(1)

        self.com.write(password1.encode("utf-8")) # 输入utf-8格式的指令
        self.split_line(f'正在输入密码：{password},等待1秒...')
        time.sleep(1)

    def findkey(self,
                key:str = 'Tx',
                action = lambda:print('>' * 10, f' 匹配到关键字后，执行的动作 ', '<' * 10)
                ):
        """
        根据关键字匹配，执行动作\n
        :param key: 要匹配的关键字
        :param action: 匹配到关键字后，执行的动作
        """
        data = self.com.readline() # 读取一行数据
        log = f'[{datetime.datetime.now()}] {data}'
        print(log)
        if key in log:
            action() # 执行动作

    def split_line(self, text:str='split_line'):
        """
        生成一条分割线\n
        :param text: 分割线中间的文本
        :return: 不返回值
        """
        print('>' * 10, f' {text} ', '<' * 10)

if __name__ == '__main__':

    com = tbox_serial(port='COM44', baudrate=230400)
    while True:
        com.print_log()
    # com.serial_close()
