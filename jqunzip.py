from jcommonUI import JCommonUI, junzip_type
import re
from tool import jindexof, jcmd_final_type
import time
import subprocess


class JQUnzip(JCommonUI):

    def __init__(self) -> None:
        super().__init__()
        self.exe: str = ""
        '''当前的程序'''
        pass

    def ab_final_event(self, d):

        super().ab_final_event(d)
        t: jcmd_final_type = d[0]
        s: str = d[1]
        m: junzip_type = d[2]
        if (t == "success"):
            if m == "unzip":
                print("解压成功")
                if self.unzip_cb:
                    self.unzip_cb(t,self.pw)
            elif m == "getMsg":
                a = re.split(r"\s+", s)
                # self.is_check_msg = True
                print(a)
                # self.files_count = int(a[4])
                # self.folders_count = int(a[6])
                # self.ui_unzip_program.progress_allcount = self.files_count

        elif (t == "cancel"):
            print("强行退出解压操作")

        elif (t == "error"):
            print(d[1])

        pass

    def ab_unzip_msg_event(self, d):

        super().ab_unzip_msg_event(d)
        t: jcmd_final_type = d[0]
        s: str = d[1]
        m: junzip_type = d[2]
        self.ui_unzip_program.msg_add(s)
        if m == "unzip" and re.search(r'^-\s', s, re.M | re.I) and not re.search(r'\\$', s, re.M | re.I):
            self.ui_unzip_program.progress_add()
        elif m == "unzip" and re.search(r'^Everything is Ok', s):
            self.ui_unzip_program.progress_settext(
                f'解压完成,共解压了{self.ui_unzip_program.progress_currentcount}个文件')
            self.cancel()
            pass
        elif re.search(r'Cannot open encrypted archive\. Wrong password\?', s) or re.match(r'^ERROR: Wrong password', s) or re.search("Errors: 1", s):
            print("密码错误")
            self.finalType = "error"
            self.cancel()
            nextpw = self.get_nextpw()
            if nextpw == "":
                self.ui_unzip_program.progress_settext("密码错误!,无法解压")
            else:
                self.ui_unzip_program.progress_settext(f'密码错误!,尝试"{nextpw}"')
                self.used_pwlist.append(nextpw)
                self.pw = nextpw
                time.sleep(5)
                print(f'开始尝试新密码:{nextpw}')
                self.start()
            pass
        # print(d[1])
        pass

    def ab_reset_cmddata(self):
        ''' 继承用的'''
        super().ab_reset_cmddata()
        pass

    def ab_cancel(self):

        super().ab_cancel()

    def ab_get_zipmsg(self):
        '''获取压缩包信息'''

        # super().ab_get_zipmsg()
        # 选择程序
        cmd = self.exe+" "
        # 解压标志
        cmd += 'l '
        # 需要解压的压缩文件
        cmd += f'"{self.inputfile}" '
        # 输入密码
        if self.pw and self.pw != "":
            cmd += f'-p"{self.pw}" '
        # 添加日志
        cmd += '-bb3 '
        # 改写输出的字符串编码
        # cmd += ' -sccUTF-8'
        # 改写文件编码
        if self.encoding and self.encoding != "":
            cmd += f'-mcp={self.encoding}'
        print(cmd)
        self.finalType = 'success'
        self.finalMsg = ""
        self.unzip_type = "getMsg"
        with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, text=True) as p:
            while self.finalType == "success":
                try:
                    if p.stderr != None:
                        print("xx")
                        error_output = p.stderr.readline()
                        if error_output:
                            error_output = error_output.strip()
                            print(error_output)
                            self.outputSingal.emit(
                                ("error", error_output, self.unzip_type))
                            continue
                    if p.poll() or not p.stdout:
                        break
                    output = p.stdout.readline()
                    if output:
                        output = output.strip()
                        print(self.finalType, output)
                        self.outputSingal.emit(
                            (self.finalType, output, self.unzip_type))
                        if output:
                            self.finalMsg = output
                    else:
                        break
                    pass
                except:
                    self.finalType = 'error'
                    self.finalMsg = "读取压缩包错误"
                    print("遇到错误")
                    break
            self.finalSingal.emit(
                (self.finalType, self.finalMsg, self.unzip_type))

    def ab_unzip(self):
        '''解压'''

        super().ab_unzip()
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
        match self.overwrite_type:
            case "直接覆盖":
                cmd += '-aoa '
            case "跳过不覆盖":
                cmd += '-aos '
            case "重命名新文件":
                cmd += '-aou '
            case "重命名旧文件":
                cmd += '-aot '

        # 添加日志
        cmd += '-bb3'
        # 改写输出的字符串编码
        # cmd += ' -sccUTF-8'
        # 改写文件编码
        if self.encoding and self.encoding != "":
            cmd += f' -mcp={self.encoding}'
        print(cmd)
        self.ui_unzip_program.progress_currentcount = 0
        self.finalType = "success"
        self.finalMsg = ""
        self.unzip_type = "unzip"
        with subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, text=True) as p:
            while self.finalType == "success":
                try:
                    if p.stderr != None:
                        error_output = p.stderr.readline()
                        if error_output:
                            error_output = error_output.strip()
                            self.outputSingal.emit(
                                ("error", error_output, self.unzip_type))
                            continue
                    if p.poll() or not p.stdout:
                        break
                    output = p.stdout.readline()
                    if output:
                        output = output.strip()
                        self.outputSingal.emit(
                            (self.finalType, output, self.unzip_type))
                    else:
                        break
                    pass
                    # time.sleep(0.02)
                except:
                    self.finalType = 'error'
                    self.finalMsg = "解压时遇错误"
                    break
            self.finalSingal.emit(
                (self.finalType, self.finalMsg, self.unzip_type))

    def ab_run(self):

        super().ab_run()
        time.sleep(2)
        # if self.is_check_msg == False:
        #     print("检测压缩包")
        #     self.ui_unzip_program.progress_allcount = 0
        #     self.__get_zipmsg()
        self.ab_unzip()
