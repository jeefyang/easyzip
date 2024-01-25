from tool import QJson
from Ui_update import sort_pw_type, main_exe_type, overwrite_type


class EasyUnzipConfig(QJson):
    def __init__(self) -> None:
        super()
        self.val_zip_url: str = "C:/Program Files/7-Zip"
        '''7z程序的路径'''
        self.is_default_unzip_del: bool = False
        '''是否默认解压后删除'''
        self.is_default_loop_unzip: bool = False
        '''是否默认递归解压'''
        self.is_default_single_zip: bool = False
        '''是否默认单个解压文件'''
        self.is_default_autosave_pw: bool = False
        '''是否默认保存密码'''
        self.is_default_try_pw: bool = False
        '''是否默认尝试密码'''
        self.is_default_autounzip: bool = False
        '''是否默认自动解压文件'''
        self.is_default_autoexit: bool = False
        '''是否默认解压完不出错,自动退出程序'''
        self.select_default_sort_pw: sort_pw_type = "次数"
        ''''默认密码排序选择'''
        self.select_default_main_exe: main_exe_type = "命令行"
        '''默认执行程序选择'''
        self.select_default_overwrite: overwrite_type = "直接覆盖"
        pass
