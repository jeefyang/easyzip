
from PyQt6.QtCore import Qt
from Ui_main import Ui_MainWindow
import sys
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QListView, QAbstractItemView, QTreeView, QApplication, QDialog, QPushButton, QMessageBox, QWidget,QTextEdit,QLineEdit
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class Ui_Update(QMainWindow,Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.edit_input_zip_list.setAcceptDrops(True)
        self.edit_output_dir.setAcceptDrops(True)
        self.edit_config_url.setAcceptDrops(True)
        self.edit_log_url.setAcceptDrops(True)
        self.edit_zip_url.setAcceptDrops(True)
        self.__set_lineedit_drag(self.edit_output_dir)
        self.__set_lineedit_drag(self.edit_zip_url)
        self.__set_lineedit_drag(self.edit_log_url)
        self.__set_lineedit_drag(self.edit_config_url)
        # self.combo_default_select_exe

    @property
    def val_input_zip_list(self):
        '''压缩包路径'''
        return self.edit_input_zip_list.toPlainText()

    @val_input_zip_list.setter
    def val_input_zip_list(self, v: str):
        self.edit_input_zip_list.setText(v)

    @property
    def val_output_dir(self):
        '''解压路径'''
        return self.edit_output_dir.text()

    @val_output_dir.setter
    def val_output_dir(self, v: str):
        self.edit_output_dir.setText(v)

    @property
    def val_config_url(self):
        '''配置文件路径'''
        return self.edit_config_url.text()

    @val_config_url.setter
    def val_config_url(self, v: str):
        self.edit_config_url.setText(v)

    @property
    def val_log_url(self):
        '''日志输出路径'''
        return self.edit_log_url.text()

    @val_log_url.setter
    def val_log_url(self, v: str):
        self.edit_log_url.setText(v)

    @property
    def val_zip_url(self):
        '''7z压缩程序文件夹路径'''
        return self.edit_zip_url.text()

    @val_zip_url.setter
    def val_zip_url(self, v: str):
        self.edit_zip_url.setText(v)

    @property
    def is_autosave(self):
        '''是否自动保存'''
        return self.check_autosave.isChecked()

    @is_autosave.setter
    def is_autosave(self, v: bool):
        self.check_autosave.setChecked(v)

    @property
    def is_loop_unzip(self):
        '''是否解压嵌套压缩包'''
        return self.check_loop_unzip.isChecked()

    @is_loop_unzip.setter
    def is_loop_unzip(self, v: bool):
        self.check_loop_unzip.setChecked(v)

    @property
    def is_unzip_self(self):
        '''是否自解压'''
        return self.check_unzip_self.isChecked()

    @is_unzip_self.setter
    def is_unzip_self(self, v: bool):
        self.check_unzip_self.setChecked(v)

    @property
    def is_unzip_del(self):
        '''是否解压后删除源软件'''
        return self.check_unzip_del.isChecked()

    @is_unzip_del.setter
    def is_unzip_del(self, v: bool):
        self.check_unzip_del.setChecked(v)

    @property
    def is_single_zip(self):
        '''是否单压缩包'''
        return self.check_single_zip.isChecked()

    @is_single_zip.setter
    def is_single_zip(self, v: bool):
        self.check_single_zip.setChecked(v)

    @property
    def is_try_pw(self):
        '''是否尝试密码'''
        return self.check_try_pw.isChecked()

    @is_try_pw.setter
    def is_try_pw(self, v: bool):
        self.check_try_pw.setChecked(v)

    @property
    def is_default_autosave(self):
        '''是否默认自动保存'''
        return self.check_default_autosave.isChecked()

    @is_default_autosave.setter
    def is_default_autosave(self, v: bool):
        self.check_default_autosave.setChecked(v)

    @property
    def is_default_loop_unzip(self):
        '''是否默认解压嵌套压缩包'''
        return self.check_default_loop_unzip.isChecked()

    @is_default_loop_unzip.setter
    def is_default_loop_unzip(self, v: bool):
        self.check_default_loop_unzip.setChecked(v)

    @property
    def is_default_unzip_self(self):
        '''是否默认自解压'''
        return self.check_default_unzip_self.isChecked()

    @is_default_unzip_self.setter
    def is_default_unzip_self(self, v: bool):
        self.check_default_unzip_self.setChecked(v)

    @property
    def is_default_unzip_del(self):
        '''是否默认解压后删除源软件'''
        return self.check_default_unzip_del.isChecked()

    @is_default_unzip_del.setter
    def is_default_unzip_del(self, v: bool):
        self.check_default_unzip_del.setChecked(v)

    @property
    def is_default_single_zip(self):
        '''是否默认单压缩包'''
        return self.check_default_single_zip.isChecked()

    @is_default_single_zip.setter
    def is_default_single_zip(self, v: bool):
        self.check_default_single_zip.setChecked(v)

    @property
    def is_default_try_pw(self):
        '''是否默认尝试密码'''
        return self.check_default_try_pw.isChecked()

    @is_default_try_pw.setter
    def is_default_try_pw(self, v: bool):
        self.check_default_try_pw.setChecked(v)



    def __set_lineedit_drag(self,o:QLineEdit):
        '''设置输入框的拖放事件'''
        def dragenterevent(a0:QDragEnterEvent | None):
            assert a0 is not None
            minedata = a0.mimeData()
            assert minedata is not None
            if minedata.hasUrls() or minedata.hasText():
                a0.accept()
            else:
                a0.ignore()
            pass

        def dropevent(a0: QDropEvent | None):
            assert a0 is not None
            minedata = a0.mimeData()
            assert minedata is not None
            if minedata.hasUrls():
                for url in minedata.urls():
                    o.setText(url.toLocalFile())
                    
            elif minedata.hasText():
                o.setText(minedata.text())
        
        o.dragEnterEvent=dragenterevent
        o.dropEvent=dropevent