from Ui_update import Ui_Unzip_Program_Update
import re
from tool import JQCmd, JThread, jindexof

import time


class JUnzip():

    def __init__(self) -> None:
        self.exe: str = ""
        '''当前的程序'''
        self.inputfile: str = ""
        '''输入的文件'''
        self.outputdir: str = ""
        '''输出的文件夹'''
        self.pw: str = ""
        '''解压的密码'''
        self.overwrite: str = "-aoa"
        '''覆盖模式'''
        self.encoding: str = ""
        '''文件代码模式'''
        self.current_pwlist: list[str] = []
        '''当前的密码列表'''
        self.used_pwlist: list[str] = []
        '''当前已经使用过的密码'''

        self.jcmd = JQCmd()
        '''专用命令行工具'''
        self.t1: JThread
        '''专用线程工具'''

        self.ui_unzip_program = Ui_Unzip_Program_Update()
        '''解压窗口'''

        self.jcmd.output.connect(self.unzip_msg_event)
        self.starttime = time.time()
        pass

    def unzip_msg_event(self, d):
        s: str = d[1]
        self.ui_unzip_program.msg_add(d[1])
        if re.match(r'^-\s', s, re.M | re.I):
            self.ui_unzip_program.progress_add()
        elif re.match(r'^Everything is Ok', s):
            self.ui_unzip_program.progress_settext(
                f'解压完成,共解压了{self.ui_unzip_program.progress_currentcount}个文件')
            self.cancel()
            pass
        elif re.match(r'^Cannot open encrypted archive\. Wrong password\?', s) or re.match(r'^ERROR: Wrong password', s):
            self.cancel()
            nextpw = self.get_nextpw()
            if nextpw == "":
                self.ui_unzip_program.progress_settext("密码错误!,无法解压")
            else:
                self.ui_unzip_program.progress_settext(f'密码错误!,尝试"{nextpw}"')
                self.used_pwlist.append(nextpw)
                self.pw = nextpw
                time.sleep(2)
                self.run()
            pass
        # print(d[1])
        pass

    def reset_cmddata(self):
        self.exe: str = ""
        '''当前的程序'''
        self.inputfile: str = ""
        '''输入的文件'''
        self.outputdir: str = ""
        '''输出的文件夹'''
        self.pw: str = ""
        '''解压的密码'''
        self.overwrite: str = "-aoa"
        '''覆盖模式'''
        self.encoding: str = ""
        pass

    def cancel(self):
        self.jcmd.cancel()
        if getattr(self, "t1"):
            self.t1.stop()
        pass

    def get_nextpw(self):
        '''获取下个密码'''
        for k in self.current_pwlist:
            if jindexof(self.used_pwlist, k) == -1:
                return k
        return ""

    def run(self):
        # 选择程序
        cmd = self.exe+" "
        # 解压标志
        cmd += 'x '
        # 需要解压的压缩文件
        cmd += f'"{self.inputfile}" '
        # 需要解压到的文件夹
        cmd += f'-o"{self.outputdir}" '
        # 输入密码
        if self.pw and self.pw != "":
            cmd += f'-p"{self.pw}" '
        # 覆盖模式
        cmd += f'{self.overwrite} '
        # 添加日志
        cmd += ' -bb3'
        # 改写输出的字符串编码
        # cmd += ' -sccUTF-8'
        # 改写文件编码
        if self.encoding and self.encoding != "":
            cmd += f' -mcp={self.encoding}'
        print(cmd)

        def set_thread():
            self.jcmd.run(cmd)

        self.t1 = JThread(set_thread)
        self.t1.start()
        pass

    def showui(self, title: str):
        '''展示ui'''
        self.ui_unzip_program.setWindowTitle(title)
        self.ui_unzip_program.show()
