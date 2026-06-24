# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_progress.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)
from PySide6.QtCore import Qt, QPoint, QThread, Signal

class Ui_Dialog_Progress(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 91)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(Dialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u6570\u636e\u52a0\u8f7d\u4e2d\uff0c\u8bf7\u7b49\u5f85 . . .", None))
    # retranslateUi

class DataLoadingThread(QThread):
    # 定义信号来传递进度
    progress_signal = Signal(int)
    finished_signal = Signal()

    def __init__(self, load_function):
        super().__init__()
        self.load_function = load_function  # 实际的加载任务函数

    def run(self):
        """        在这里执行数据加载的任务，并将进度通过信号发送给主线程        """
        self.load_function()
        # 完成后发送信号
        self.finished_signal.emit()

class DataLoaderWithProgress(QDialog):
    def __init__(self, parent, load_function, show_plotter_function):
        super().__init__(parent)
        self.load_function = load_function
        self.show_plotter = show_plotter_function

        # 设置弹窗 UI
        self.progress_ui = Ui_Dialog_Progress()
        self.progress_ui.setupUi(self)

        # 设置进度条为 indeterminate 模式
        self.progress_ui.progressBar.setRange(0, 0)
        self.setWindowModality(Qt.WindowModal)

        # 启动数据加载线程
        self.loading_thread = DataLoadingThread(self.load_function)
        self.loading_thread.progress_signal.connect(self.update_progress)
        self.loading_thread.finished_signal.connect(self.close_dialog)  # 数据加载完成时关闭弹窗

        # 显示弹窗
        self.show()

        # 启动线程
        self.loading_thread.start()

    def update_progress(self, value):
        # 更新进度条
        self.progress_ui.progressBar.setValue(value)

    def close_dialog(self):
        """关闭弹窗"""
        self.accept()  # 或者 dialog.reject()
        self.show_plotter()

