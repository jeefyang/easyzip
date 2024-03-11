from cgitb import text
import random
from typing import Callable, Literal
from collections.abc import Callable, Iterable, Mapping
from typing import Any, TypeVar
import json
import threading
import time
import subprocess
import psutil
from PyQt6.QtCore import QObject, QThread, pyqtSignal

T = TypeVar("T")


def getJson(j: object):
    '''快速获取json'''
    if hasattr(j, "__dict__") == False:  # 普通类型
        return j
    o = {}
    for key in j.__dict__:
        attr = getattr(j, key)
        if isinstance(attr, list):
            for c in attr:
                o[key] = []
                o[key].append(getJson(c))
                pass
        elif hasattr(attr, "__dict__") == True:
            o[key] = getJson(attr)  # type:ignore
        else:
            o[key] = attr
    return o


class QJson():
    '''快速json对象,子属性只适用普通类型,不能套娃!!!'''

    def __init__(self) -> None:
        pass

    def tojson(self):
        return getJson(self)

    def loadjson(self, s: str):
        j = json.loads(s)
        for key in j:
            setattr(self, key, j[key])
        pass


def jindexof(list: list[T], d: T) -> int:
    try:
        return list.index(d)
    except:
        return -1


class JThread(threading.Thread):
    '''自制线程器'''

    def __init__(self, target, args=()):
        super(JThread, self).__init__()
        self.target = target
        self.args = args
        self.stop_event = threading.Event()

    def pause(self):
        self.stop_event.wait()

    def resume(self):
        self.stop_event.clear()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            self.target(*self.args)
            time.sleep(1)

        # while not self.stop_event.is_set():
        #     self.target(*self.args)
        #     time.sleep(1)


jcmd_final_type = Literal["success", "error", "cancel","normal","pwwrong"]


class JQCmd(QThread):

    output = pyqtSignal(tuple)
    final = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(JQCmd, self).__init__(parent)
        self.working = True
        self.subp: subprocess.Popen[str] | None = None
        '''命令行对象'''

    def __del__(self):
        self.working = False
        self.wait()

    def run(self, cmd: str):
        ''''''
        finaltype: jcmd_final_type = "success"
        self.subp = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)

        while self.subp != None and self.subp.poll() is None and self.working == True:
            try:
                if self.subp.stderr != None:
                    error_output = self.subp.stderr.readline()
                    if error_output:
                        error_output = error_output.strip()
                        self.output.emit(("error", error_output))
                        continue
                if self.subp == None or self.subp.stdout == None:
                    break
                output = self.subp.stdout.readline()
                if output:
                    output = output.strip()
                    self.output.emit(("success", output))
                else:
                    break
                pass
            except:
                self.output.emit(("error", "退出失败"))
                finaltype = "error"
                break

        self.final.emit((finaltype, ""))

        pass

    def cancel(self):
        '''取消执行'''
        print("触发停止解压指令")
        if self.subp != None:
            print("正在关闭命令行", self.subp.pid)
            try:
                pobj = psutil.Process(self.subp.pid)
                for c in pobj.children(recursive=True):
                    c.kill()
                pobj.kill()
                self.subp = None
            except:
                if self.subp != None:
                    self.subp.kill()
                print("无法结束命令行,只能强行触发kill命令")
                self.subp = None
            print("关闭命令行结束")
        self.final.emit(("cancel", ""))


class JCmd():

    def __init__(self) -> None:
        self.output_fun: Callable[[jcmd_final_type, str], None] | None = None
        '''实时输出的方法'''
        self.final_fun: Callable[[jcmd_final_type], None] | None = None
        '''完成的方法'''
        self.err_fun: Callable[[str], None] | None = None
        '''错误的方法'''
        self.subp: subprocess.Popen[str] | None = None
        '''命令行对象'''
        self.t1: JThread | None = None
        '''线程对象'''
        self.isrun = False
        '''是否正在运行'''
        pass

    def on_output(self, cb: Callable[[jcmd_final_type, str], None]) -> None:
        '''实时输出事件'''
        self.output_fun = cb
        pass

    def on_err(self, cb: Callable[[str], None]) -> None:
        '''错误输出事件'''
        self.err_fun = cb
        pass

    def on_final(self, cb: Callable[[jcmd_final_type], None]) -> None:
        '''完成事件'''
        self.final_fun = cb
        pass

    def cmd(self, cmd: str):

        def set_thread():
            finaltype: jcmd_final_type = "success"
            self.subp = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
            while self.subp != None and self.subp.poll() is None and self.isrun == True:
                try:
                    if self.subp.stderr != None:
                        error_output = self.subp.stderr.readline()
                        if error_output and self.output_fun:
                            error_output = error_output.strip()
                            self.output_fun("error", error_output)
                            continue
                    if self.subp == None or self.subp.stdout == None:
                        break
                    output = self.subp.stdout.readline()
                    if output and self.output_fun:
                        output = output.strip()
                        self.output_fun("success", output)
                    else:
                        break
                    pass
                except:
                    if self.output_fun:
                        self.output_fun("error", "退出失败")
                    finaltype = "error"
                    break

            if self.final_fun:
                self.final_fun(finaltype)
        self.isrun = True
        self.t1 = JThread(target=set_thread)
        self.t1.start()
        pass

    def cancel(self):
        '''取消执行'''
        print("触发停止解压指令")
        self.isrun = False
        if self.subp != None:
            print("正在关闭命令行", self.subp.pid)
            try:
                pobj = psutil.Process(self.subp.pid)
                for c in pobj.children(recursive=True):
                    c.kill()
                pobj.kill()
                self.subp = None
            except:
                if self.subp != None:
                    self.subp.kill()
                print("无法结束命令行,只能强行触发kill命令")
                self.subp = None
            print("关闭命令行结束")
        if self.t1 != None:
            print("正在关闭线程")
            self.t1.stop()
            self.t1 = None
            print("关闭线程结束")
        if self.final_fun:
            self.final_fun("cancel")
