from collections.abc import Callable
from Ui_update import Ui_Unzip_Program_Update, overwrite_type
import re
from tool import jindexof, jcmd_final_type
from PyQt6.QtCore import QThread, pyqtSignal
from abc import ABCMeta, abstractmethod, ABC


import psutil
import time
import tempfile
from typing import Literal


junzip_type = Literal["unzip", "getMsg"]


class Meta(type(ABC), type(QThread)):
    pass


class JCommonUIAbstract(ABC, QThread, metaclass=Meta):

    outputSingal = pyqtSignal(tuple)
    '''输出信号'''
    finalSingal = pyqtSignal(tuple)
    '''结束信号'''

    unzip_cb: Callable[[jcmd_final_type,str], None] | None = None
    '''解压回调'''

    def __init__(self) -> None:
        super().__init__()
        self.finalType: jcmd_final_type = "success"
        self.finalMsg: str = ""
        self.unzip_type: junzip_type = "unzip"

    @abstractmethod
    def ab_final_event(self, d):
        ''' 继承用的'''

        # print(d)
        pass

    @abstractmethod
    def ab_unzip_msg_event(self, d):
        ''' 继承用的'''

        # print(d)
        pass

    @abstractmethod
    def ab_reset_cmddata(self):
        ''' 继承用的'''

        pass

    @abstractmethod
    def ab_cancel(self):
        '''取消执行(继承用)'''

        print("触发停止解压指令")
        self.finalType = "cancel"
        self.finalMsg = "强制退出"
        self.terminate()
        self.finalSingal.emit((self.finalType, self.finalMsg, self.unzip_type))
        pass

    @abstractmethod
    def ab_get_zipmsg(self):
        '''获取压缩包信息'''
        pass

    @abstractmethod
    def ab_unzip(self):
        '''解压'''
        pass

    @abstractmethod
    def ab_run(self):
        pass


class JCommonUI(JCommonUIAbstract):

    def __init__(self) -> None:
        super().__init__()

        self.inputfile: str = ""
        '''输入的文件'''
        self.outputdir: str = ""
        '''输出的文件夹'''
        self.pw: str = ""
        '''解压的密码'''
        self.encoding: str = ""
        '''文件代码模式'''
        self.current_pwlist: list[str] = []
        '''当前的密码列表'''
        self.used_pwlist: list[str] = []
        '''当前已经使用过的密码'''
        self.overwrite_type: overwrite_type = "直接覆盖"
        '''覆盖模式'''
        self.ui_unzip_program = Ui_Unzip_Program_Update()
        '''解压窗口'''

        self.is_check_msg = False

        self.outputSingal.connect(self.ab_unzip_msg_event)
        self.starttime = time.time()

        self.finalSingal.connect(self.ab_final_event)
        self.files_count = 0
        '''文件总数'''
        self.folders_count = 0
        '''文件夹总数'''
        pass

    def reset_status(self):
        '''重置状态'''
        self.reset_cmddata()
        self.is_check_msg = False
        pass

    def reset_cmddata(self):
        self.exe: str = ""
        '''当前的程序'''
        self.inputfile: str = ""
        '''输入的文件'''
        self.outputdir: str = ""
        '''输出的文件夹'''
        self.pw: str = ""
        '''覆盖模式'''
        self.encoding: str = ""
        self.ab_reset_cmddata()
        pass

    def cancel(self):
        '''取消执行'''

        self.ab_cancel()

    def get_nextpw(self):
        '''获取下个密码'''
        print(self.current_pwlist, self.used_pwlist)
        for k in self.current_pwlist:
            if jindexof(self.used_pwlist, k) == -1:
                return k
        print("没有密码可取")
        return ""

    def run(self):
        self.ab_run()

    def showui(self, title: str):
        '''展示ui'''
        self.ui_unzip_program.progress_currentcount = 0
        self.ui_unzip_program.progress_settext("解压开始!")
        self.ui_unzip_program.msg_clear()
        self.ui_unzip_program.setWindowTitle(title)
        self.ui_unzip_program.show()
