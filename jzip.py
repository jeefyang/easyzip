import os
import zipfile
import tarfile
from numpy import void
import py7zr
from unrar import rarfile

from Ui_update import Ui_Unzip_Program_Update
import re
from tool import jindexof, jcmd_final_type
from PyQt6.QtCore import QThread, pyqtSignal

import subprocess
import psutil
import time
import tempfile
from typing import List, Literal
from jcommonUI import JCommonUI, junzip_type, overwrite_type
from collections.abc import Callable
import os
from pathlib import Path
from lzma import LZMAError

# import pyzipper


class JZip():

    cacheOutput: str = "./"
    listcb: Callable[[int], None] | None = None
    msgcb: Callable[[str], None] | None = None
    finalcb: Callable[[str], None] | None = None
    wrongpwcb: Callable[[str], None] | None = None
    overwrite: overwrite_type = "直接覆盖"

    def checkzip(self, url: str):

        if zipfile.is_zipfile(url):
            return "zip"
        if rarfile.is_rarfile(url):
            return "rar"
        if py7zr.is_7zfile(url):
            return "7z"
        return "null"

    def check_overwrite(self, info: str, outpath: str) -> str:
        if self.overwrite == "直接覆盖":
            return info
        f = os.path.join(outpath, info)
        if os.path.exists(f) and os.path.isfile(f):
            if self.overwrite == "跳过不覆盖":
                return ""
            if self.overwrite == "重命名旧文件":
                name = os.path.splitext(f)[0]
                ex = os.path.splitext(f)[-1]
                os.rename(f, f'{name}(1){ex}')
                return info
            if self.overwrite == "重命名新文件":
                name = os.path.splitext(f)[0]
                ex = os.path.splitext(f)[-1]
                return self.check_overwrite(f'{name}(1){ex}', outpath)
        return info

    def extract(self, ziprar: zipfile.ZipFile | rarfile.RarFile, outpath: str,  type: Literal['zip', 'rar', '7z'], sevenZlist: List[str] | None = None, sevenZ: py7zr.SevenZipFile | None = None):
        if sevenZlist == None:
            sevenZlist = ziprar.namelist()
        if self.listcb:
            self.listcb(len(sevenZlist))
        for info in sevenZlist:
            newinfo = self.check_overwrite(info, outpath)
            if not newinfo:
                if self.msgcb:
                    x = info.encode("cp437").decode(
                        "gbk") if type == "zip" else info
                    self.msgcb(f"{x} 重名跳过")
                continue
            dir = outpath
            name = newinfo
            if newinfo != info:  # 需要重名
                dir = self.cacheOutput
                name = info
                if self.msgcb:
                    x = info.encode("cp437").decode(
                        "gbk") if type == "zip" else info
                    newx = newinfo.encode("cp437").decode(
                        "gbk") if type == "zip" else newinfo
                    self.msgcb(f"{x} 重名为 {newx}")
            else:
                if self.msgcb:
                    self.msgcb(info)

            # print(name)
            p: str = ""
            if sevenZ:
                sevenZ.extract(dir, [name])
                p = os.path.join(dir, name)
            else:
                p = ziprar.extract(name, dir)
            if type == "zip":  # 转码
                name = name.encode("cp437").decode("gbk")
                newinfo = newinfo.encode("cp437").decode("gbk")
                Path(p).rename(os.path.join(
                    dir, name))

            if newinfo != info:  # 需要重名
                os.rename(os.path.join(dir, name),
                          os.path.join(outpath, newinfo))
                pass
        pass

    def unzip(self, url: str, outpath: str, pwd: str | None = None):

        c = self.checkzip(url)
        if c == "null":
            return
        if c == "7z":
            try:
                with py7zr.SevenZipFile(url, 'r', password=pwd) as f:

                    self.extract(
                        None,   # type: ignore
                        outpath, c, sevenZlist=f.getnames(), sevenZ=f)
                    if self.finalcb:
                        self.finalcb("")
            except LZMAError as err:
                if self.wrongpwcb and format(err) == "Corrupt input data":
                    self.wrongpwcb(format(err))

        if c == "zip":
            try:
                with zipfile.ZipFile(url, "r") as f:
                    if pwd:
                        f.pwd = pwd.encode()
                    self.extract(f, outpath,  c)
                    if self.finalcb:
                        self.finalcb("")
            except RuntimeError as err:
                if self.wrongpwcb and "Bad password" in format(err):
                    self.wrongpwcb(format(err))
            pass
        if c == 'rar':
            try:
                with rarfile.RarFile(url, "r", pwd=pwd) as f:
                    self.extract(f, outpath,  c)
                if self.finalcb:
                    self.finalcb("")
            except RuntimeError as err:
                if self.wrongpwcb and format(err) == "Bad password for Archive":
                    self.wrongpwcb(format(err))


class JZipUI(JCommonUI):
    '''压缩包'''

    __zip = JZip()

    def set_cacheOutput(self, dir: str):
        self.__zip.cacheOutput = dir

    def ab_final_event(self, d):
        t: jcmd_final_type = d[0]
        s: str = d[1]
        m: junzip_type = d[2]
        if t == "success":
            if m == "unzip":
                self.ui_unzip_program.progress_settext(
                    f'解压完成,共解压了{self.ui_unzip_program.progress_currentcount}个文件')
            elif m == "getMsg":
                self.ui_unzip_program.progress_allcount = int(s)
                pass
        elif t == "pwwrong":
            print("密码错误")
            self.cancel()
            nextpw = self.get_nextpw()
            if nextpw == "":
                self.ui_unzip_program.progress_settext("密码错误!,无法解压")
                if self.unzip_cb:
                    self.unzip_cb("pwwrong", self.pw)
            else:
                self.ui_unzip_program.progress_settext(f'密码错误!,尝试"{nextpw}"')
                self.used_pwlist.append(nextpw)
                self.pw = nextpw
                time.sleep(1)
                print(f'开始尝试新密码:{nextpw}')
                self.start()
        pass

    def ab_unzip_msg_event(self, d):

        super().ab_unzip_msg_event(d)

        t: jcmd_final_type = d[0]
        s: str = d[1]
        m: junzip_type = d[2]
        self.ui_unzip_program.msg_add(s)
        self.ui_unzip_program.progress_add()

    def ab_reset_cmddata(self):

        super().ab_reset_cmddata()

    def ab_cancel(self):

        super().ab_cancel()

    def ab_get_zipmsg(self):

        pass

    def ab_unzip(self):

        self.finalType = "success"
        self.finalMsg = ""
        self.unzip_type = "unzip"

        def listcb(l):
            type: junzip_type = "getMsg"
            self.finalSingal.emit((self.finalType, str(l), type))
            pass

        def msgcb(s):
            self.outputSingal.emit((self.finalType, s, self.unzip_type))
            pass

        def wrongpwcb(s):
            self.finalType = 'pwwrong'
            self.finalMsg = s
            self.finalSingal.emit(
                (self.finalType, self.finalMsg, self.unzip_type))
            pass

        def finalcb(s):
            self.finalSingal.emit(
                (self.finalType, s, self.unzip_type))
            if self.unzip_cb:
                self.unzip_cb(self.finalType, self.pw)
            pass

        self.__zip.listcb = listcb
        self.__zip.msgcb = msgcb
        self.__zip.wrongpwcb = wrongpwcb
        self.__zip.finalcb = finalcb
        self.__zip.overwrite = self.overwrite_type
        self.__zip.unzip(self.inputfile, self.outputdir, self.pw or None)
        pass

    def ab_run(self):

        super().ab_run()

        self.ab_unzip()
        pass
