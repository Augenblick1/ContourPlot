import json
import subprocess
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyvista as pv
from PySide6.QtCore import Qt, QPoint, QThread, Signal
from PySide6.QtGui import QAction, QPainter, QPen, QFont, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow, QPushButton, QMenu, QComboBox, QGridLayout, \
    QFileDialog, QTableWidget, QTableWidgetItem, \
    QListWidgetItem, QDialog
from PySide6.QtWidgets import QLabel
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from matplotlib.tri import Triangulation, LinearTriInterpolator
from pyvistaqt import QtInteractor
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from scipy.spatial import Delaunay
from scipy.spatial import distance
from sklearn.linear_model import LinearRegression
from adjustText import adjust_text
from matplotlib.patches import Rectangle
from scipy.spatial import ConvexHull

from ui.main_ui import Ui_MainWindow
from dialogs import *
from data_loading import *

plt.rcParams['font.family'] = 'SimHei'
matplotlib.rcParams['axes.unicode_minus'] = False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化存储数据的字典
        self.loaded_data = {}

        # 连接 actionImport 的触发信号到 import_file 方法
        self.ui.actionImport.triggered.connect(self.import_file)

        #
        self.ui.actionExport_figures.triggered.connect(self.export_figures)

        # 显示侧边栏
        self.ui.actionShowdock.triggered.connect(self.show_dock)

        # 连接双击事件
        self.ui.listWidget.itemDoubleClicked.connect(self.show_data)  # 直接使用 ui 中定义的对象

        # 连接右键事件
        self.ui.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget.customContextMenuRequested.connect(self.show_context_menu)

        self.ui.listWidget_2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.listWidget_2.customContextMenuRequested.connect(self.show_context_menu_1)

        # 连接键盘事件
        self.ui.listWidget.keyPressEvent = self.listWidget_key_press_event

        # 绘制等值线图
        self.ui.actionContour.triggered.connect(self.plot_speed_contour)

        self.processed_data = {}

        # 初始化 project_data
        self.project_data = {}  # 确保 project_data 在保存和打开项目时存在

        self.filtered_data = {}

        self.displayed_slices = []

        self.slice_actor = {}
        self.all_q_cylinder = {}
        self.all_baserock_cylinder = {}
        self.all_well_name = {}

        self.ui.listWidget_2.itemDoubleClicked.connect(self.show_processed_data)  # 直接使用 ui 中定义的对象

        self.ui.pushButton.clicked.connect(self.processed_data_export_to_csv)

        self.ui.pushButton_2.clicked.connect(self.filtered_data_export_to_csv)

        self.ui.actionborehole.triggered.connect(self.plot_well_state)
        self.ui.actionSave.triggered.connect(self.save_project)
        self.ui.actionOpen.triggered.connect(self.open_project)
        self.ui.actionCreat_New.triggered.connect(self.new_project)


        # self.ui.action3DPlot.triggered.connect(self.Data_loading_3D)
        self.ui.action3DPlot.triggered.connect(self.show_one_table)

        # self.ui.action3DPlot.triggered.connect(self.plot_3D)

        self.ui.action3DPlot.triggered.connect(self.switch_to_tab_2)

        self.coef = None
        self.intercept = None
        self.first_point = None
        self.last_point = None

        self.speed_data = None
        self.profile_data = None

        self.speed_data_1 = None

        self.grid = None

        self.colors_en = 'jet'

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.plotter = QtInteractor()

        self.is_saved = True

        self.connect_ui_elements()

        # 创建一个隐藏的NavigationToolbar2QT用于功能调用
        self.canvas.toolbar = NavigationToolbar2QT(self.canvas, None)
        self.canvas.toolbar.hide()

        # 设置底部工具栏
        self.setup_bottom_toolbar()

        # 连接窗口大小变化信号
        self.ui.widget_3.resizeEvent = self.on_widget_3_resize

        # 创建比例尺标签
        self.scale_bar_label = QLabel(self.ui.widget_3)
        self.scale_bar_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.scale_bar_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.scale_bar_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 255, 0.8);
                padding: 5px;
                border: 1px solid #999;
                border-radius: 3px;
            }
        """)

        # 设置窗口标志，确保始终在顶层
        self.scale_bar_label.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 初始位置设置
        self.scale_bar_label.setGeometry(20, self.ui.tab_4.height() - 60, 200, 40)
        self.scale_bar_label.show()

        self.ui.tabWidget_2.currentChanged.connect(self.toggle_tabs)
        self.ui.tabWidget_2.currentChanged.connect(self.sync_tabs)
        self.ui.tabWidget.tabBar().hide()

        self.ui.btn_home_view.clicked.connect(lambda: self.reset_view('iso'))
        self.ui.btn_front_veiw.clicked.connect(lambda: self.reset_view('yz'))
        self.ui.btn_left_veiw.clicked.connect(lambda: self.reset_view('xz'))
        self.ui.btn_up_veiw.clicked.connect(lambda: self.reset_view('xy'))

    # 使用循环批量连接信号到 modify_project_data
    def connect_ui_elements(self):
        # Comboboxes
        for combo_box in [self.ui.comboBox, self.ui.comboBox_2]:
            combo_box.currentIndexChanged.connect(self.modify_project_data)

        # Checkboxes
        for check_box in [
            self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3,
            self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6,
            # self.ui.checkBox_13, self.ui.checkBox_14, self.ui.checkBox_15,
        ]:
            check_box.stateChanged.connect(self.modify_project_data)

        # Sliders
        self.ui.horizontalSlider.valueChanged.connect(self.modify_project_data)

        # LineEdits
        for line_edit in [
            self.ui.lineEdit, self.ui.lineEdit_2,
            # self.ui.lineEdit_5,
            # self.ui.lineEdit_6, self.ui.lineEdit_7, self.ui.lineEdit_8, self.ui.lineEdit_9
        ]:
            line_edit.returnPressed.connect(self.modify_project_data)

        # 添加上一个/下一个按钮的连接
        self.ui.btn_zoom_in.clicked.connect(lambda: self.switch_profile(-1))
        self.ui.btn_zoom_out.clicked.connect(lambda: self.switch_profile(1))

    def import_file(self):
        # 打开文件对话框让用户选择文件
        file_paths, _ = QFileDialog.getOpenFileNames(self, "导入数据", "",
                                                     "CSV Files (*.csv);Excel Files (*.xls *.xlsx)")
        if file_paths:
            for file_path in file_paths:
                file_name = file_path.split('/')[-1]

                # 创建 QListWidgetItem 并将文件名添加到 listWidget 中
                list_item = QListWidgetItem(file_name)
                list_item.setCheckState(Qt.Unchecked)
                self.ui.listWidget.addItem(list_item)  # 直接使用 ui 中定义的对象

                # 加载文件内容
                if file_path.endswith('.csv'):
                    data = pd.read_csv(file_path, header=0)
                else:
                    data = pd.read_excel(file_path, header=0)

                # 存储文件内容到字典中
                self.loaded_data[file_name] = data

    def show_dock(self):
        # 显示 dockWidget 侧边栏
        self.ui.dockWidget.show()  # 直接使用 ui 中定义的对象
        self.ui.dockWidget_2.show()  # 直接使用 ui 中定义的对象

    def show_data(self, item):
        file_name = item.text()
        if file_name in self.loaded_data:
            data = self.loaded_data[file_name]
            dialog = DataViewDialog(data, file_name, self)
            dialog.exec()

    def show_one_table(self, item):
        selected_files = [item.text() for item in self.ui.listWidget.findItems("", Qt.MatchContains) if
                          item.checkState() == Qt.Checked]
        if not selected_files:
            QMessageBox.warning(self, "未选择文件", "您尚未选择任何文件，请先选择文件后再继续。")
            return

        if len(selected_files) > 1:
            QMessageBox.warning(self, "文件选择错误", "您只能选择一个文件，请重新选择。")
            return

        selected_files = ','.join(selected_files)

        if selected_files in self.loaded_data:
            data = self.loaded_data[selected_files]
            dialog = Show_one_table(data, selected_files, self)

            def on_dialog_accepted():
                self.Data_loading_3D()
            dialog.accepted.connect(on_dialog_accepted)
            dialog.exec()

    def show_processed_data(self, item):
        selected_profile = item.text()
        if selected_profile in self.processed_data:
            data = self.processed_data[selected_profile]
            dialog = DataViewDialog(data, selected_profile, self)
            dialog.exec()

    def show_filtered_data(self, item):
        selected_profile = item.text()
        if selected_profile in self.filtered_data:
            data = self.filtered_data[selected_profile]
            dialog = DataViewDialog(data, selected_profile, self)
            dialog.exec()

    def switch_to_tab_2(self):
        # 切换到第二个 Tab（索引为 1）
        self.ui.tabWidget_2.setCurrentIndex(0)

    def Data_loading_3D(self):
        self.dialog = DataLoaderWithProgress(self, self.plot_3D_data, self.plot_3D_show)

    def Data_loading_profile_3D(self):
        self.dialog = DataLoaderWithProgress(self, self.plot_3D_profile_data, self.profile_3D_show)

    def plot_3D_data(self):
        selected_files = [item.text() for item in self.ui.listWidget.findItems("", Qt.MatchContains) if
                          item.checkState() == Qt.Checked]
        if not selected_files:
            QMessageBox.warning(self, "未选择文件", "您尚未选择任何文件，请先选择文件后再继续。")
            return
        selected_files = ','.join(selected_files)

        self.speed_data_1 = self.loaded_data.get(selected_files)
        speed_data = self.speed_data_1
        profile_data = None

        self.make_grid(speed_data, profile_data)
        self.make_hull_grid(speed_data, profile_data)

    def plot_3D_show(self):
        speed_data = self.speed_data_1
        profile_data = None

        self.show_plotter_bounds()
        self.plot_3d_scatter(speed_data, profile_data)
        self.plot_3d_slice(speed_data, profile_data)
        self.ui.pushButton_1.clicked.connect(lambda: self.plot_3d_isosurface(speed_data, profile_data))

        check_boxes_1 = [
            self.ui.checkBox_17, self.ui.checkBox_18
        ]
        for check_box in check_boxes_1:
            check_box.stateChanged.connect(self.plot_well)

        self.ui.checkBox_16.stateChanged.connect(lambda: self.plot_3d_scatter(speed_data, profile_data))

        check_boxes_2 = [self.ui.checkBox_19, self.ui.checkBox_20, self.ui.checkBox_21]
        for check_box in check_boxes_2:
            check_box.stateChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))

        horizontalslider_slice = [self.ui.horizontalSlider_1, self.ui.horizontalSlider_2, self.ui.horizontalSlider_3]
        for slider in horizontalslider_slice:
            slider.valueChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))

        self.ui.comboBox_1.currentIndexChanged.connect(lambda: self.plot_3d_scatter(speed_data, profile_data))
        self.ui.comboBox_1.currentIndexChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))

        check_boxes_2 = [
            self.ui.checkBox_17, self.ui.checkBox_18
        ]
        for check_box in check_boxes_2:
            check_box.stateChanged.connect(self.plot_3d_well)

    def colors_3D(self):
        colors_cn = self.ui.comboBox_1.currentText()
        if colors_cn == '彩虹1':
            self.colors_en = 'jet'
        elif colors_cn == '彩虹2':
            self.colors_en = 'rainbow'
        elif colors_cn == '冷色':
            self.colors_en = 'cool'
        elif colors_cn == '暖色':
            self.colors_en = 'hot'

    def plot_speed_contour(self):
        selected_files = [item.text() for item in self.ui.listWidget.findItems("", Qt.MatchContains) if
                          item.checkState() == Qt.Checked]
        if not selected_files:
            QMessageBox.warning(self, "未选择文件", "您尚未选择任何文件，请先选择文件后再继续。")
            return

        if len(selected_files) < 2 or len(selected_files) > 2:
            QMessageBox.warning(self, "选择文件错误", "请选择两个文件，请先选择文件后再继续。")
            return

        dialog = DataSelectionDialog(selected_files, self)
        if dialog.exec() == QDialog.Accepted:
            selections = dialog.get_selected_files()

            speed_data = None
            profile_data = None

            for file, is_speed, is_profile in selections:
                if is_speed:
                    speed_data = self.loaded_data[file]
                if is_profile:
                    profile_data = self.loaded_data[file]

            if speed_data is not None and profile_data is not None:
                self.show_combined_data(speed_data, profile_data)

    def show_combined_data(self, speed_data, profile_data):
        self.speed_data = speed_data
        self.profile_data = profile_data

        dialog = show_both_data(speed_data, profile_data, self)

        def on_dialog_accepted():
            self.Data_loading_profile_3D()
            self.show_combined_data_close()
            self.download_data(speed_data, profile_data)

        dialog.accepted.connect(on_dialog_accepted)
        dialog.exec()

    def show_combined_data_close(self):
        # 绘图完成后将所有复选框设为未选中
        for index in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(index)
            item.setCheckState(Qt.Unchecked)

    def connect_combo_box(self, combo_box, table, col, data_types):
        combo_box.currentIndexChanged.connect(lambda index: self.update_header_label(table, col, data_types[index]))

    def update_header_label(self, table, col, text):
        table.horizontalHeaderItem(col).setText(text)

    def plot_3D_profile_data(self):
        speed_data = self.speed_data
        profile_data = self.profile_data

        self.make_grid(speed_data, profile_data)
        self.make_hull_grid(speed_data, profile_data)

    def profile_3D_show(self):
        self.colors_3D()
        speed_data = self.speed_data
        profile_data = self.profile_data

        self.write_profiles(speed_data, profile_data)

        # 连接 comboBox 选择更改信号
        for combo_box in [self.ui.comboBox_2, self.ui.comboBox]:
            combo_box.currentIndexChanged.connect(lambda: self.update_plot_profile(speed_data, profile_data))

        # 连接所有 checkBox 状态更改信号
        check_boxes = [
            self.ui.checkBox, self.ui.checkBox_2, self.ui.checkBox_3,
            self.ui.checkBox_4, self.ui.checkBox_5, self.ui.checkBox_6, self.ui.checkBox_7
            # self.ui.checkBox_13, self.ui.checkBox_14, self.ui.checkBox_15
        ]
        for check_box in check_boxes:
            check_box.stateChanged.connect(lambda: self.update_plot_profile(speed_data, profile_data))

        self.ui.checkBox_6.stateChanged.connect(lambda: self.plot_well)

        check_boxes_1 = [
            self.ui.checkBox_19, self.ui.checkBox_20, self.ui.checkBox_21
        ]
        for check_box in check_boxes_1:
            check_box.stateChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))

        self.ui.checkBox_16.stateChanged.connect(lambda: self.plot_3d_scatter(speed_data, profile_data))

        horizontalslider_slice = [self.ui.horizontalSlider_1, self.ui.horizontalSlider_2, self.ui.horizontalSlider_3]
        for slider in horizontalslider_slice:
            slider.valueChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))

        check_boxes_2 = [
            self.ui.checkBox_17, self.ui.checkBox_18
        ]
        for check_box in check_boxes_2:
            check_box.stateChanged.connect(self.plot_3d_well)

        # 连接 slider 更改信号
        self.ui.horizontalSlider.valueChanged.connect(lambda: self.update_plot_profile(speed_data, profile_data))

        # 连接 lineEdit 的回车按下事件
        line_edits = [
            self.ui.lineEdit, self.ui.lineEdit_2
        ]
        for line_edit in line_edits:
            line_edit.returnPressed.connect(lambda: self.update_plot_profile(speed_data, profile_data))

        # 调用绘图代码或刷新显示
        self.plot_profile_fc(speed_data, profile_data)
        self.show_plotter_bounds()
        self.plot_3d_scatter(speed_data, profile_data)

        self.ui.listWidget_3.itemChanged.connect(lambda: self.plot_3d_profiles(speed_data, profile_data))
        self.ui.listWidget_3.itemChanged.connect(self.update_displayed_profiles)

        self.ui.pushButton_1.clicked.connect(lambda: self.plot_3d_isosurface(speed_data, profile_data))
        self.ui.pushButton_3.clicked.connect(self.plot_3d_isosurface_delete)

        self.ui.lineEdit_3.returnPressed.connect(lambda: self.plot_3d_isosurface(speed_data, profile_data))

        self.ui.comboBox_1.currentIndexChanged.connect(lambda: self.plot_3d_scatter(speed_data, profile_data))
        self.ui.comboBox_1.currentIndexChanged.connect(lambda: self.plot_3d_slice(speed_data, profile_data))
        self.ui.comboBox_1.currentIndexChanged.connect(self.update_displayed_profiles)

    def write_profiles(self, speed_data, profile_data):
        # 2D剖面：获取 profile 列表并添加到 comboBox_2
        profiles = profile_data.iloc[:, 0].unique().tolist()
        self.ui.comboBox_2.clear()
        self.ui.comboBox_2.addItems(profiles)

        # 3D剖面：获取 profile 列表并添加到 listwidget_3
        profiles = ["全选"] + profiles
        self.ui.listWidget_3.clear()  # 清空 listWidget_3
        self.list_items = []  # 存储所有 QListWidgetItem 的引用

        # 全选逻辑
        def all_selected():
            """处理全选/全不选逻辑"""
            is_checked = self.list_items[0].checkState() == Qt.Checked
            for i in range(1, len(self.list_items)):  # 跳过第一个"全选"
                self.list_items[i].setCheckState(Qt.Checked if is_checked else Qt.Unchecked)

        # 更新显示选中项
        def show_selected():
            """显示选中的项"""
            selected_items = [
                item.text() for item in self.list_items[1:]  # 跳过"全选"
                if item.checkState() == Qt.Checked
            ]
            # 更新文本框显示选中的项
            # self.ui.textBrowser.setText(", ".join(selected_items))

        # 添加选项到 listWidget_3
        for i, profile_name in enumerate(profiles):
            list_item = QListWidgetItem(profile_name)
            list_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            list_item.setCheckState(Qt.Unchecked)
            self.ui.listWidget_3.addItem(list_item)
            self.list_items.append(list_item)  # 存储到 list_items 中

            # 连接信号
            if i == 0:  # "全选"项
                list_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                list_item.setCheckState(Qt.Unchecked)
                self.ui.listWidget_3.itemChanged.connect(
                    lambda item=list_item: all_selected() if item == self.list_items[0] else None
                )
            else:  # 其他普通项
                list_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                self.ui.listWidget_3.itemChanged.connect(show_selected)

    def plot_profile_fc(self, speed_data, profile_data):

        # 检查并删除现有的 colorbar
        if hasattr(self, 'cbar'):
            self.cbar.remove()
            del self.cbar

        self.ax.clear()

        selected_profile = self.ui.comboBox_2.currentText()  # 获取当前选中的剖面
        selected_points = profile_data[profile_data.iloc[:, 0] == selected_profile].iloc[:,
                          1:].values.flatten().tolist()
        filtered_speed_data = speed_data[speed_data.iloc[:, 0].isin(selected_points)]

        unique_observation_points = filtered_speed_data.iloc[:, :3].drop_duplicates()
        x = unique_observation_points.iloc[:, 1].values.reshape(-1, 1)
        y = unique_observation_points.iloc[:, 2].values

        model = LinearRegression()
        model.fit(x, y)
        self.coef = model.coef_[0]
        self.intercept = model.intercept_
        m = self.coef
        b = self.intercept
        projections = []
        for index, row in unique_observation_points.iterrows():
            x1, y1 = row.iloc[1], row.iloc[2]
            x2, y2 = self.perpendicular_projection(m, b, x1, y1)
            projections.append((x2, y2))
        projection_df = pd.DataFrame(projections, columns=['横坐标投影', '纵坐标投影'],
                                     index=unique_observation_points.index)
        unique_observation_points = pd.concat([unique_observation_points, projection_df], axis=1)

        self.first_point = unique_observation_points.iloc[0, 3:5].values
        self.last_point = unique_observation_points.iloc[-1, 3:5].values
        first_point = self.first_point
        distances = unique_observation_points.apply(lambda row: distance.euclidean(first_point, row.iloc[3:5]), axis=1)
        unique_observation_points['距离到第一个点'] = distances

        new_filtered_speed_data = filtered_speed_data.drop(filtered_speed_data.columns[[1, 2]], axis=1)
        new_filtered_speed_data = new_filtered_speed_data.merge(
            unique_observation_points.iloc[:, [0, -1]],
            left_on=new_filtered_speed_data.columns[0],
            right_on=unique_observation_points.columns[0],
            how='left'
        )

        last_col = new_filtered_speed_data.columns[-1]
        col_order = [new_filtered_speed_data.columns[0], last_col] + list(new_filtered_speed_data.columns[1:-1])
        new_filtered_speed_data = new_filtered_speed_data[col_order]

        x = new_filtered_speed_data.iloc[:, 1].values
        y = new_filtered_speed_data.iloc[:, 2].values
        z = new_filtered_speed_data.iloc[:, 3:].values.flatten()

        tri = Delaunay(np.column_stack((x, y)))  # Delaunay三角剖分

        unique_x = np.unique(x)  # 找到唯一的 x 值
        max_y_for_x = [y[x == ux].max() for ux in unique_x]  # 对于每个唯一的 x 值，找到对应的最大 y 值
        min_y_for_x = [y[x == ux].min() for ux in unique_x]  # 对于每个唯一的 x 值，找到对应的最小 y 值
        min_max_y_for_x = min(max_y_for_x)  # 对于每个唯一的 x 值对应最大y值的最小值
        max_min_y_for_x = max(min_y_for_x)  # 对于每个唯一的 x 值对应最小y值的最大值

        xi = np.linspace(x.min(), x.max(), 500)
        yi = np.linspace(max_min_y_for_x, min_max_y_for_x, 500)
        xi, yi = np.meshgrid(xi, yi)

        # 将Delaunay结果转换为Triangulation格式以便插值
        triang = Triangulation(x, y, tri.simplices)
        interpolator = LinearTriInterpolator(triang, z)

        # 计算插值结果
        zi = interpolator(xi, yi)

        # 设置y轴范围
        self.ax.set_ylim(max_min_y_for_x, min_max_y_for_x)

        colors_cn = self.ui.comboBox.currentText()
        if colors_cn == '彩虹1':
            colors_en = 'jet'
        elif colors_cn == '彩虹2':
            colors_en = 'rainbow'
        elif colors_cn == '冷色':
            colors_en = 'cool'
        elif colors_cn == '暖色':
            colors_en = 'hot'

        if self.ui.checkBox_2.isChecked():
            z_max_ceiling = np.ceil(z.max() / 100) * 100
            contour = self.ax.contourf(xi, yi, zi, levels=np.linspace(0, z_max_ceiling, 200), cmap=colors_en)

            if self.ui.checkBox_3.isChecked():
                self.cbar = self.figure.colorbar(contour, ax=self.ax, extend='both', fraction=0.005)
                self.cbar.ax.invert_yaxis()

                # 通过 np.arange 设置刻度
                z_max_ceiling = np.ceil(z.max() / 100) * 100
                ticks = np.arange(0, z_max_ceiling + 100, 1000)
                self.cbar.set_ticks(ticks)

        if self.ui.checkBox_4.isChecked():
            # 使用高斯滤波来进一步平滑数据
            zi_smooth = gaussian_filter(zi, sigma=self.ui.horizontalSlider.value())  # 调整 sigma 值来控制平滑程度，1-3 是常用的范围

            # 确保 z_min 和 z_max 为整百数
            z_min = np.floor(zi_smooth.min() / 100) * 100  # 向下取整到最近的整百数
            z_max = np.ceil(zi_smooth.max() / 100) * 100  # 向上取整到最近的整百数

            # 设置等高线 levels，确保为整百数
            linetext = self.ui.lineEdit.text()
            try:
                linenumber = int(linetext)  # 将字符串转换为整数
                if linenumber <= 0:
                    raise ValueError("The step value must be greater than zero.")
            except ValueError:
                QMessageBox.critical(self, "输入错误", "请输入一个有效的正整数！")
                return

            levels = np.arange(z_min, z_max, linenumber)
            contour_lines = self.ax.contour(xi, yi, zi_smooth, levels=levels, colors='black')
            # 添加等高线标签
            if self.ui.checkBox.isChecked():
                self.ax.clabel(contour_lines, inline=True, fontsize=8, fmt="%.1f", colors='black')

        x_label = "距离（m）"
        y_label = "深度（m）"
        title_label = "剖面图"

        # if self.ui.checkBox_15.isChecked():
        self.ax.tick_params(axis='y', which='both', left=True, labelleft=True)  # 显示 y 轴的刻度和标签
        self.ax.set_ylabel(y_label)
        # else:
        #     self.ax.tick_params(axis='y', which='both', left=False, labelleft=False)  # 隐藏 y 轴的刻度和标签

        # if self.ui.checkBox_14.isChecked():
        self.ax.tick_params(axis='x', which='both', left=True, labelleft=True)  # 显示x轴的刻度和标签
        self.ax.set_xlabel(x_label)
        # else:
        # self.ax.tick_params(axis='x', which='both', left=False, labelleft=False)  # 隐藏 x 轴的刻度和标签

        # if self.ui.checkBox_13.isChecked():
        self.ax.set_title(title_label, pad=10)
        # else:
        #     self.ax.set_title('')  # 清除标题

        # y_lim_min = self.ui.lineEdit_8.text()
        # y_lim_max = self.ui.lineEdit_9.text()
        # try:
        #     # 使用三元表达式来简化逻辑
        #     y_lim_min = float(y_lim_min) if y_lim_min else max_min_y_for_x
        #     y_lim_max = float(y_lim_max) if y_lim_max else min_max_y_for_x
        #
        #     # 设置 y 轴范围
        #     self.ax.set_ylim(y_lim_min, y_lim_max)
        # except ValueError:
        #     QMessageBox.warning(self, "输入错误", "请输入有效的数字作为 y 轴的最小值和最大值。")


        if self.ui.checkBox_5.isChecked():
            y_min, y_max = self.ax.get_ylim()
            scatter = self.ax.scatter(unique_observation_points.iloc[:, -1],
                                      np.zeros_like(unique_observation_points.iloc[:, -1])+y_max-100,
                                      color='red', marker='v', s=100, label='Data points')
            texts = []
            for i, txt in enumerate(unique_observation_points.iloc[:, 0]):
                texts.append(self.ax.text(unique_observation_points.iloc[:, -1].iloc[i], 0, txt, fontsize=10, ha='center', va='bottom'))

        # 更新图像
        self.ax.set_aspect('equal', adjustable='box')
        layout = self.ui.widget_3.layout()
        layout.addWidget(self.canvas)
        self.canvas.draw()

        # 在绘图完成后，确保比例尺在最上层
        if hasattr(self, 'scale_bar_label'):
            self.scale_bar_label.raise_()

    # 更新图表函数，基于 ComboBox 的选择
    def update_plot_profile(self, speed_data, profile_data):
        # 调用绘图代码或刷新显示
        self.plot_profile_fc(speed_data, profile_data)
        self.plot_well()

    def perpendicular_projection(self, m, b, x1, y1):
        x2 = (x1 + m * (y1 - b)) / (m ** 2 + 1)
        y2 = (m * x1 + (m ** 2) * y1 + b) / (m ** 2 + 1)
        return x2, y2

    def show_context_menu(self, position: QPoint):
        item = self.ui.listWidget.itemAt(position)
        if item:
            context_menu = QMenu(self)
            open_action = QAction("显示数据", self)
            delete_action = QAction("删除", self)

            open_action.triggered.connect(lambda: self.show_data(item))
            delete_action.triggered.connect(lambda: self.delete_item(item))

            context_menu.addAction(open_action)
            context_menu.addAction(delete_action)
            context_menu.exec(self.ui.listWidget.mapToGlobal(position))

    def show_context_menu_1(self, position: QPoint):
        item_1 = self.ui.listWidget_2.itemAt(position)
        if item_1:
            context_menu = QMenu(self)
            download_action = QAction("下载处理数据", self)
            download_action.triggered.connect(self.processed_data_export_to_csv)

            show_processed_data_action = QAction("显示处理数据", self)
            show_processed_data_action.triggered.connect(
                lambda: self.show_processed_data(item_1))  # 使用 lambda 传递 item_1

            show_filtered_data_action = QAction("显示原始数据", self)
            show_filtered_data_action.triggered.connect(lambda: self.show_filtered_data(item_1))

            context_menu.addAction(download_action)
            context_menu.addAction(show_processed_data_action)
            context_menu.addAction(show_filtered_data_action)
            context_menu.exec(self.ui.listWidget_2.mapToGlobal(position))

    def delete_item(self, item):
        file_name = item.text()
        if file_name in self.loaded_data:
            del self.loaded_data[file_name]
        self.ui.listWidget.takeItem(self.ui.listWidget.row(item))

    def listWidget_key_press_event(self, event):
        if event.key() == Qt.Key_Delete:
            selected_items = self.ui.listWidget.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.delete_item(item)

    def download_data(self, speed_data, profile_data):
        profiles = profile_data.iloc[:, 0].unique().tolist()

        # 遍历每个剖面名称
        for selected_profile in profiles:

            selected_points = profile_data[profile_data.iloc[:, 0] == selected_profile].iloc[:,
                              1:].values.flatten().tolist()
            filtered_speed_data = speed_data[speed_data.iloc[:, 0].isin(selected_points)]

            # 将筛选过的数据存储到字典中
            self.filtered_data[selected_profile] = filtered_speed_data

            unique_observation_points = filtered_speed_data.iloc[:, :3].drop_duplicates()
            x = unique_observation_points.iloc[:, 1].values.reshape(-1, 1)
            y = unique_observation_points.iloc[:, 2].values

            model = LinearRegression()
            model.fit(x, y)
            m = model.coef_[0]
            b = model.intercept_
            projections = []
            for index, row in unique_observation_points.iterrows():
                x1, y1 = row.iloc[1], row.iloc[2]
                x2, y2 = self.perpendicular_projection(m, b, x1, y1)
                projections.append((x2, y2))
            projection_df = pd.DataFrame(projections, columns=['横坐标投影', '纵坐标投影'],
                                         index=unique_observation_points.index)
            unique_observation_points = pd.concat([unique_observation_points, projection_df], axis=1)

            first_point = unique_observation_points.iloc[0, 3:5].values
            distances = unique_observation_points.apply(lambda row: distance.euclidean(first_point, row.iloc[3:5]),
                                                        axis=1)
            unique_observation_points['距离到第一个点'] = distances

            new_filtered_speed_data = filtered_speed_data.drop(filtered_speed_data.columns[[1, 2]], axis=1)
            new_filtered_speed_data = new_filtered_speed_data.merge(
                unique_observation_points.iloc[:, [0, -1]],
                left_on=new_filtered_speed_data.columns[0],
                right_on=unique_observation_points.columns[0],
                how='left'
            )

            last_col = new_filtered_speed_data.columns[-1]
            col_order = [new_filtered_speed_data.columns[0], last_col] + list(new_filtered_speed_data.columns[1:-1])
            new_filtered_speed_data = new_filtered_speed_data[col_order]

            # 创建 QListWidgetItem 并将文件名添加到 listWidget 中
            list_item1 = QListWidgetItem(selected_profile)
            list_item1.setCheckState(Qt.Unchecked)
            self.ui.listWidget_2.addItem(list_item1)  # 直接使用 ui 中定义的对象

            # 将处理后的数据存储到processed_data字典中
            self.processed_data[selected_profile] = new_filtered_speed_data

    def processed_data_export_to_csv(self):
        # 获取选中的剖面名称列表
        selected_profiles = [item.text() for item in self.ui.listWidget_2.findItems("", Qt.MatchContains) if
                             item.checkState() == Qt.Checked]

        # 如果没有选中任何项目，弹出警告
        if not selected_profiles:
            QMessageBox.warning(self, "未选择文件", "您尚未选择任何文件，请先选择文件后再继续。")
            return

        # 弹出文件夹选择对话框，让用户选择保存位置
        folder = QFileDialog.getExistingDirectory(self, "选择保存文件夹")

        # 如果用户没有选择文件夹，取消操作
        if not folder:
            QMessageBox.warning(self, "取消保存", "保存操作已取消")
            return

        # 遍历每个选中的剖面名称，逐个保存文件
        for selected_profile in selected_profiles:
            if selected_profile not in self.processed_data:
                QMessageBox.warning(self, "文件未找到", f"未找到对应的数据文件：{selected_profile}")
                continue

            data = self.processed_data[selected_profile]

            # 生成完整的文件路径（包括剖面名称作为文件名的一部分）
            filename = f"{folder}/{selected_profile}_处理数据.csv"

            try:
                # 将数据保存为 CSV 文件
                data.to_csv(filename, index=False)
                QMessageBox.information(self, "保存成功", f"数据已成功保存到 {filename}")
            except Exception as e:
                # 如果保存失败，弹出错误信息
                QMessageBox.critical(self, "保存失败", f"保存数据时发生错误: {str(e)}")

    def filtered_data_export_to_csv(self):
        # 获取选中的剖面名称列表
        selected_profiles = [item.text() for item in self.ui.listWidget_2.findItems("", Qt.MatchContains) if
                             item.checkState() == Qt.Checked]

        # 如果没有选中任何项目，弹出警告
        if not selected_profiles:
            QMessageBox.warning(self, "未选择文件", "您尚未选择任何文件，请先选择文件后再继续。")
            return

        # 弹出文件夹选择对话框，让用户选择保存位置
        folder = QFileDialog.getExistingDirectory(self, "选择保存文件夹")

        # 如果用户没有选择文件夹，取消操作
        if not folder:
            QMessageBox.warning(self, "取消保存", "保存操作已取消")
            return

        # 遍历每个选中的剖面名称，逐个保存文件
        for selected_profile in selected_profiles:
            if selected_profile not in self.filtered_data:
                QMessageBox.warning(self, "文件未找到", f"未找到对应的数据文件：{selected_profile}")
                continue

            data = self.filtered_data[selected_profile]

            # 生成完整的文件路径（包括剖面名称作为文件名的一部分）
            filename = f"{folder}/{selected_profile}_原始数据.csv"

            try:
                # 将数据保存为 CSV 文件
                data.to_csv(filename, index=False)
                QMessageBox.information(self, "保存成功", f"数据已成功保存到 {filename}")
            except Exception as e:
                # 如果保存失败，弹出错误信息
                QMessageBox.critical(self, "保存失败", f"保存数据时发生错误: {str(e)}")

    def plot_well_state(self):
        selected_files = [item.text() for item in self.ui.listWidget.findItems("", Qt.MatchContains) if
                          item.checkState() == Qt.Checked]
        if not selected_files:
            QMessageBox.warning(self, "未选择文件", "您尚未选择钻孔数据，请先选择文件后再继续。")
            return

        well_data_frames = [self.loaded_data[file_name] for file_name in selected_files if
                            file_name in self.loaded_data]
        well_data = pd.concat(well_data_frames, ignore_index=True)
        self.well_data = well_data
        self.ui.checkBox_6.setChecked(True)
        self.plot_well()

    def plot_well(self):
        if self.ui.checkBox_6.isChecked():
            try:
                well_data = self.well_data

                m = self.coef
                b = self.intercept
                processed_well_data = []
                for index, row in well_data.iterrows():
                    x1, y1 = row.iloc[1], row.iloc[2]
                    x2 = (x1 + m * (y1 - b)) / (m ** 2 + 1)
                    y2 = (m * x1 + (m ** 2) * y1 + b) / (m ** 2 + 1)
                    processed_well_data.append((x2, y2))
                processed_well_data_df = pd.DataFrame(processed_well_data, columns=['横坐标投影', '纵坐标投影'],
                                                      index=well_data.index)

                well_data = pd.concat([well_data, processed_well_data_df], axis=1)

                first_point = self.first_point
                last_point = self.last_point
                distances_to_firstPint = well_data.apply(lambda row: distance.euclidean(first_point, row.iloc[5:7]),
                                                         axis=1)
                well_data['到第一个点距离'] = distances_to_firstPint

                distances_to_line = well_data.apply(lambda row: distance.euclidean(row.iloc[1:3], row.iloc[5:7]),
                                                    axis=1)
                well_data['到剖面距离'] = distances_to_line

                # 筛选出合理投影距离和剖面范围内的数据
                projection_distance_text = self.ui.lineEdit_2.text()
                projection_distance = float(projection_distance_text)
                filtered_well_data = well_data[well_data['到剖面距离'] < projection_distance]
                filtered_well_data = filtered_well_data[filtered_well_data['横坐标投影'] > first_point[0]]
                filtered_well_data = filtered_well_data[filtered_well_data['横坐标投影'] < last_point[0]]

                # 绘制散点图
                if not filtered_well_data.empty:

                    # 绘制垂直线
                    texts = []
                    y_min, y_max = self.ax.get_ylim()
                    for index, row in filtered_well_data.iterrows():
                        x = np.array([row['到第一个点距离'], row['到第一个点距离']])  # 到第一个点的距离作为x轴
                        y = np.array([y_max, -row.iloc[4]])  # 深度数据作为y轴
                        y_1 = np.array([y_max, -row.iloc[3]])  # 另一组深度数据作为y_1

                        self.ax.plot(x, y, color='red', linewidth=4)  # 红色线条
                        self.ax.plot(x, y_1, color='yellow', linewidth=4)  # 黄色线条

                        if self.ui.checkBox_7.isChecked():
                            well_name = row.iloc[0]
                            texts.append(
                                self.ax.text(row['到第一个点距离'], 0, well_name, fontsize=10, ha='center', va='bottom')
                            )



                self.canvas.draw()
            except Exception as e:
                QMessageBox.warning(self, "错误", "请选择正确的钻孔数据")

    def plot_3d_scatter(self, speed_data, profile_data):
        self.colors_3D()
        if self.ui.checkBox_16.isChecked():
            # 读取点云数据 (假设你的 Excel 文件路径正确)
            data = self.speed_data

            x = data.iloc[:, 1].values
            y = data.iloc[:, 2].values
            z = data.iloc[:, 3].values
            values = data.iloc[:, 4].values

            points = np.vstack((x, y, z)).T
            scalars = values

            # 创建点云数据
            point_cloud = pv.PolyData(points)
            point_cloud["Scalars"] = scalars  # 添加标量值

            # 删除先前的散点（如果存在）
            if hasattr(self, 'scatter_actor') and self.scatter_actor is not None:
                self.plotter.remove_actor(self.scatter_actor)
                self.scatter_actor = None  # 清除引用

            self.scatter_actor = self.plotter.add_mesh(
                point_cloud,
                render_points_as_spheres=True,
                point_size=10,
                cmap=self.colors_en,  # 使用颜色映射表
                scalars="Scalars",  # 指定标量数据
                show_scalar_bar=False  # 不显示颜色条
            )
            self.plotter.show()

        else:
            # 删除先前的等值面（如果存在）
            if hasattr(self, 'scatter_actor') and self.scatter_actor is not None:
                self.plotter.remove_actor(self.scatter_actor)
                self.scatter_actor = None  # 清除引用

            self.plotter.show()
            self.plotter.update()

    def make_hull_grid(self, speed_data, profile_data):
        data = speed_data

        x = data.iloc[:, 1].values
        y = data.iloc[:, 2].values
        z = data.iloc[:, 3].values
        values = data.iloc[:, 4].values

        # 计算散点的凸包
        points = np.c_[x, y, z]  # 散点的三维坐标
        hull = ConvexHull(points)  # 计算凸包

        # 插值并生成网格
        grid_x, grid_y, grid_z = np.mgrid[
                                 x.min():x.max():100j,
                                 y.min():y.max():100j,
                                 z.min():z.max():100j
                                 ]
        grid_points = np.c_[grid_x.ravel(), grid_y.ravel(), grid_z.ravel()]  # 网格点的三维坐标

        grid_values = griddata(points, values, grid_points, method='linear')  # 插值到网格
        grid_values = np.nan_to_num(grid_values)

        tri = Delaunay(points)  # 构建三维 Delaunay 三角剖分
        mask = tri.find_simplex(grid_points) >= 0  # 判断网格点是否在凸包内
        grid_values[~mask] = np.nan  # 将凸包外的点置为 NaN

        # 创建 StructuredGrid 用于可视化插值结果
        grid = pv.StructuredGrid()
        grid.points = grid_points  # 设置网格点坐标
        grid.dimensions = grid_x.shape  # 设置网格形状
        grid["values"] = grid_values  # 将插值值赋予网格点
        grid["Elevation"] = grid_points[:, 2]
        self.hull_grid = grid

    def plot_3d_isosurface(self, speed_data, profile_data):
        if hasattr(self, 'isosurface_actor') and self.isosurface_actor is not None:
            self.plotter.remove_actor(self.isosurface_actor)
            self.isosurface_actor = None  # 清除引用

        # 生成新的等值面
        isovalue_text = self.ui.lineEdit_3.text()
        try:
            isovalue = float(isovalue_text)
            contour = self.hull_grid.contour(isosurfaces=[isovalue])
            vmin = self.hull_grid["Elevation"].min()
            vmax = self.hull_grid["Elevation"].max()

            self.isosurface_actor = self.plotter.add_mesh(contour, cmap="jet", scalars=contour["Elevation"],
                                                          clim=[vmin, vmax], show_scalar_bar=False, opacity=1)
        except ValueError:
            print("输入的等值面值无效，请输入一个有效的数字。")

    def plot_3d_isosurface_delete(self):
        if hasattr(self, 'isosurface_actor') and self.isosurface_actor is not None:
            self.plotter.remove_actor(self.isosurface_actor)
            self.isosurface_actor = None  # 清除引用

    def plot_3d_profiles(self, speed_data, profile_data):
        data = speed_data
        point_pairs = []
        for profile_name in profile_data.iloc[:, 0].unique():
            selected_points = profile_data[profile_data.iloc[:, 0] == profile_name].iloc[:,
                              1:].values.flatten().tolist()
            filtered_speed_data = data[data.iloc[:, 0].isin(selected_points)]
            first_point = filtered_speed_data.iloc[0, 1:3]
            last_point = filtered_speed_data.iloc[-1, 1:3]
            # print(first_point)

            # 将当前剖面的点对添加到 point_pairs 中
            point_pairs.append((np.array(first_point), np.array(last_point)))

        self.all_profiles_data = {}

        # 循环遍历每个点对，生成剖面
        for index, (point1, point2) in enumerate(point_pairs):
            # 计算法向量（剖面的方向向量）
            point1 = np.append(point1, 0).astype(float)
            point2 = np.append(point2, 0).astype(float)
            point3 = (point1 + point2) / 2
            point3[2] = -500

            v1 = point2 - point1
            v2 = point3 - point1

            normal = np.cross(v1, v2)

            # 剖面的法向量归一化
            normal = normal / np.linalg.norm(normal)

            # 创建剖面，法向量和原点基于给定的点对
            slice_custom = self.grid.slice(normal=normal, origin=point3)

            self.all_profiles_data[f"slice_{index}"] = slice_custom

    def update_displayed_profiles(self):
        self.colors_3D()
        # 创建自定义 colormap，将 0 值显示为灰色
        jet_cmap = plt.get_cmap(self.colors_en, 256)  # 生成 jet 颜色映射
        colors = jet_cmap(np.linspace(0, 1, 256))  # 将颜色映射分成 256 个等级
        colors[0] = np.array([0.5, 0.5, 0.5, 0])  # 将第一个等级 (values = 0) 设置为透明

        # 创建新的 colormap
        new_cmap = ListedColormap(colors)

        # 获取当前选中的剖面
        slice_to_display = []
        for index in range(1, self.ui.listWidget_3.count()):
            list_item = self.ui.listWidget_3.item(index)
            if list_item.checkState() == Qt.Checked:
                slice_name = f"slice_{index - 1}"  # 注意索引从 1 开始
                slice_to_display.append(slice_name)

        # 更新显示的网格
        for slice_name in slice_to_display:
            if slice_name not in self.displayed_slices:
                slice_custom = self.all_profiles_data.get(slice_name)
                if slice_custom:
                    self.slice_actor[f"{slice_name}"] = self.plotter.add_mesh(slice_custom, scalars=slice_custom["values"], cmap=new_cmap, opacity=1,
                                      show_scalar_bar=False)
                    self.displayed_slices.append(slice_name)  # 记录已显示的剖面
            else:
                continue

        # 删除未选中的剖面
        for slice_name in list(self.displayed_slices):  # 使用 list 转换以便迭代时修改
            if slice_name not in slice_to_display:
                # 如果当前未勾选该剖面，删除该剖面
                slice_custom = self.all_profiles_data.get(slice_name)
                if slice_custom:  # 确保有对应的剖面数据
                    self.plotter.remove_actor(self.slice_actor[f"{slice_name}"])  # 从 plotter 中移除网格
                    self.displayed_slices.remove(slice_name)  # 从已显示的剖面集合中删除

    def make_grid(self, speed_data, profile_data):
        # 读取点云数据
        data = speed_data

        x = data.iloc[:, 1].values
        y = data.iloc[:, 2].values
        z = data.iloc[:, 3].values
        values = data.iloc[:, 4].values

        # 插值并生成网格
        grid_x, grid_y, grid_z = np.mgrid[
                                 x.min():x.max():100j,
                                 y.min():y.max():100j,
                                 z.min():z.max():100j
                                 ]

        grid_values = griddata((x, y, z), values, (grid_x, grid_y, grid_z), method='linear')
        grid_values = np.nan_to_num(grid_values)

        # 创建 StructuredGrid 用于可视化插值结果
        grid = pv.StructuredGrid(grid_x, grid_y, grid_z)
        grid["values"] = grid_values.flatten(order="F")
        self.grid = grid


    def plot_3d_slice(self, speed_data, profile_data):
        self.colors_3D()
        jet_cmap = plt.get_cmap(self.colors_en, 256)  # 生成 jet 颜色映射
        colors = jet_cmap(np.linspace(0, 1, 256))  # 将颜色映射分成 256 个等级
        colors[0] = np.array([0.5, 0.5, 0.5, 0])  # 将第一个等级 (values = 0) 设置为透明

        # 创建新的 colormap
        new_cmap = ListedColormap(colors)

        # 提取 z 坐标数据
        z_coords = self.grid.points[:, 2]
        z_min = z_coords.min()
        z_max = z_coords.max()
        z_midel = (z_min + z_max) / 2

        # 提取 z 坐标数据
        x_coords = self.grid.points[:, 0]
        x_min = x_coords.min()
        x_max = x_coords.max()
        x_midel = (x_min + x_max) /2

        y_coords = self.grid.points[:, 1]
        y_min = y_coords.min()
        y_max = y_coords.max()
        y_midel = (y_min + y_max) / 2

        slider_value_1 = self.ui.horizontalSlider_1.value() / 100

        slider_value_2 = self.ui.horizontalSlider_2.value() / 100

        slider_value_3 = self.ui.horizontalSlider_3.value() / 100

        # x切片
        if self.ui.checkBox_19.isChecked():
            x_value = (x_max - x_min) * slider_value_1 + x_min
            origin = [x_value, y_midel, z_midel]

            if hasattr(self, 'x_slice') and self.x_slice is not None:
                self.plotter.remove_actor(self.x_slice)
                self.x_slice = None  # 清除引用

            if not hasattr(self, 'x_slice') or self.x_slice is None:
                slice_grid = self.grid.slice(normal='x', origin=origin)
                self.x_slice = self.plotter.add_mesh(slice_grid, cmap=new_cmap, scalars=slice_grid["values"],
                                                     show_scalar_bar=False, opacity=1.0, show_edges=False)

        else:
            if hasattr(self, 'x_slice') and self.x_slice is not None:
                self.plotter.remove_actor(self.x_slice)
                self.x_slice = None

        # y切片
        if self.ui.checkBox_20.isChecked():
            y_value = (y_max - y_min) * slider_value_2 + y_min
            origin = [x_midel, y_value, z_midel]

            if hasattr(self, 'y_slice') and self.y_slice is not None:
                self.plotter.remove_actor(self.y_slice)
                self.y_slice = None  # 清除引用

            if not hasattr(self, 'y_slice') or self.y_slice is None:
                slice_grid = self.grid.slice(normal='y', origin=origin)
                self.y_slice = self.plotter.add_mesh(slice_grid, cmap=new_cmap, scalars=slice_grid["values"],
                                                     show_scalar_bar=False, opacity=1.0, show_edges=False)

        else:
            if hasattr(self, 'y_slice') and self.y_slice is not None:
                self.plotter.remove_actor(self.y_slice)
                self.y_slice = None

        # z切片
        if self.ui.checkBox_21.isChecked():
            z_value = (z_max - z_min) * slider_value_3 + z_min
            origin = [x_midel, y_midel, z_value]

            if hasattr(self, 'z_slice') and self.z_slice is not None:
                self.plotter.remove_actor(self.z_slice)
                self.z_slice = None  # 清除引用

            if not hasattr(self, 'z_slice') or self.z_slice is None:
                slice_grid = self.grid.slice(normal='z', origin=origin)
                self.z_slice = self.plotter.add_mesh(slice_grid, cmap=new_cmap, scalars=slice_grid["values"],
                                                     show_scalar_bar=False, opacity=1.0, show_edges=False)

        else:
            if hasattr(self, 'z_slice') and self.z_slice is not None:
                self.plotter.remove_actor(self.z_slice)
                self.z_slice = None

        self.plotter.update()

    def plot_3d_well(self):
        if not hasattr(self, "well_data"):
            selected_files = [item.text() for item in self.ui.listWidget.findItems("", Qt.MatchContains) if
                              item.checkState() == Qt.Checked]
            if not selected_files:
                QMessageBox.warning(self, "未选择文件", "您尚未选择钻孔数据，请先选择文件后再继续。")
                self.ui.checkBox_17.setChecked(False)
                return

            well_data_frames = [self.loaded_data[file_name] for file_name in selected_files if
                                file_name in self.loaded_data]
            self.well_data = pd.concat(well_data_frames, ignore_index=True)

        # 设置圆柱的半径
        cylinder_radius = 100
        well_data = self.well_data

        if self.ui.checkBox_17.isChecked():
            try:
                # 绘制第四系
                for index, row in well_data.iterrows():
                    start_point = [row.iloc[1], row.iloc[2], 0]
                    end_point = [row.iloc[1], row.iloc[2], -row.iloc[3]]

                    # 计算圆柱的高度
                    height = row.iloc[4]  # 圆柱的高度

                    # 计算圆柱的方向（起点到终点的向量）
                    direction = [end_point[0] - start_point[0], end_point[1] - start_point[1],
                                 end_point[2] - start_point[2]]

                    if self.ui.checkBox_18.isChecked():
                        # 可以选择在圆柱上方显示其名称
                        well_name = row["Name"]  # 从第一列获取名称
                        label_position = [(start_point[0] + end_point[0]) / 2,
                                          (start_point[1] + end_point[1]) / 2,
                                          (start_point[2] + end_point[2]) / 2 + height / 2]  # 中间位置
                        if f"cylinder_{index}" not in self.all_well_name:
                            self.all_well_name[f"cylinder_{index}"] = self.plotter.add_point_labels([label_position], [well_name], font_size=16, text_color="black",
                                                          always_visible=True, background_color=[0.5, 0.5, 0.5, 0])
                            self.plotter.update()
                        else:
                            continue

                    else:
                        if hasattr(self, 'all_well_name') and self.all_well_name:
                            self.plotter.remove_actor(self.all_well_name[f"cylinder_{index}"])

                    # 创建圆柱
                    cylinder = pv.Cylinder(center=start_point, direction=direction, radius=cylinder_radius,
                                           height=height)
                    if f"cylinder_{index}" not in self.all_q_cylinder:
                        # 添加圆柱到场景中，并为其设置名称
                        self.all_q_cylinder[f"cylinder_{index}"] = self.plotter.add_mesh(cylinder, color="blue")
                    else:
                        continue

                # 绘制基岩
                for index, row in well_data.iterrows():
                    start_point = [row.iloc[1], row.iloc[2], -row.iloc[3]]
                    end_point = [row.iloc[1], row.iloc[2], -row.iloc[4]]

                    # 计算圆柱的高度
                    height = row.iloc[4]  # 圆柱的高度

                    # 计算圆柱的方向（起点到终点的向量）
                    direction = [end_point[0] - start_point[0], end_point[1] - start_point[1],
                                 end_point[2] - start_point[2]]

                    # 创建圆柱
                    cylinder = pv.Cylinder(center=start_point, direction=direction, radius=cylinder_radius,
                                           height=height)

                    # 添加圆柱到场景中
                    if f"cylinder_{index}" not in self.all_baserock_cylinder:
                        self.all_baserock_cylinder[f"cylinder_{index}"] = self.plotter.add_mesh(cylinder, color="red")
                    else:
                        continue

                    self.plotter.update()

            except Exception as e:
                QMessageBox.warning(self, "错误", "请选择正确的钻孔数据")

        else:
            for index, row in well_data.iterrows():
                if hasattr(self, 'all_q_cylinder') and self.all_q_cylinder:
                    self.plotter.remove_actor(self.all_q_cylinder[f"cylinder_{index}"])
                if hasattr(self, 'all_baserock_cylinder') and self.all_baserock_cylinder:
                    self.plotter.remove_actor(self.all_baserock_cylinder[f"cylinder_{index}"])
                if hasattr(self, 'all_well_name') and self.all_well_name:
                    self.plotter.remove_actor(self.all_well_name[f"cylinder_{index}"])

            self.all_q_cylinder = {}
            self.all_baserock_cylinder = {}
            self.all_well_name = {}

    def show_plotter_bounds(self):
        # 调用绘图代码或刷新显示
        # 清空之前的内容
        layout = self.ui.widget_5.layout()  # 获取布局
        layout.addWidget(self.plotter.interactor)  # 将 FigureCanvas 添加到布局中
        self.plotter.clear()
        self.plotter.show_bounds(
            color='k',
            all_edges=True,
            show_xaxis=False,
            show_yaxis=False,
            show_zaxis=False,
            show_xlabels=False,
            show_ylabels=False,
            show_zlabels=False,
            ztitle=' ',
        )

    def reset_view(self, camera_position):
        self.plotter.camera_position = camera_position  # 设置视角
        self.plotter.reset_camera()  # 重置相机
        self.plotter.render()  # 强制重新渲染

    def export_figures(self):
        # 弹出保存对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;PDF Files (*.pdf);;All Files (*)"
        )

        if file_path:  # 用户选择了保存路径
            self.canvas.figure.savefig(file_path, dpi=300, bbox_inches='tight')
            print(f"Image saved to: {file_path}")

    def update_ui_with_project_data(self):
        # 更新主窗口标题
        self.setWindowTitle(self.project_data.get("project_name", "项目"))

        # 清空并重新加载 listWidget 和 listWidget_2 中的文件
        self.ui.listWidget.clear()
        self.ui.listWidget_2.clear()

        # 重新加载已保存的文件列表
        for file_name in self.project_data.get("loaded_files", []):
            list_item = QListWidgetItem(file_name)
            list_item.setCheckState(Qt.Unchecked)
            self.ui.listWidget.addItem(list_item)

        for file_name in self.project_data.get("filtered_files", []):
            list_item = QListWidgetItem(file_name)
            list_item.setCheckState(Qt.Unchecked)
            self.ui.listWidget_2.addItem(list_item)

    def save_project(self):
        # 如果已经有保存路径，则直接保存
        if hasattr(self, 'current_file_path') and self.current_file_path:
            file_path = self.current_file_path
        else:
            # 否则弹出对话框选择保存路径
            file_path, _ = QFileDialog.getSaveFileName(self, "保存项目", "",
                                                       "ContourPlot Files (*.ctplot);;All Files (*)")
            if not file_path:  # 如果用户取消保存操作
                return

        try:
            # 更新 project_data 字典
            self.project_data = {
                "project_name": self.windowTitle(),
                "loaded_files": list(self.loaded_data.keys()),
                "filtered_files": list(self.filtered_data.keys()),
                "loaded_data_content": {name: data.to_dict() for name, data in self.loaded_data.items()},
                "filtered_data_content": {name: data.to_dict() for name, data in self.filtered_data.items()},
            }

            # 保存 checkBox 状态
            check_boxes = [
                "checkBox_4", "checkBox", "checkBox_3", "checkBox_2",
                "checkBox_5", "checkBox_6", "checkBox_7"
            ]
            for cb_name in check_boxes:
                self.project_data[cb_name] = getattr(self.ui, cb_name).isChecked()

            # 保存 lineEdit 文本
            line_edits = [
                "lineEdit", "lineEdit_2", "lineEdit_3"
            ]
            for le_name in line_edits:
                self.project_data[le_name] = getattr(self.ui, le_name).text()

            # 保存 comboBox 选中索引
            comboBoxes = ["comboBox", "comboBox_1", "comboBox_2"]
            for combobox in comboBoxes:
                self.project_data[combobox] = getattr(self.ui, combobox).currentIndex()

            # 保存 slider 值
            horizontalSliders = ["horizontalSlider", "horizontalSlider_1", "horizontalSlider_2", "horizontalSlider_3"]
            for horizontal_SL in horizontalSliders:
                self.project_data[horizontal_SL] = getattr(self.ui, horizontal_SL).value()

            # 保存 speed_data 和 profile_data
            if getattr(self, "speed_data", None) is not None and getattr(self, "profile_data", None) is not None:
                self.project_data["speed_data"] = self.speed_data.to_dict()
                self.project_data["profile_data"] = self.profile_data.to_dict()

            # 将项目数据写入文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(self.project_data, file, ensure_ascii=False, indent=4)

            # 保存成功后更新路径和状态
            self.current_file_path = file_path  # 更新当前文件路径
            self.is_saved = True  # 保存后设置为已保存状态
            QMessageBox.information(self, "成功", "项目已成功保存！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存项目时出错：{e}")

    def open_project(self):
        # 检查当前项目是否未保存
        if not getattr(self, "is_saved", True):  # 如果未保存
            reply = QMessageBox.question(
                self,
                "未保存的更改",
                "当前项目有未保存的更改，是否保存？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if reply == QMessageBox.Yes:
                self.save_project()  # 调用保存函数
            elif reply == QMessageBox.Cancel:
                return  # 取消打开操作

        file_path, _ = QFileDialog.getOpenFileName(self, "打开项目", "", "ContourPlot Files (*.ctplot);;All Files (*)")

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.project_data = json.load(file)

                # 记录当前文件路径
                self.current_file_path = file_path

                # 加载文件名列表到 listWidget
                self.update_ui_with_project_data()

                # 还原 loaded_data 和 filtered_data 的内容
                self.loaded_data = {name: pd.DataFrame(data) for name, data in
                                    self.project_data.get("loaded_data_content", {}).items()}
                self.filtered_data = {name: pd.DataFrame(data) for name, data in
                                      self.project_data.get("filtered_data_content", {}).items()}

                # 还原 CheckBox 状态
                check_boxes = [
                    "checkBox", "checkBox_2", "checkBox_3", "checkBox_4", "checkBox_5", "checkBox_6", "checkBox_7"
                ]
                for cb_name in check_boxes:
                    check_state = Qt.Checked if self.project_data.get(cb_name, False) else Qt.Unchecked
                    getattr(self.ui, cb_name).setCheckState(check_state)

                # 还原 Slider 值
                horizontalSliders = ["horizontalSlider", "horizontalSlider_1", "horizontalSlider_2",
                                     "horizontalSlider_3"]
                for horizontal_SL in horizontalSliders:
                    getattr(self.ui, horizontal_SL).setValue(self.project_data.get(horizontal_SL, 0))

                # 还原 LineEdit 文本
                line_edits = [
                    "lineEdit", "lineEdit_2", "lineEdit_3"
                ]
                for le_name in line_edits:
                    getattr(self.ui, le_name).setText(self.project_data.get(le_name, ""))

                # 还原 ComboBox 选中索引
                comboBoxes = ["comboBox", "comboBox_1", "comboBox_2"]
                for combobox in comboBoxes:
                    getattr(self.ui, combobox).setCurrentIndex(self.project_data.get(combobox, 0))

                # 还原 speed_data 和 profile_data
                if "speed_data" in self.project_data and "profile_data" in self.project_data:
                    self.speed_data = pd.DataFrame(self.project_data["speed_data"])
                    self.profile_data = pd.DataFrame(self.project_data["profile_data"])
                    speed_data = self.speed_data
                    profile_data = self.profile_data

                    # 更新绘图
                    self.Data_loading_profile_3D()
                    self.Data_loading_3D()
                    # self.download_data(speed_data, profile_data)

                # 打开新项目后标记为已保存状态
                self.is_saved = True

            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开项目时出错：{e}")

    def closeEvent(self, event):
        # 弹出询问是否保存的对话框
        if self.is_saved:
            # 如果已保存，直接关闭
            event.accept()
        else:
            reply = QMessageBox.question(
                self,
                "保存项目",
                "您要在退出前保存项目吗？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if reply == QMessageBox.Yes:
                # 如果用户选择保存，调用保存项目的方法
                self.save_project()
                event.accept()  # 允许关闭窗口
            elif reply == QMessageBox.No:
                event.accept()  # 不保存直接关闭窗口
            else:
                event.ignore()  # 取消关闭操作，保持软件运行

    def modify_project_data(self):
        self.is_saved = False

    def new_project(self):
        """新建项目，重新打开程序实例"""
        # 询问用户是否确认新建项目
        reply = QMessageBox.question(
            self,
            "新建项目",
            "即将关闭当前项目并创建新项目，您要继续吗？",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            reply = QMessageBox.question(
                self,
                "保存项目",
                "请问要保存当前项目吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.save_project()

            # 重新启动当前程序
            self.restart_application()

    def restart_application(self):
        """重新启动程序"""
        try:
            # 获取当前执行的 Python 文件路径
            current_file = sys.argv[0]
            # 使用 subprocess 重新启动程序
            subprocess.Popen([sys.executable, current_file])
        except Exception as e:
            QMessageBox.critical(self, "错误", f"无法重新启动程序：{e}")
        finally:
            # 退出当前程序
            sys.exit()

    def switch_profile(self, direction):
        """
        切换剖面
        :param direction: 方向，-1表示上一个，1表示下一个
        """
        current_index = self.ui.comboBox_2.currentIndex()
        total_items = self.ui.comboBox_2.count()

        if total_items == 0:
            return

        # 计算新的索引
        new_index = (current_index + direction) % total_items

        # 设置新的选中项
        self.ui.comboBox_2.setCurrentIndex(new_index)

    def setup_bottom_toolbar(self):
        # 主页按钮 - Reset original view
        self.ui.btn_home.clicked.connect(self.canvas.toolbar.home)

        # 放大按钮 - Zoom in
        self.ui.btn_enlarge.clicked.connect(lambda: self.canvas.toolbar.zoom())

        # 缩小按钮 - Zoom out
        self.ui.btn_narrow.clicked.connect(lambda: self.canvas.toolbar.zoom(False))

        # 移动按钮 - Pan
        self.ui.btn_fullscreen.clicked.connect(self.canvas.toolbar.pan)

        # 设置按钮 - Edit parameters
        self.ui.btn_curve.clicked.connect(self.canvas.toolbar.edit_parameters)

        # 文件按钮 - Save
        self.ui.btn_file.clicked.connect(self.export_figures)

        self.ui.btn_back.clicked.connect(self.canvas.toolbar.back)

        # 连接比例尺
        self.ui.scale_combo.currentTextChanged.connect(self.update_scale)

        # 连接纵轴比例调整
        self.ui.aspect_ratio_input.textChanged.connect(self.update_aspect_ratio)
        # 添加鼠标滚轮事件
        self.ui.aspect_ratio_input.wheelEvent = self.handle_aspect_ratio_wheel

    def toggle_fullscreen(self):
        if self.ui.tab_4.isFullScreen():
            self.ui.tab_4.showNormal()
        else:
            self.ui.tab_4.showFullScreen()

    def update_scale(self, scale_text):
        try:
            # 提取比例数值
            scale = float(scale_text.split(':')[1])

            # 创建比例尺图像
            scale_bar_width = 200  # 固定宽度
            scale_bar_height = 40  # 固定高度
            scale_image = QPixmap(scale_bar_width, scale_bar_height)
            scale_image.fill(Qt.transparent)

            painter = QPainter(scale_image)
            painter.setRenderHint(QPainter.Antialiasing)

            # 设置字体
            font = QFont("Microsoft YaHei", 9)
            painter.setFont(font)

            # 绘制比例尺线
            pen = QPen(Qt.black, 2)
            painter.setPen(pen)

            # 计算比例尺实际表示的距离和位置
            real_distance = 100  # 米
            bar_length = 150  # 像素
            y = scale_bar_height - 15

            # 绘制水平线
            painter.drawLine(20, y, 20 + bar_length, y)

            # 绘制刻度
            painter.drawLine(20, y - 5, 20, y + 5)  # 左刻度
            painter.drawLine(20 + bar_length, y - 5, 20 + bar_length, y + 5)  # 右刻度

            # 添加文字说明
            # 实际距离
            distance_text = f"{real_distance}m"
            distance_rect = painter.fontMetrics().boundingRect(distance_text)
            painter.drawText(
                20 + (bar_length - distance_rect.width()) // 2,  # 水平居中
                y - 4,  # 位于线条上方
                distance_text
            )

            # 比例
            scale_text = f"1:{int(scale)}"
            scale_rect = painter.fontMetrics().boundingRect(scale_text)
            painter.drawText(
                20 + (bar_length - scale_rect.width()) // 2,  # 水平居中
                y + 10,  # 位于线条下方
                scale_text
            )

            painter.end()

            # 更新标签
            self.scale_bar_label.setPixmap(scale_image)
            # 确保比例尺在最上层
            self.scale_bar_label.raise_()

        except Exception as e:
            QMessageBox.warning(self, "错误", f"更新比例尺时出错: {str(e)}")

    def on_widget_3_resize(self, event):
        """处理tab_4大小变化事件"""
        if hasattr(self, 'scale_bar_label'):
            self.scale_bar_label.setGeometry(
                20,
                self.ui.widget_3.height() - 60,
                200,
                40
            )
            # 确保比例尺在最上层
            self.scale_bar_label.raise_()
        event.accept()

    def update_aspect_ratio(self, value):
        try:
            ratio = float(value)
            if ratio <= 0:
                return

            # 更新图表的纵横比
            self.ax.set_aspect(ratio)
            self.canvas.draw()

        except ValueError:
            return

    def handle_aspect_ratio_wheel(self, event):
        try:
            current_ratio = float(self.ui.aspect_ratio_input.text())
            delta = event.angleDelta().y()

            # 根据滚轮方向调整比例
            if delta > 0:
                new_ratio = current_ratio + 0.1
            else:
                new_ratio = max(0.1, current_ratio - 0.1)
            # 格式化为两位小数
            self.ui.aspect_ratio_input.setText(f"{new_ratio:.2f}")

        except ValueError:
            return

    def sync_tabs(self, index):
        # 当 tab_widget1 的当前索引发生变化时，更新 tab_widget2 的当前索引，反之亦然
        sender = self.sender()
        if sender == self.ui.tabWidget_2:
            self.ui.tabWidget.setCurrentIndex(index)
        elif sender == self.ui.tabWidget:
            self.ui.tabWidget_2.setCurrentIndex(index)

    def toggle_tabs(self):
        # 获取 tabWidget_2 中当前选中的 tab 的索引
        current_tab_2 = self.ui.tabWidget_2.currentIndex()

        # 如果选中了 tab_3 (索引可能是 2)
        if current_tab_2 == 0:
            self.ui.tab_6.setVisible(True)  # 显示 tab_5
            self.ui.tab.setVisible(False)  # 隐藏 tab
        # 如果选中了 tab_4 (索引可能是 3)
        elif current_tab_2 == 1:
            self.ui.tab_6.setVisible(False)  # 隐藏 tab_5
            self.ui.tab.setVisible(True)  # 显示 tab