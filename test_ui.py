# -*-co

import sys
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication
from Ui_update import Ui_Update
import os
from type import EasyUnzipConfig
import json
import re
import subprocess
import time
import threading
import psutil
from tool import JThread


class MyMainWin(Ui_Update):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # 配置路径
        self.config_url = "./config.json"
        '''配置路径'''
        self.pw_url = "./pw.json"
        '''密码路径'''
        self.history_url = "./history.json"
        '''历史路径'''
        self.unzip_log_url = "./unzip.log"
        '''解压日志'''
        self.config: EasyUnzipConfig = EasyUnzipConfig()
        self.subp: subprocess.Popen[bytes] | None = None
        self.t1: JThread | None = None
        self.is_unzip: bool = False

        self.history_key_list = ["val_input_zip_list", "val_output_dir", "select_pw", "is_unzip_del",
                                 "is_loop_unzip", "is_unzip_self", "is_single_zip", "is_autosave_pw", "is_try_pw", "is_autoexit", "select_sort_pw", "select_overwrite", "select_main_exe"]
        # print(getJson(self.config))
        # self.config.__dict__ for ob in
        self.__init_config()
        # 监听事件
        self.btn_setdefault.clicked.connect(self.default_set_config)
        self.btn_save_config.clicked.connect(self.save_configdata)
        self.btn_reset_default.clicked.connect(self.default_set_origin_config)
        self.btn_unzip.clicked.connect(self.unzip)
        self.btn_save_history.clicked.connect(self.save_history)
        self.btn_cancel_unzip.clicked.connect(self.cancel_unzip)

        pass
        # self.setupUi(self)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # return super().closeEvent(a0)
        if self.subp == None:
            return
        self.subp.communicate()
        self.subp = None

    def __init_config(self):
        '''配置初始化'''
        # 读取配置
        if os.path.exists(self.config_url) == False:
            with open(self.config_url, 'w', encoding="utf-8") as f:
                f.write(json.dumps(self.config.tojson()))
                pass
        else:
            with open(self.config_url, 'r', encoding="utf-8") as f:
                s = f.read()
                self.config.loadjson(s)
            pass
        # 应用默认配置
        self.init_default_config()
        # 如果有历史则读取历史
        self.load_history()

    def init_default_config(self):
        '''初始化默认配置'''
        for key in self.config.__dict__:
            if re.match(r'^is_.*', key, re.M) != None:
                setattr(self, key, getattr(self.config, key))
        self.val_zip_url = self.config.val_zip_url
        self.default_set_config()
        pass

    def default_set_origin_config(self):
        '''恢复原始默认配置(读取url)'''
        with open(self.config_url, 'r', encoding="utf-8") as f:
            s = f.read()
            j = json.loads(s)
            for key in j:
                if re.match(r'^is_default_.*', key, re.M) != None or re.match(r'^select_default_.*', key, re.M) != None:
                    a = key.split("_")
                    a.pop(1)
                    otherkey = '_'.join(a)
                    setattr(self, otherkey, j[key])
        pass

    def default_set_config(self):
        '''恢复默认配置'''
        for key in dir(self):
            if re.match(r'^is_default_.*', key, re.M) != None or re.match(r'^select_default_.*', key, re.M) != None:
                a = key.split("_")
                a.pop(1)
                otherkey = '_'.join(a)
                setattr(self, otherkey, getattr(self, key))
                pass
        self.init_common()
        pass

    def save_configdata(self):
        '''保存配置数据'''
        for key in dir(self):
            if re.match(r'^is_default_.*', key, re.M) != None or re.match(r'^select_default_.*', key, re.M) != None:
                setattr(self.config, key, getattr(self, key))
                pass
        self.config.val_zip_url = self.val_zip_url
        j = self.config.tojson()
        with open(self.config_url, 'w', encoding='utf-8') as f:
            f.write(json.dumps(j))
        pass

    def init_common(self):
        '''初始化通用'''
        self.unzip_self_event()

    def unzip_one(self, input: str, pw: str | None = None):
        '''解压单文件'''
        # 选择程序
        exe = ""
        if self.select_main_exe == "命令行":
            exe += '7z.exe'
        elif self.select_main_exe == "图形GUI":
            exe += '7zG.exe'
        cmd = f'"{self.val_zip_url}/{exe}"'
        # 需要解压的文件
        cmd += ' x '
        cmd += f'"{input}" -o'
        # 输出目录
        output = self.val_output_dir
        if self.is_unzip_self == True:
            output = os.path.join(os.path.dirname(input),
                                  os.path.splitext(os.path.basename(input))[0])
        # print(output)
        # if os.path.exists(output) == False:
        #     os.makedirs(output)
        cmd += f'"{output}"'
        # 密码
        if pw != None and pw != "":
            cmd += f' -p"{pw}"'
        # 覆盖模式
        match self.select_overwrite:
            case "直接覆盖":
                cmd += ' -aoa'
            case "跳过不覆盖":
                cmd += ' -aos'
            case "重命名新文件":
                cmd += ' -aou'
            case "重命名旧文件":
                cmd += ' -aot'

        # 添加日志
        cmd += ' -bb3'
        # 改写输出的字符串编码
        cmd += ' -sccUTF-8'
        # 改写文件编码
        if self.select_encoding != None and self.select_encoding != "":
            cmd += f' -mcp={self.select_encoding}'
        print(cmd)
        # 执行命令
        # self.subp = subprocess.Popen(
        #     cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # while self.subp.poll() is None:
        #     if self.subp.stdout == None:
        #         break
        #     output = self.subp.stdout.readline()
        #     if output:
        #         # output = output.decode("gb2312").strip()
        #         output = output.decode("utf-8").strip()
        #         print(output)
        #     else:
        #         break
        #     time.sleep(1)

        def set_thread():
            self.subp = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            while self.subp != None and self.subp.poll() is None:
                if self.subp.stdout == None:
                    break
                output = self.subp.stdout.readline()
                if output and self.is_unzip == True:
                    output = output.decode("utf-8").strip()
                    print(output)
                else:
                    break
            self.is_unzip = False
            # time.sleep(1)
        self.is_unzip = True
        self.t1 = JThread(target=set_thread)
        self.t1.start()

        print("完成")
        pass

    def cancel_unzip(self):
        '''取消解压'''
        print("触发停止解压指令")
        self.is_unzip = False
        if self.subp != None:
            print("正在关闭命令行")
            pobj = psutil.Process(self.subp.pid)
            for c in pobj.children(recursive=True):
                c.kill()
            pobj.kill()
            self.subp = None
            print("关闭命令行结束")
        if self.t1 != None:
            print("正在关闭线程")
            self.t1.stop()
            self.t1 = None
            print("关闭线程结束")

    def unzip(self):
        '''解压'''
        s = self.val_input_zip_list
        list = s.splitlines()
        for f in list:
            f = f.strip()
            if f == None or f == "":
                continue
            self.unzip_one(f, self.select_pw)
            pass
        pass

    def save_history(self):
        '''保存历史'''
        j = {}
        for key in self.history_key_list:
            a = getattr(self, key)
            if a == None:
                continue
            j[key] = a
        with open(self.history_url, "w", encoding="utf") as f:
            f.write(json.dumps(j))

    def load_history(self):
        '''读取历史'''
        if os.path.exists(self.history_url) == False:
            return
        with open(self.history_url, "r", encoding="utf-8") as f:
            s = f.read()
            if s == None or s == "":
                return
            j = json.loads(s)
            for key in self.history_key_list:
                if j[key] == None:
                    continue
                setattr(self, key, j[key])


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mywin = MyMainWin()
    mywin.show()
    sys.exit(app.exec())
    pass
