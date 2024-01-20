
import sys
from PyQt6.QtWidgets import QApplication
from Ui_update import Ui_Update
import os


class MyMainWin(Ui_Update):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        if self.__is_config_completed() == False:
            self.__auto_completion_url()
        pass
        # self.setupUi(self)

    def __is_config_completed(self):
        '''检测配置是否完整'''
        if self.val_config_url == "" or self.val_config_url == None:
            return False
        if self.val_log_url == "" or self.val_log_url == None:
            return False
        if self.val_zip_url == "" or self.val_zip_url == None or os.path.exists(self.val_zip_url) == False:
            return False
        return True

    def __auto_completion_url(self):
        '''自动补全链接'''
        if self.val_config_url == "" or self.val_config_url == None:
            self.val_config_url = "./op"
        if self.val_log_url == "" or self.val_log_url == None:
            self.val_log_url = './log'
        if self.val_zip_url == "" or self.val_zip_url == None or os.path.exists(self.val_zip_url) == False:
            self.val_zip_url = "C:/Program Files/7-Zip"
        pass

    def __init_log(self):
        '''日志初始化'''
        if self.val_log_url == "" or self.val_log_url == None:
            return
        pass
    # def

    def __init_config(self):
        '''配置初始化'''
        if self.val_config_url == "" or self.val_config_url == None:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mywin = MyMainWin()
    mywin.show()
    sys.exit(app.exec())
    pass
