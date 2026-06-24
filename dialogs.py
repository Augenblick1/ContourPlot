# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QMessageBox, QSizePolicy, QPushButton, QCheckBox, QDialogButtonBox, QGridLayout, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, \
    QDialog

from ui.dialog_ui import Ui_Dialog

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QTableWidget,
    QTableWidgetItem, QWidget)


class DataViewDialog(QDialog):
    def __init__(self, data, title, parent=None):
        super(DataViewDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        self.table = self.ui.tableWidget
        if self.table is not None:
            self.populate_table(data)
            self.adjust_table_size()
        else:
            QMessageBox.critical(self, "Error", "Failed to find tableWidget in UI!")

    def populate_table(self, data):
        # 设置表格行列数
        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setHorizontalHeaderLabels(data.columns)

        # 填充表格数据
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QTableWidgetItem(str(data.iat[i, j]))
                self.table.setItem(i, j, item)

    def adjust_table_size(self):
        # 调整表格大小以适应内容
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

class DataSelectionDialog(QDialog):
    def __init__(self, files, parent=None):
        super(DataSelectionDialog, self).__init__(parent)
        self.setWindowTitle("选择匹配的数据")
        self.resize(300, 200)

        # 创建一个主布局
        main_layout = QVBoxLayout(self)

        # 创建一个网格布局，用于放置标签和复选框
        grid_layout = QGridLayout(self)

        # 添加表头
        header_label_1 = QLabel("文件")
        header_label_1.setMaximumHeight(30)  # 设置最大高度，防止表头行过宽
        header_label_1.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)  # 限制拉伸

        header_label_2 = QLabel("速度数据")
        header_label_2.setMaximumHeight(30)  # 设置最大高度，防止表头行过宽
        header_label_2.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        header_label_3 = QLabel("剖面信息")
        header_label_3.setMaximumHeight(30)  # 设置最大高度，防止表头行过宽
        header_label_3.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        grid_layout.addWidget(header_label_1, 0, 0, Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(header_label_2, 0, 1, Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(header_label_3, 0, 2, Qt.AlignmentFlag.AlignHCenter)

        self.file_checkboxes = []

        # 动态生成label和checkbox
        for i, file in enumerate(files):
            label = QLabel(file)
            speed_checkbox = QCheckBox()
            profile_checkbox = QCheckBox()

            grid_layout.addWidget(label, i + 1, 0, Qt.AlignmentFlag.AlignHCenter)
            grid_layout.addWidget(speed_checkbox, i + 1, 1, Qt.AlignmentFlag.AlignHCenter)
            grid_layout.addWidget(profile_checkbox, i + 1, 2, Qt.AlignmentFlag.AlignHCenter)

            self.file_checkboxes.append((file, speed_checkbox, profile_checkbox))

        # 调整每行的高度比例，使它们占用相同的高度比例
        total_rows = len(files) + 1  # 表头行 + 文件行
        for i in range(total_rows):
            grid_layout.setRowStretch(i, 1)  # 为每一行设置相同的拉伸因子

        # 将网格布局添加到主布局中
        main_layout.addLayout(grid_layout)

        # 创建确定和取消按钮并设置为中文
        button_box = QDialogButtonBox()
        btn_ok = QPushButton("确定")
        btn_cancel = QPushButton("取消")
        button_box.addButton(btn_ok, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(btn_cancel, QDialogButtonBox.ButtonRole.RejectRole)

        # 连接按钮的点击事件
        btn_ok.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)

        # 将按钮添加到主布局中
        main_layout.addWidget(button_box)


    def get_selected_files(self):
        selected_files = []
        for file, speed_checkbox, profile_checkbox in self.file_checkboxes:
            if speed_checkbox.isChecked() or profile_checkbox.isChecked():
                selected_files.append((file, speed_checkbox.isChecked(), profile_checkbox.isChecked()))
        return selected_files


class show_both_data_ui(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(824, 640)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 640))
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy1)
        self.tableWidget.setMinimumSize(QSize(400, 0))

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.tableWidget)

        self.tableWidget_2 = QTableWidget(Dialog)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy1.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy1)
        self.tableWidget_2.setMinimumSize(QSize(400, 0))

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.tableWidget_2)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")  # 修改"确定"按钮文本
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")  # 修改"取消"按钮文本

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.buttonBox)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u539f\u59cb\u6570\u636e", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5256\u9762\u4fe1\u606f", None))
    # retranslateUi

class show_both_data(QDialog):
    def __init__(self, speed_data, profile_data, parent=None):
        super(show_both_data, self).__init__(parent)
        self.ui = show_both_data_ui()
        self.ui.setupUi(self)

        self.table = self.ui.tableWidget
        if self.table is not None:
            self.populate_table(speed_data)
            self.adjust_table_size()
        else:
            QMessageBox.critical(self, "Error", "Failed to find tableWidget in UI!")

        self.table = self.ui.tableWidget_2
        if self.table is not None:
            self.populate_table(profile_data)
            self.adjust_table_size()
        else:
            QMessageBox.critical(self, "Error", "Failed to find tableWidget in UI!")

    def populate_table(self, data):
        # 设置表格行列数
        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setHorizontalHeaderLabels(data.columns)

        # 填充表格数据
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QTableWidgetItem(str(data.iat[i, j]))
                self.table.setItem(i, j, item)

    def adjust_table_size(self):
        # 调整表格大小以适应内容
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

class Show_one_table(QDialog):
    def __init__(self, data, title, parent=None):
        super(Show_one_table, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle(title)

        layout = self.ui.verticalLayout

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # 修改按钮文本为中文
        self.buttonBox.button(QDialogButtonBox.Ok).setText("确定")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("取消")

        # 连接按钮信号
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)

        self.table = self.ui.tableWidget
        if self.table is not None:
            self.populate_table(data)
            self.adjust_table_size()
        else:
            QMessageBox.critical(self, "Error", "Failed to find tableWidget in UI!")

    def populate_table(self, data):
        # 设置表格行列数
        self.table.setRowCount(data.shape[0])
        self.table.setColumnCount(data.shape[1])
        self.table.setHorizontalHeaderLabels(data.columns)

        # 填充表格数据
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                item = QTableWidgetItem(str(data.iat[i, j]))
                self.table.setItem(i, j, item)

    def adjust_table_size(self):
        # 调整表格大小以适应内容
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
