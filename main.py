from traitlets import Int
from tool import JThread, jindexof, jcmd_final_type

import time
import re
import json
from type import EasyUnzipConfig
import os
from Ui_update import Ui_Main_Update, Ui_Unzip_Program_Update
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow
from PyQt6.QtGui import QCloseEvent
import sys
from junzip import JUnzip
from jqunzip import JQUnzip
from jzip import JZipUI


class MyMainWin(Ui_Main_Update):

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
        self.unzip_trim_url = "./trim.json"
        '''微调字段'''
        self.config: EasyUnzipConfig = EasyUnzipConfig()
        '''配置数据'''
        self.pwlist: list[list[str | int]] = []
        '''密码数据列表'''

        self.history_key_list = ["val_input_zip_list", "val_output_dir", "select_pw", "is_unzip_del",
                                 "is_loop_unzip", "is_unzip_self", "is_single_zip", "is_autosave_pw", "is_try_pw", "is_autoexit", "select_sort_pw", "select_overwrite", "select_main_exe"]
        '''用于保存历史的关键字段'''

        # print(getJson(self.config))
        # self.config.__dict__ for ob in

        # self.junzip = JUnzip()
        # self.zipUI = JQUnzip()
        self.zipUI = JZipUI()
        # self.junzip= JUnzip()

        self.__init_config()
        # 监听事件
        self.btn_setdefault.clicked.connect(self.default_set_config)
        self.btn_save_config.clicked.connect(self.save_configdata)
        self.btn_reset_default.clicked.connect(self.default_set_origin_config)
        self.btn_unzip.clicked.connect(self.unzip)
        self.btn_save_history.clicked.connect(self.save_history)
        self.btn_cancel_unzip.clicked.connect(self.closeEvent)
        self.btn_add_pw.clicked.connect(self.add_pw_one_event)
        self.btn_del_pw.clicked.connect(self.del_pw)
        self.btn_add_pwlist.clicked.connect(self.add_pwlist_event)

        # self.junzip.ui_unzip_program.btn_unzip_close.clicked.connect(
        #     self.closeEvent)
        # self.junzip.ui_unzip_program.closeEvent = self.closeEvent

        self.zipUI.ui_unzip_program.btn_unzip_close.clicked.connect(
            self.closeEvent)
        self.zipUI.ui_unzip_program.closeEvent = self.closeEvent

        pass
        # self.setupUi(self)

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        # return super().closeEvent(a0)

        # self.junzip.cancel()
        self.zipUI.cancel()

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
        # 读取密码
        if os.path.exists(self.pw_url) == False:
            with open(self.pw_url, 'w', encoding='utf-8') as f:
                f.write(json.dumps(self.pwlist))
        else:
            with open(self.pw_url, 'r', encoding="utf-8") as f:
                s = f.read()
                self.pwlist = json.loads(s)
            pass
        # 应用默认配置
        self.init_default_config()
        # 密码列表配置
        self.init_pwlist()
        # 如果有历史则读取历史
        self.load_history()

    def del_pw(self):
        '''删除密码'''
        a = list(map(lambda x: x[0], self.pwlist))
        index = jindexof(a, self.select_pw)
        if index == -1:
            return
        self.pwlist.pop(index)
        self.save_pwlist()
        self.init_pwlist()
        self.select_pw = ""
        pass

    def add_pw_count(self, pw: str | None):
        '''添加密码次数'''
        if pw == "" or pw == None:
            return
        a = list(map(lambda x: x[0], self.pwlist))
        index = jindexof(a, pw)
        if index == -1:
            self.add_pw()
            pass
        a = list(map(lambda x: x[0], self.pwlist))
        index = jindexof(a, pw)
        self.pwlist[index][2] += 1  # type:ignore
        self.save_pwlist()

    def init_pwlist(self):
        '''初始化密码'''
        def sortname(e: list[str | int]):
            return e[0]

        def sortdate(e: list[str | int]):
            return e[1]

        def sortcount(e: list[str | int]):
            return e[2]
        l = list(map(lambda a: a, self.pwlist))
        if self.select_default_sort_pw == "名称":
            l.sort(key=sortname)
        elif self.select_default_sort_pw == "日期":
            l.sort(key=sortdate)
        elif self.select_default_sort_pw == "次数":
            l.sort(key=sortcount)

        self.combo_pw.clear()
        for d in l:
            self.combo_pw.addItem(str(d[0]))
            pass

        # self.junzip.current_pwlist = list(
        #     map(lambda a: str(a[0]), self.pwlist))

        self.zipUI.current_pwlist = list(
            map(lambda a: str(a[0]), self.pwlist))

    def add_pw_one_event(self):
        ''' 添加当前密码'''
        pw = self.combo_pw.currentText()
        self.add_pw(pw, True)

    def add_pw(self, pw: str = "", is_save: bool = True):
        '''添加密码'''
        if pw == "":
            pw = self.select_pw
        if pw == None or pw == "":
            print("没有密码可添加")
            return
        a = list(map(lambda x: x[0], self.pwlist))
        if jindexof(a, pw) != -1:
            print("密码已经存在")
            return
        a = [pw, int(round(time.time()*1000)), 0]
        self.pwlist.append(a)
        if is_save == True:
            self.save_pwlist()
            self.init_pwlist()

    def add_pwlist_event(self):
        '''添加密码列表事件'''
        url = QFileDialog.getOpenFileName(self, "选取单个文件")[0]
        with open(url, 'r', encoding='utf-8') as f:
            s = f.read()
            self.add_pwlist(s)
        pass

    def add_pwlist(self, s: str):
        '''添加密码列表'''
        a = s.splitlines()
        for k in a:
            self.add_pw(k, False)
        self.save_pwlist()
        self.init_pwlist()
        pass

    def save_pwlist(self):
        '''保存密码'''
        with open(self.pw_url, "w", encoding='utf-8') as f:
            f.write(json.dumps(self.pwlist))
        pass

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

        # self.junzip.exe = f'"{self.val_zip_url}/{exe}"'
        self.zipUI.exe = f'"{self.val_zip_url}/{exe}"'

        # 需要解压的文件
        # self.junzip.inputfile = input
        self.zipUI.inputfile = input

        # 输出目录
        output = self.val_output_dir
        if self.is_unzip_self == True:
            output = os.path.join(os.path.dirname(input),
                                  os.path.splitext(os.path.basename(input))[0])
        # print(output)
        # if os.path.exists(output) == False:
        #     os.makedirs(output)

        # self.junzip.outputdir = output
        self.zipUI.outputdir = output

        # 密码
        # self.junzip.pw = ""
        self.zipUI.pw = ""

        if pw != None and pw != "":

            # self.junzip.pw = pw
            self.zipUI.pw = pw

        self.zipUI.overwrite_type = self.select_overwrite
        print(f"解压覆盖模式:{self.zipUI.overwrite_type}")
        # self.junzip.encoding = self.select_encoding
        # self.junzip.run()

        self.zipUI.encoding = self.select_encoding

        self.zipUI.start()

    def unzip_loop(self, slist: list[str], i: int):
        '''解压循环'''

        if i >= len(slist):
            print("打完收工")
            # time.sleep(2)
            # self.zipUI.ui_unzip_program.hide()
            return

        f = slist[i]

        def cb(t: jcmd_final_type, s):
            print(f"解压完成,密码使用了: {s} ")
            if t == "success" and s:
                self.add_pw_count(s)
                self.save_pwlist()
                self.init_pwlist()
            if t == "pwwrong":
                print(f"{f} 没有可用的密码")
            self.unzip_loop(slist, i+1)

        self.zipUI.unzip_cb = cb

        if f == None or f == "":
            return self.unzip_loop(slist, i+1)
        self.zipUI.showui(os.path.basename(f))
        if self.select_pw:

            # self.junzip.used_pwlist = [self.select_pw]
            self.zipUI.used_pwlist = [self.select_pw]

        else:

            # self.junzip.used_pwlist = []
            self.zipUI.used_pwlist = []
        self.zipUI.reset_status()
        self.unzip_one(f, self.select_pw)
        pass

    def unzip(self):
        '''解压'''

        self.zipUI.set_cacheOutput("./.cache")
        s = self.val_input_zip_list
        slist = s.splitlines()
        self.unzip_loop(slist, 0)
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
