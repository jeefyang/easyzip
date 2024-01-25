
from PyQt6.QtCore import Qt
from Ui_main import Ui_MainWindow
import sys
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QListView, QAbstractItemView, QTreeView, QApplication, QDialog, QPushButton, QMessageBox, QWidget, QTextEdit, QLineEdit
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from typing import Literal

sort_pw_type = Literal['次数', '名称', '日期']
main_exe_type = Literal["命令行", "图形GUI"]
overwrite_type = Literal["直接覆盖", "跳过不覆盖", "重命名新文件", "重命名旧文件"]


class Ui_Update(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.edit_input_zip_list.setAcceptDrops(True)
        self.edit_output_dir.setAcceptDrops(True)
        self.edit_zip_url.setAcceptDrops(True)
        self.tab_main.setAcceptDrops(True)
        self.setAcceptDrops(True)
        # 拖放事件
        self.__set_mainwin_drag()
        self.__set_edit_zip_list_drag()
        self.__set_lineedit_drag(self.edit_output_dir)
        self.__set_lineedit_drag(self.edit_zip_url)
        # 读取按钮事件
        # self.__read_multifile_event(
        #     self.btn_input_list, self.edit_input_zip_list)
        self.load_input_list_event()
        self.__read_folder_event(self.btn_output, self.edit_output_dir)
        self.__read_folder_event(self.btn_zip_url, self.edit_zip_url)
        self.check_unzip_self.clicked.connect(self.unzip_self_event)

        # self.combo_default_select_exe

    def unzip_self_event(self):
        '''自解压事件'''
        self.edit_output_dir.setDisabled(self.is_unzip_self)
        self.btn_output.setDisabled(self.is_unzip_self)

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
    def val_zip_url(self):
        '''7z压缩程序文件夹路径'''
        return self.edit_zip_url.text()

    @val_zip_url.setter
    def val_zip_url(self, v: str):
        self.edit_zip_url.setText(v)

    @property
    def is_autosave_pw(self):
        '''是否自动保存'''
        return self.check_autosave_pw.isChecked()

    @is_autosave_pw.setter
    def is_autosave_pw(self, v: bool):
        self.check_autosave_pw.setChecked(v)

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
    def is_autounzip(self):
        '''是否自动解压'''
        return self.check_autounzip.isChecked()

    @is_autounzip.setter
    def is_autounzip(self, v: bool):
        self.check_autounzip.setChecked(v)

    @property
    def is_autoexit(self):
        '''是否完成后自动退出'''
        return self.check_autoexit.isChecked()

    @is_autoexit.setter
    def is_autoexit(self, v: bool):
        self.check_autoexit.setChecked(v)

    @property
    def is_shutdown(self):
        '''是否完成后自动关机'''
        return self.check_shutdown.isChecked()

    @is_shutdown.setter
    def is_shutdown(self, v: bool):
        self.check_shutdown.setChecked(v)

    @property
    def select_pw(self) -> str:
        '''当前选中的密码'''
        return self.combo_pw.currentText()

    @select_pw.setter
    def select_pw(self, v: str):
        self.combo_pw.setCurrentText(v)

    @property
    def select_sort_pw(self) -> sort_pw_type:
        '''密码排序选择'''
        return self.combo_sort_pw.currentText()  # type:ignore

    @select_sort_pw.setter
    def select_sort_pw(self, v: sort_pw_type):
        self.combo_sort_pw.setCurrentText(v)

    @property
    def select_main_exe(self) -> main_exe_type:
        '''执行程序选择'''
        return self.combo_main_exe.currentText()  # type:ignore

    @select_main_exe.setter
    def select_main_exe(self, v: main_exe_type):
        self.combo_main_exe.setCurrentText(v)

    @property
    def select_overwrite(self) -> overwrite_type:
        '''覆盖模式选择'''
        return self.combo_overwrite.currentText()  # type:ignore

    @select_overwrite.setter
    def select_overwrite(self, v: overwrite_type):
        self.combo_overwrite.setCurrentText(v)

    @property
    def select_encoding(self):
        '''编码选择'''
        return self.combo_encoding.currentText()

    @select_encoding.setter
    def select_encoding(self, v: str):
        self.combo_encoding.setCurrentText(v)

    @property
    def is_default_autosave_pw(self):
        '''是否默认自动保存'''
        return self.check_default_autosave_pw.isChecked()

    @is_default_autosave_pw.setter
    def is_default_autosave_pw(self, v: bool):
        self.check_default_autosave_pw.setChecked(v)

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

    @property
    def is_default_autounzip(self):
        '''是否默认自动解压'''
        return self.check_default_autounzip.isChecked()

    @is_default_autounzip.setter
    def is_default_autounzip(self, v: bool):
        self.check_default_autounzip.setChecked(v)

    @property
    def is_default_autoexit(self):
        '''是否默认完成后自动退出'''
        return self.check_default_autoexit.isChecked()

    @is_default_autoexit.setter
    def is_default_autoexit(self, v: bool):
        self.check_default_autoexit.setChecked(v)

    @property
    def select_default_sort_pw(self):
        '''默认密码排序选择'''
        return self.combo_default_sort_pw.currentText()

    @select_default_sort_pw.setter
    def select_default_sort_pw(self, v: Literal['次数', '名称', '日期']):
        self.combo_default_sort_pw.setCurrentText(v)

    @property
    def select_default_main_exe(self) -> main_exe_type:
        '''默认执行程序选择'''
        return self.combo_default_main_exe.currentText()  # type:ignore

    @select_default_main_exe.setter
    def select_default_main_exe(self, v: main_exe_type):
        self.combo_default_main_exe.setCurrentText(v)

    @property
    def select_default_overwrite(self) -> overwrite_type:
        '''覆盖模式选择'''
        return self.combo_default_overwrite.currentText()  # type:ignore

    @select_default_overwrite.setter
    def select_default_overwrite(self, v: overwrite_type):
        self.combo_default_overwrite.setCurrentText(v)

    def __set_lineedit_drag(self, o: QLineEdit):
        '''设置输入框的拖放事件'''
        def dragenterevent(a0: QDragEnterEvent | None):
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

        o.dragEnterEvent = dragenterevent
        o.dropEvent = dropevent

    def __set_edit_zip_list_drag(self):
        '''压缩包路径拖放事件'''
        def dragenterevent(e: QDragEnterEvent | None):
            assert e is not None
            minedata = e.mimeData()
            assert minedata is not None
            if minedata.hasUrls() or minedata.hasText():
                e.accept()
            else:
                e.ignore()

        def dropevent(e: QDropEvent | None) -> None:
            assert e is not None
            minedata = e.mimeData()
            assert minedata is not None
            if minedata.hasUrls():
                for url in minedata.urls():
                    str = url.toLocalFile()
                    self.__add_inputurl(str)
            elif minedata.hasText():
                str = minedata.text()
                self.__add_inputurl(str)
        self.edit_input_zip_list.dragEnterEvent = dragenterevent
        self.edit_input_zip_list.dropEvent = dropevent
        pass

    def __add_inputurl(self, s: str):
        '''添加输入路径'''
        if self.is_single_zip == True:
            self.edit_input_zip_list.setText(s)
        else:
            self.edit_input_zip_list.append(s)

    def __set_mainwin_drag(self):
        '''设置主面板拖放'''
        def dragenterevent(a0: QDragEnterEvent | None):
            assert a0 is not None
            minedata = a0.mimeData()
            assert minedata is not None
            if minedata.hasUrls() or minedata.hasText():
                a0.accept()
            else:
                a0.ignore()

        def dropevent(a0: QDropEvent | None) -> None:
            assert a0 is not None
            minedata = a0.mimeData()
            assert minedata is not None
            if minedata.hasUrls():
                for url in minedata.urls():
                    str = url.toLocalFile()
                    self.__add_inputurl(str)
            elif minedata.hasText():
                str = minedata.text()
                self.__add_inputurl(str)
        self.tab_main.dragEnterEvent = dragenterevent
        self.tab_main.dropEvent = dropevent
        self.dragEnterEvent = dragenterevent
        self.dropEvent = dropevent
        pass

    def __read_folder_event(self, btn: QPushButton, line: QLineEdit):
        '''读取文件夹事件'''
        def click():
            url = QFileDialog.getExistingDirectory(self, "选取文件夹")
            line.setText(url)
        btn.clicked.connect(click)
        pass

    def __read_multifile_event(self, btn: QPushButton, text: QTextEdit):
        '''多文件读取事件'''
        def click():
            urls = QFileDialog.getOpenFileNames(self, "选取多个文件")[0]
            for url in urls:
                text.append(str(url))
                pass
            pass
        btn.clicked.connect(click)
        pass

    def load_input_list_event(self):
        '''输入压缩包载入事件'''
        def click():
            if self.is_single_zip == True:
                url = QFileDialog.getOpenFileName(self, "选取单个文件")[0]
                self.val_input_zip_list = url
            else:
                urls = QFileDialog.getOpenFileNames(self, "选取多个文件")[0]
                for url in urls:
                    self.edit_input_zip_list.append(str(url))
        self.btn_input_list.clicked.connect(click)

    def show_dialog(self, type: Literal["warn", "info", "error"], v: str):
        '''弹框提示-'''
        if type == "warn":
            QMessageBox.warning(None, "警告", v)
        elif type == "info":
            QMessageBox.information(None, "提示", v)
        elif type == "error":
            QMessageBox.critical(None, "错误", v)
        pass
