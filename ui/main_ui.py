from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, QFile, QEvent)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDockWidget,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout, QToolBox,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QStatusBar, QTabWidget, QToolBar,
    QVBoxLayout, QWidget, QToolButton)
from utils.logger_config import logger
from ui.assets.img import icons_rc
from ui.assets import logo_rc
from ui.assets import styles_rc


class Ui_MainWindow(object):
    def __init__(self):
        self.toggle = True
        self.is_maximized = False

    def setupUi(self, MainWindow):
        # 加载bdQSS样式表
        try:
            file = QFile(":/main.qss") # 或者使用 ":/main.qss"
            file.open(QFile.ReadOnly | QFile.Text)
            stream = file.readAll()
            MainWindow.setStyleSheet(str(stream, encoding='utf-8'))
            file.close()
        except Exception as e:
            logger.info(f"加载RC样式表失败: {str(e)}")
        # 设置应用程序的默认调色板为亮色模式
        QApplication.setPalette(QApplication.style().standardPalette())

        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1200, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/图标/logo/app_logo.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)

        # ========================= 移除默认边框 =========================
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)

        # ========================= 菜单栏动作 =========================
        # 文件菜单
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon1 = QIcon()
        icon1.addFile(u":/menu/m-openProject.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionOpen.setIcon(icon1)

        self.actionCreat_New = QAction(MainWindow)
        self.actionCreat_New.setObjectName(u"actionCreat_New")
        icon2 = QIcon()
        icon2.addFile(u":/menu/m-new.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionCreat_New.setIcon(icon2)

        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        icon3 = QIcon()
        icon3.addFile(u":/menu/m-inputData.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionImport.setIcon(icon3)

        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon4 = QIcon()
        icon4.addFile(u":/menu/m-saveProject.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSave.setIcon(icon4)

        self.actionExport_figures = QAction(MainWindow)
        self.actionExport_figures.setObjectName(u"actionExport_figures")
        icon8 = QIcon()
        icon8.addFile(u":/menu/m-exportImg.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionExport_figures.setIcon(icon8)

        # 绘图菜单
        self.actionContour = QAction(MainWindow)
        self.actionContour.setObjectName(u"actionContour")
        icon5 = QIcon()
        icon5.addFile(u":/menu/m-generateContourMaps.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionContour.setIcon(icon5)

        self.action3DPlot = QAction(MainWindow)
        self.action3DPlot.setObjectName(u"action3DPlot")
        icon7 = QIcon()
        icon7.addFile(u":/menu/m-generate3dMaps.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.action3DPlot.setIcon(icon7)

        self.actionborehole = QAction(MainWindow)
        self.actionborehole.setObjectName(u"actionborehole")
        icon6 = QIcon()
        icon6.addFile(u":/menu/m-drillingProjection.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionborehole.setIcon(icon6)

        # 窗口菜单
        self.actionShowdock = QAction(MainWindow)
        self.actionShowdock.setObjectName(u"actionShowdock")

        # ========================= 主窗口布局 =========================
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # ========================= 主显示区域 =========================
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        # ========================= 主显示区域 - TabWidget =========================
        self.tabWidget_2 = QTabWidget(self.widget)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        # ========================= 主显示区域 - TabWidget - 3D Tab =========================
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_7 = QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tabWidget_2.addTab(self.tab_3, "")

        self.widget_5 = QWidget()
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_w5 = QVBoxLayout(self.widget_5)
        self.verticalLayout_w5.setObjectName(u"verticalLayout_w5")
        self.verticalLayout_7.addWidget(self.widget_5)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 10)

        # ========================= 主显示区域 - TabWidget - 3D - 底部工具栏 =========================
        self.bottom_toolbar_1 = QWidget(self.tab_3)
        self.bottom_toolbar_1.setObjectName("bottom_toolbar")
        self.bottom_toolbar_1.setMaximumHeight(50)

        self.bottom_toolbar_1.setStyleSheet("background-color: #F5F5F5;")

        # 创建水平布局
        self.bottom_toolbar_1_layout = QHBoxLayout(self.bottom_toolbar_1)
        self.bottom_toolbar_1_layout.setContentsMargins(10, 0, 10, 0)
        self.bottom_toolbar_1_layout.setSpacing(10)

        self.verticalLayout_7.addWidget(self.bottom_toolbar_1)

        # 添加home_view按钮
        self.btn_home_view = QToolButton(self.bottom_toolbar_1)
        self.btn_home_view.setIcon(QIcon(":/down/b-homePage@2x.png"))
        self.btn_home_view.setToolTip("home_view")
        self.bottom_toolbar_1_layout.addWidget(self.btn_home_view)
        self.btn_home_view.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加front_view按钮
        self.btn_front_veiw = QToolButton(self.bottom_toolbar_1)
        self.btn_front_veiw.setIcon(QIcon(":/down/from-front.png"))
        self.btn_front_veiw.setToolTip("front_view")
        self.bottom_toolbar_1_layout.addWidget(self.btn_front_veiw)
        self.btn_front_veiw.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加left_view按钮
        self.btn_left_veiw = QToolButton(self.bottom_toolbar_1)
        self.btn_left_veiw.setIcon(QIcon(":/down/from-left.png"))
        self.btn_left_veiw.setToolTip("front_view")
        self.bottom_toolbar_1_layout.addWidget(self.btn_left_veiw)
        self.btn_left_veiw.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加up_view按钮
        self.btn_up_veiw = QToolButton(self.bottom_toolbar_1)
        self.btn_up_veiw.setIcon(QIcon(":/down/from-up.png"))
        self.btn_up_veiw.setToolTip("front_view")
        self.bottom_toolbar_1_layout.addWidget(self.btn_up_veiw)
        self.btn_up_veiw.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加分隔线
        line_2 = QFrame(self.bottom_toolbar_1)
        line_2.setFrameShape(QFrame.VLine)
        line_2.setFrameShadow(QFrame.Sunken)
        line_2.setStyleSheet("background-color: #DCDCDC;")
        self.bottom_toolbar_1_layout.addWidget(line_2)

        # 填充颜色
        self.comboBox_1 = QComboBox(self.bottom_toolbar_1)
        icon9 = QIcon()
        icon9.addFile(u":/颜色映射/figure source/jet.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox_1.addItem(icon9, "")
        icon10 = QIcon()
        icon10.addFile(u":/颜色映射/figure source/rainbow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox_1.addItem(icon10, "")
        icon11 = QIcon()
        icon11.addFile(u":/颜色映射/figure source/cool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox_1.addItem(icon11, "")
        icon12 = QIcon()
        icon12.addFile(u":/颜色映射/figure source/hot.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox_1.addItem(icon12, "")
        self.comboBox_1.setObjectName(u"comboBox_1")
        self.comboBox_1.setMaximumSize(QSize(16777215, 25))
        self.comboBox_1.setIconSize(QSize(40, 20))
        self.bottom_toolbar_1_layout.addWidget(self.comboBox_1)

        self.comboBox_1.setStyleSheet("""
            QComboBox QAbstractItemView::item:hover {
                margin-left: 10px; /* 鼠标悬停时向右偏移 */
                background: lightgray; /* 悬停高亮背景 */
            }                       
        """
        )

        # 添加弹簧
        self.bottom_toolbar_1_layout.addStretch()


        # ========================= 主显示区域 - TabWidget - 剖面 Tab =========================
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_6 = QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.widget_3 = QWidget(self.tab_4)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_w3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_w3.setObjectName(u"verticalLayout_w3")
        self.verticalLayout_6.addWidget(self.widget_3)

        self.verticalLayout_6.setStretch(0, 1)
        self.verticalLayout_6.setStretch(1, 10)

        self.verticalLayout_4.addWidget(self.tabWidget_2)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        MainWindow.setCentralWidget(self.centralwidget)

        # ========================= 主显示区域 - TabWidget - 剖面 - 底部工具栏 =========================
        self.bottom_toolbar = QWidget(self.tab_4)
        self.bottom_toolbar.setObjectName("bottom_toolbar")
        self.bottom_toolbar.setMaximumHeight(50)

        self.bottom_toolbar.setStyleSheet("background-color: #F5F5F5;")

        # 创建水平布局
        self.bottom_toolbar_layout = QHBoxLayout(self.bottom_toolbar)
        self.bottom_toolbar_layout.setContentsMargins(10, 0, 10, 0)
        self.bottom_toolbar_layout.setSpacing(10)

        # 添加“上一个”工具按钮
        self.btn_zoom_in = QToolButton(self.bottom_toolbar)
        self.btn_zoom_in.setIcon(QIcon(":/down/b-left.png"))
        self.btn_zoom_in.setToolTip("上一个")
        self.bottom_toolbar_layout.addWidget(self.btn_zoom_in)

        self.btn_zoom_in.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 剖面选择
        self.comboBox_2 = QComboBox(self.bottom_toolbar)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.setMinimumWidth(120)
        self.comboBox_2.setMaximumWidth(200)
        self.bottom_toolbar_layout.addWidget(self.comboBox_2)

        # 添加“下一个”工具按钮
        self.btn_zoom_out = QToolButton(self.bottom_toolbar)
        self.btn_zoom_out.setIcon(QIcon(":/down/b-right.png"))
        self.btn_zoom_out.setToolTip("下一个")
        self.bottom_toolbar_layout.addWidget(self.btn_zoom_out)
        self.btn_zoom_out.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加分隔线
        line = QFrame(self.bottom_toolbar)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("background-color: #DCDCDC;")
        self.bottom_toolbar_layout.addWidget(line)

        # 添加主页按钮
        self.btn_home = QToolButton(self.bottom_toolbar)
        self.btn_home.setIcon(QIcon(":/down/b-homePage@2x.png"))
        self.btn_home.setToolTip("主页")
        self.bottom_toolbar_layout.addWidget(self.btn_home)
        self.btn_home.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加放大按钮
        self.btn_enlarge = QToolButton(self.bottom_toolbar)
        self.btn_enlarge.setIcon(QIcon(":/down/b-enlarge@2x.png"))
        self.btn_enlarge.setToolTip("放大")
        self.bottom_toolbar_layout.addWidget(self.btn_enlarge)
        self.btn_enlarge.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加缩小按钮
        self.btn_narrow = QToolButton(self.bottom_toolbar)
        self.btn_narrow.setIcon(QIcon(":/down/b-narrow@2x.png"))
        self.btn_narrow.setToolTip("缩小")
        self.bottom_toolbar_layout.addWidget(self.btn_narrow)
        self.btn_narrow.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加移动按钮
        self.btn_fullscreen = QToolButton(self.bottom_toolbar)
        self.btn_fullscreen.setIcon(QIcon(":/down/b-fullScreen@2x.png"))
        self.btn_fullscreen.setToolTip("移动")
        self.bottom_toolbar_layout.addWidget(self.btn_fullscreen)
        self.btn_fullscreen.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加设置按钮
        self.btn_curve = QToolButton(self.bottom_toolbar)
        self.btn_curve.setIcon(QIcon(":/down/b-curve@2x.png"))
        self.btn_curve.setToolTip("设置")
        self.bottom_toolbar_layout.addWidget(self.btn_curve)
        self.btn_curve.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加保存图片按钮
        self.btn_file = QToolButton(self.bottom_toolbar)
        self.btn_file.setIcon(QIcon(":/down/b-file@2x.png"))
        self.btn_file.setToolTip("保存图片")
        self.bottom_toolbar_layout.addWidget(self.btn_file)
        self.btn_file.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;  
                    }
                """)

        # 添加分隔线
        line2 = QFrame(self.bottom_toolbar)
        line2.setFrameShape(QFrame.VLine)
        line2.setFrameShadow(QFrame.Sunken)
        line2.setStyleSheet("background-color: #DCDCDC;")
        self.bottom_toolbar_layout.addWidget(line2)

        # 填充颜色
        self.comboBox = QComboBox(self.bottom_toolbar)
        icon9 = QIcon()
        icon9.addFile(u":/颜色映射/figure source/jet.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox.addItem(icon9, "")
        icon10 = QIcon()
        icon10.addFile(u":/颜色映射/figure source/rainbow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox.addItem(icon10, "")
        icon11 = QIcon()
        icon11.addFile(u":/颜色映射/figure source/cool.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox.addItem(icon11, "")
        icon12 = QIcon()
        icon12.addFile(u":/颜色映射/figure source/hot.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.comboBox.addItem(icon12, "")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMaximumSize(QSize(16777215, 25))
        self.comboBox.setIconSize(QSize(40, 20))
        self.bottom_toolbar_layout.addWidget(self.comboBox)
        
        # Z标尺
        self.btn_ruler = QToolButton(self.bottom_toolbar)
        self.btn_ruler.setIcon(QIcon(":/down/b-Z@2x.png"))
        self.btn_ruler.setToolTip("横纵比例")
        self.bottom_toolbar_layout.addWidget(self.btn_ruler)
        self.btn_ruler.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 添加纵轴比例输入框
        self.aspect_ratio_input = QLineEdit(self.bottom_toolbar)
        self.aspect_ratio_input.setFixedWidth(60)
        self.aspect_ratio_input.setText("1.00")
        self.aspect_ratio_input.setAlignment(Qt.AlignCenter)
        self.bottom_toolbar_layout.addWidget(self.aspect_ratio_input)

        # 返回
        self.btn_back = QToolButton(self.bottom_toolbar)
        self.btn_back.setIcon(QIcon(":/down/b-back@2x.png"))
        self.btn_back.setToolTip("返回")
        self.bottom_toolbar_layout.addWidget(self.btn_back)
        self.btn_back.setStyleSheet("""                   
                    QToolButton:hover {
                        background-color: #DCDCDC;
                    }
                """)

        # 比例尺
        self.scale_combo = QComboBox(self.bottom_toolbar)
        self.scale_combo.setObjectName("scale_combo")
        self.scale_combo.addItems(["1:100.00", "1:200.00", "1:500.00", "1:1000.00", "1:2000.00", "1:5000.00"])
        self.scale_combo.setCurrentText('1:1000.00')  # 设置默认比例

        self.bottom_toolbar_layout.addWidget(self.scale_combo)

        # 添加弹簧
        self.bottom_toolbar_layout.addStretch()

        # 将底部工具栏添加到主布局
        self.verticalLayout_6.addWidget(self.bottom_toolbar)

        # ========================= 主显示区域 - 工具栏空间 =========================
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget)

        # ========================= 菜单栏 =========================
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 46))

        # 添加 logo 到菜单栏最左侧
        logoLabel = QLabel(self.menubar)
        logoPixmap = QPixmap(":/window/w-logo.png")
        logoLabel.setPixmap(logoPixmap.scaled(153, 21, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logoLabel.setFixedSize(173, 21)
        logoLabel.setContentsMargins(20, 0, 0, 0)
        # 将 logo 添加为第一个部件
        self.menubar.setCornerWidget(logoLabel, Qt.TopLeftCorner)

        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuWindow = QMenu(self.menubar)
        self.menuWindow.setObjectName(u"menuWindow")
        self.menuPlot = QMenu(self.menubar)
        self.menuPlot.setObjectName(u"menuPlot")
        MainWindow.setMenuBar(self.menubar)

        # ========================= 自定义标题栏按钮 =========================
        # 创建一个容器来放置标题栏按钮
        titleBarWidget = QWidget(self.menubar)
        titleBarLayout = QHBoxLayout(titleBarWidget)
        titleBarLayout.setContentsMargins(0, 0, 0, 0)
        titleBarLayout.setSpacing(5)

        # 最小化按钮
        self.btn_minimize = QPushButton(titleBarWidget)
        self.btn_minimize.setObjectName("btn_minimize")
        self.btn_minimize.setIcon(QIcon(":/window/w-minimize.png"))  # 替换为你的最小化图标路径
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)

        # 最大化/还原按钮
        self.btn_maximize = QPushButton(titleBarWidget)
        self.btn_maximize.setObjectName("btn_maximize")
        self.btn_maximize.setIcon(QIcon(":/window/w-maximize.png"))
        self.btn_maximize.setFixedSize(30, 30)
        self.btn_maximize.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)

        # 关闭按钮
        self.btn_close = QPushButton(titleBarWidget)
        self.btn_close.setObjectName("btn_close")
        self.btn_close.setIcon(QIcon(":/window/w-close.png"))  # 替换为你的关闭图标路径
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: #FF5C5C;
            }
        """)

        # 将按钮添加到布局中
        titleBarLayout.addWidget(self.btn_minimize)
        titleBarLayout.addWidget(self.btn_maximize)
        titleBarLayout.addWidget(self.btn_close)

        # 将自定义标题栏按钮添加到菜单栏的右上角
        self.menubar.setCornerWidget(titleBarWidget, Qt.TopRightCorner)

        # ========================= 工具栏 =========================
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setIconSize(QSize(24, 24))
        self.toolBar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        # 创建主容器
        mainWidget = QWidget()
        mainLayout = QHBoxLayout(mainWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # 创建按钮容器
        buttonWidget = QWidget()
        buttonLayout = QHBoxLayout(buttonWidget)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(2)

        # 将 QAction 转换为 QToolButton 添加到布局中
        for action in [self.actionOpen, self.actionCreat_New, self.actionImport, 
                      self.actionExport_figures, self.actionSave, self.actionContour, 
                      self.action3DPlot, self.actionborehole]:
            button = QToolButton()
            button.setDefaultAction(action)
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            button.setIconSize(QSize(24, 24))
            buttonLayout.addWidget(button)

        # 添加按钮容器到主布局
        mainLayout.addWidget(buttonWidget)
        
        # 添加弹簧
        mainLayout.addStretch()

        # 创建logo
        # logoLabel = QLabel()
        # logoPixmap = QPixmap(":/menu/SGEEG-logo.png")
        # logoLabel.setPixmap(logoPixmap.scaled(160, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # logoLabel.setFixedSize(180, 40)
        # logoLabel.setContentsMargins(0, 0, 20, 0)
        
        # 添加logo到主布局
        # mainLayout.addWidget(logoLabel)

        # 将主容器添加到工具栏
        self.toolBar.addWidget(mainWidget)
        
        # 设置工具栏不可移动
        self.toolBar.setMovable(False)

        # ========================= 状态栏 =========================
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # ========================= 左侧停靠窗口 - 数据（原始数据 & 处理数据） =========================
        self.dockWidget = QDockWidget(MainWindow)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy1)
        self.dockWidget.setMinimumSize(QSize(200, 215))
        self.dockWidget.setMaximumSize(QSize(200, 400))
        self.dockWidget.setFloating(False)

        # 创建用于显示两个Tab的QTabWidget
        self.dataTabWidget = QTabWidget(self.dockWidget)
        self.dataTabWidget.setObjectName(u"dataTabWidget")

        # 原始数据Tab
        self.raw_data_tab = QWidget()
        self.raw_data_tab.setObjectName(u"raw_data_tab")
        self.verticalLayout_raw = QVBoxLayout(self.raw_data_tab)
        self.verticalLayout_raw.setSpacing(0)
        self.verticalLayout_raw.setContentsMargins(0, 0, 0, 0)
        self.listWidget = QListWidget(self.raw_data_tab)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy2)
        self.listWidget.setMaximumSize(QSize(131500, 55000))
        self.verticalLayout_raw.addWidget(self.listWidget)
        self.dataTabWidget.addTab(self.raw_data_tab, QCoreApplication.translate("MainWindow", "原始数据", None))

        # 处理数据Tab（将原先tab_2中的内容移到这里）
        self.processed_data_tab = QWidget()
        self.processed_data_tab.setObjectName(u"processed_data_tab")
        self.verticalLayout_processed = QVBoxLayout(self.processed_data_tab)
        self.verticalLayout_processed.setSpacing(0)
        self.verticalLayout_processed.setContentsMargins(0, 0, 0, 0)
        self.listWidget_2 = QListWidget(self.processed_data_tab)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.verticalLayout_processed.addWidget(self.listWidget_2)

        self.widget_4 = QWidget(self.processed_data_tab)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_2 = QPushButton(self.widget_4)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QPushButton(self.widget_4)
        self.pushButton.setObjectName(u"pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_processed.addWidget(self.widget_4)

        self.dataTabWidget.addTab(self.processed_data_tab, QCoreApplication.translate("MainWindow", "处理数据", None))

        # 将 dataTabWidget 作为 dockWidget 的主组件
        dockWidgetContents = QWidget()
        dockWidgetLayout = QVBoxLayout(dockWidgetContents)
        dockWidgetLayout.setSpacing(0)
        dockWidgetLayout.setContentsMargins(0, 0, 0, 0)
        dockWidgetLayout.addWidget(self.dataTabWidget)
        self.dockWidget.setWidget(dockWidgetContents)

        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget)

        # ========================= 左侧停靠窗口 - 设置 =========================
        self.dockWidget_2 = QDockWidget(MainWindow)
        self.dockWidget_2.setObjectName(u"dockWidget_2")
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.dockWidgetContents_2)
        self.tabWidget.setObjectName(u"tabWidget")

        # ========================= 左侧停靠窗口 - 设置 - 3D Tab =========================
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_tab_6 = QVBoxLayout(self.tab_6)
        self.verticalLayout_tab_6.setObjectName(u"verticalLayout_tab_6")
        # self.verticalLayout_tab_6.setContentsMargins(0, 0, 0, 0)
        self.tabWidget.addTab(self.tab_6, "3D")

        # toolbox
        self.toolBox = QToolBox(self.tab_6)
        self.toolBox.setObjectName(u"toolBox")
        self.verticalLayout_tab_6.addWidget(self.toolBox)

        #散点
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.toolBox.addItem(self.page, u"散点")
        self.page.setGeometry(QRect(0, 0, 194, 194))
        self.formLayout_3 = QFormLayout(self.page)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_18 = QLabel(self.page)
        self.label_18.setObjectName(u"label_18")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)
        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.label_18)
        self.checkBox_16 = QCheckBox(self.page)
        self.checkBox_16.setObjectName(u"checkBox_16")
        sizePolicy1.setHeightForWidth(self.checkBox_16.sizePolicy().hasHeightForWidth())
        self.checkBox_16.setSizePolicy(sizePolicy1)
        self.checkBox_16.setChecked(True)
        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.checkBox_16)

        # 剖面
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.toolBox.addItem(self.page_2, u"剖面")
        self.verticalLayout_page_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_page_2.setObjectName(u"verticalLayout_page_2")
        self.listWidget_3 = QListWidget(self.page_2)
        self.listWidget_3.setObjectName(u"listWidget_3")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.listWidget_3.sizePolicy().hasHeightForWidth())
        self.listWidget_3.setSizePolicy(sizePolicy5)
        self.verticalLayout_l3 = QVBoxLayout(self.listWidget_3)
        self.verticalLayout_page_2.addWidget(self.listWidget_3)

        # 钻孔
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.toolBox.addItem(self.page_3, u"钻孔")
        self.formLayout_p3 = QFormLayout(self.page_3)
        self.formLayout_p3.setObjectName(u"formLayout_p3")
        self.checkBox_17 = QCheckBox(self.page_3)
        self.checkBox_17.setObjectName(u"checkBox_17")
        sizePolicy1.setHeightForWidth(self.checkBox_17.sizePolicy().hasHeightForWidth())
        self.checkBox_17.setSizePolicy(sizePolicy1)
        self.checkBox_17.setChecked(False)
        self.formLayout_p3.setWidget(0, QFormLayout.LabelRole, self.checkBox_17)
        self.label_19 = QLabel(self.page_3)
        self.label_19.setObjectName(u"label_19")
        self.formLayout_p3.setWidget(0, QFormLayout.FieldRole, self.label_19)
        self.checkBox_18 = QCheckBox(self.page_3)
        self.checkBox_18.setObjectName(u"checkBox_18")
        sizePolicy1.setHeightForWidth(self.checkBox_18.sizePolicy().hasHeightForWidth())
        self.checkBox_18.setSizePolicy(sizePolicy1)
        self.checkBox_18.setChecked(False)
        self.formLayout_p3.setWidget(1, QFormLayout.LabelRole, self.checkBox_18)
        self.label_23 = QLabel(self.page_3)
        self.label_23.setObjectName(u"label_23")
        self.formLayout_p3.setWidget(1, QFormLayout.FieldRole, self.label_23)

        # 切片
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 194, 194))
        self.gridlayout_p4 = QGridLayout(self.page_4)
        self.gridlayout_p4.setObjectName(u"gridlayout_p4")
        self.checkBox_19 = QCheckBox(self.page_4)
        self.checkBox_19.setObjectName(u"checkBox_19")
        sizePolicy1.setHeightForWidth(self.checkBox_19.sizePolicy().hasHeightForWidth())
        self.checkBox_19.setSizePolicy(sizePolicy1)
        self.checkBox_19.setChecked(False)
        self.gridlayout_p4.addWidget(self.checkBox_19, 0, 0, 1, 1)
        self.label_20 = QLabel(self.page_4)
        self.label_20.setObjectName(u"label_20")
        self.gridlayout_p4.addWidget(self.label_20, 0, 1, 1, 1)

        self.horizontalSlider_1 = QSlider(self.page_4)
        self.horizontalSlider_1.setObjectName(u"horizontalSlider_1")
        self.horizontalSlider_1.setMaximum(100)
        self.horizontalSlider_1.setMinimum(0)
        self.horizontalSlider_1.setValue(50)
        self.horizontalSlider_1.setOrientation(Qt.Orientation.Horizontal)
        self.gridlayout_p4.addWidget(self.horizontalSlider_1, 0, 2, 1, 1)

        self.checkBox_20 = QCheckBox(self.page_4)
        self.checkBox_20.setObjectName(u"checkBox_20")
        sizePolicy1.setHeightForWidth(self.checkBox_20.sizePolicy().hasHeightForWidth())
        self.checkBox_20.setSizePolicy(sizePolicy1)
        self.checkBox_20.setChecked(False)
        self.gridlayout_p4.addWidget(self.checkBox_20, 1, 0, 1, 1)

        self.label_21 = QLabel(self.page_4)
        self.label_21.setObjectName(u"label_21")
        self.gridlayout_p4.addWidget(self.label_21, 1, 1, 1, 1)

        self.horizontalSlider_2 = QSlider(self.page_4)
        self.horizontalSlider_2.setObjectName(u"horizontalSlider_2")
        self.horizontalSlider_2.setMaximum(100)
        self.horizontalSlider_2.setMinimum(0)
        self.horizontalSlider_2.setValue(50)
        self.horizontalSlider_2.setOrientation(Qt.Orientation.Horizontal)
        self.gridlayout_p4.addWidget(self.horizontalSlider_2, 1, 2, 1, 1)


        self.checkBox_21 = QCheckBox(self.page_4)
        self.checkBox_21.setObjectName(u"checkBox_21")
        sizePolicy1.setHeightForWidth(self.checkBox_21.sizePolicy().hasHeightForWidth())
        self.checkBox_21.setSizePolicy(sizePolicy1)
        self.checkBox_21.setChecked(False)
        self.gridlayout_p4.addWidget(self.checkBox_21, 2, 0, 1, 1)

        self.label_22 = QLabel(self.page_4)
        self.label_22.setObjectName(u"label_22")
        self.gridlayout_p4.addWidget(self.label_22, 2, 1, 1, 1)

        self.horizontalSlider_3 = QSlider(self.page_4)
        self.horizontalSlider_3.setObjectName(u"horizontalSlider_3")
        self.horizontalSlider_3.setMaximum(100)
        self.horizontalSlider_3.setMinimum(0)
        self.horizontalSlider_3.setValue(50)
        self.horizontalSlider_3.setOrientation(Qt.Orientation.Horizontal)
        self.gridlayout_p4.addWidget(self.horizontalSlider_3, 2, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.gridlayout_p4.addItem(self.verticalSpacer, 3, 2, 1, 1)

        self.toolBox.addItem(self.page_4, u"切片")

        # 等值面
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.formLayout_p5 = QFormLayout(self.page_5)
        self.formLayout_p5.setObjectName(u"formLayout_p5")

        self.lineEdit_3 = QLineEdit(self.page_5)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)

        sizePolicy2.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy2)

        self.lineEdit_3.setMaximumSize(QSize(16777215, 16777215))
        self.lineEdit_3.setMinimumHeight(30)

        self.formLayout_p5.setWidget(0, QFormLayout.SpanningRole, self.lineEdit_3)

        self.pushButton_1 = QPushButton(self.page_5)
        self.pushButton_1.setObjectName(u"pushButton_1")
        self.formLayout_p5.setWidget(1, QFormLayout.LabelRole, self.pushButton_1)

        self.pushButton_3 = QPushButton(self.page_5)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.formLayout_p5.setWidget(1, QFormLayout.FieldRole, self.pushButton_3)

        self.toolBox.addItem(self.page_5, u"等值面")

        # ========================= 左侧停靠窗口 - 设置 - 2D Tab =========================
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_tab = QVBoxLayout(self.tab)
        self.verticalLayout_tab.setObjectName(u"verticalLayout_tab")

        # toolBox_2
        self.toolBox_2 = QToolBox(self.tab)
        self.toolBox_2.setObjectName(u"toolBox_2")
        self.verticalLayout_tab.addWidget(self.toolBox_2)

        # 常见属性
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.toolBox_2.addItem(self.page_6, u"常见属性")
        self.formLayout_p6 = QFormLayout(self.page_6)
        self.formLayout_p6.setObjectName(u"formLayout_p6")

        # 填充
        self.checkBox_2 = QCheckBox(self.page_6)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setMaximumSize(QSize(16777215, 25))
        self.checkBox_2.setChecked(True)
        self.formLayout_p6.setWidget(0, QFormLayout.FieldRole, self.checkBox_2)
        self.label_5 = QLabel(self.page_6)
        self.label_5.setObjectName(u"label_5")
        self.formLayout_p6.setWidget(0, QFormLayout.LabelRole, self.label_5)

        # 显示等值线
        self.label_9 = QLabel(self.page_6)
        self.label_9.setObjectName(u"label_9")
        self.formLayout_p6.setWidget(1, QFormLayout.LabelRole, self.label_9)
        self.checkBox_4 = QCheckBox(self.tab)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setMaximumSize(QSize(16777215, 25))
        self.formLayout_p6.setWidget(1, QFormLayout.FieldRole, self.checkBox_4)

        # 等值线间隔
        self.label_10 = QLabel(self.page_6)
        self.label_10.setObjectName(u"label_10")
        self.formLayout_p6.setWidget(2, QFormLayout.LabelRole, self.label_10)
        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.formLayout_p6.setWidget(2, QFormLayout.FieldRole, self.lineEdit)

        # 平滑
        self.label_13 = QLabel(self.page_6)
        self.label_13.setObjectName(u"label_13")
        self.formLayout_p6.setWidget(3, QFormLayout.LabelRole, self.label_13)
        self.horizontalSlider = QSlider(self.tab)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)
        self.formLayout_p6.setWidget(3, QFormLayout.FieldRole, self.horizontalSlider)

        # 标签
        self.label_4 = QLabel(self.page_6)
        self.label_4.setObjectName(u"label_4")
        self.formLayout_p6.setWidget(4, QFormLayout.LabelRole, self.label_4)
        self.checkBox = QCheckBox(self.tab)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMaximumSize(QSize(16777215, 25))
        self.formLayout_p6.setWidget(4, QFormLayout.FieldRole, self.checkBox)

        # 色卡
        self.label_7 = QLabel(self.page_6)
        self.label_7.setObjectName(u"label_7")
        self.formLayout_p6.setWidget(5, QFormLayout.LabelRole, self.label_7)
        self.checkBox_3 = QCheckBox(self.tab)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setMaximumSize(QSize(16777215, 25))
        self.formLayout_p6.setWidget(5, QFormLayout.FieldRole, self.checkBox_3)

        # 采集点
        self.label_12 = QLabel(self.page_6)
        self.label_12.setObjectName(u"label_12")
        self.formLayout_p6.setWidget(6, QFormLayout.LabelRole, self.label_12)
        self.checkBox_5 = QCheckBox(self.tab)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setMaximumSize(QSize(16777215, 25))
        self.formLayout_p6.setWidget(6, QFormLayout.FieldRole, self.checkBox_5)

        # 钻孔
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.toolBox_2.addItem(self.page_7, u"钻孔")
        self.formLayout_p7 = QFormLayout(self.page_7)
        self.formLayout_p7.setObjectName(u"formLayout_p6")

        # 钻孔投影
        self.label_15 = QLabel(self.page_7)
        self.label_15.setObjectName(u"label_15")
        self.formLayout_p7.setWidget(0, QFormLayout.LabelRole, self.label_15)
        self.checkBox_6 = QCheckBox(self.tab)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setMaximumSize(QSize(16777215, 25))
        self.checkBox_6.setChecked(False)
        self.formLayout_p7.setWidget(0, QFormLayout.FieldRole, self.checkBox_6)

        # 钻孔名
        self.checkBox_7 = QCheckBox(self.page_7)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setMaximumSize(QSize(16777215, 25))
        self.checkBox_7.setChecked(False)
        self.formLayout_p7.setWidget(1, QFormLayout.FieldRole, self.checkBox_7)
        self.label_17 = QLabel(self.tab)
        self.label_17.setObjectName(u"label_17")
        self.formLayout_p7.setWidget(1, QFormLayout.LabelRole, self.label_17)
        self.tabWidget.addTab(self.tab, "")

        # 钻孔投影距离
        self.label_14 = QLabel(self.page_7)
        self.label_14.setObjectName(u"label_14")
        self.formLayout_p7.setWidget(2, QFormLayout.LabelRole, self.label_14)
        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.formLayout_p7.setWidget(2, QFormLayout.FieldRole, self.lineEdit_2)

        # ========================= 显示属性 =========================
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockWidget_2)

        # ========================= 连接菜单动作和工具栏动作 =========================
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuPlot.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionCreat_New)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExport_figures)
        self.menuWindow.addAction(self.actionShowdock)
        self.menuPlot.addAction(self.actionContour)
        self.menuPlot.addAction(self.action3DPlot)
        self.menuPlot.addAction(self.actionborehole)
        # ========================= 连接标题栏按钮的信号 =========================
        self.btn_minimize.clicked.connect(MainWindow.showMinimized)
        self.btn_maximize.clicked.connect(lambda: self.toggle_maximize(MainWindow))
        self.btn_close.clicked.connect(MainWindow.close)

        self.retranslateUi(MainWindow)

        self.tabWidget_2.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(1)
        self.toolBox.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

        # 在创建menubar后添加以下代码
        class MenuBarFilter(QObject):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.moving = False
                self.offset = None
                
            def eventFilter(self, obj, event):
                if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.LeftButton:
                    self.moving = True
                    self.offset = event.globalPos() - MainWindow.pos()
                    return True
                elif event.type() == QEvent.Type.MouseMove and self.moving:
                    MainWindow.move(event.globalPos() - self.offset)
                    return True
                elif event.type() == QEvent.Type.MouseButtonRelease:
                    self.moving = False
                    return True
                return super().eventFilter(obj, event)
        
        # 安装事件过滤器到菜单栏
        self.menu_filter = MenuBarFilter(self.menubar)
        self.menubar.installEventFilter(self.menu_filter)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "等值线生成工具", None))
        # ========================= 菜单栏翻译 =========================
        # 文件菜单
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", "打开项目", None))
        self.actionCreat_New.setText(QCoreApplication.translate("MainWindow", "新建项目", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", "导入数据", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", "保存项目", None))
        self.actionExport_figures.setText(QCoreApplication.translate("MainWindow", "导出图片", None))
        # 绘图菜单
        self.actionContour.setText(QCoreApplication.translate("MainWindow", "生成等值线图", None))
        self.action3DPlot.setText(QCoreApplication.translate("MainWindow", "生成三维图形", None))
        self.actionborehole.setText(QCoreApplication.translate("MainWindow", "钻孔投影", None))
        # 窗口菜单
        self.actionShowdock.setText(QCoreApplication.translate("MainWindow", "显示侧边栏", None))

        # ========================= 主显示区域翻译 =========================
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"3D", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", "剖面", None))

        # ========================= 菜单栏菜单标题翻译 =========================
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "文件", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "编辑", None))
        self.menuWindow.setTitle(QCoreApplication.translate("MainWindow", "窗口", None))
        self.menuPlot.setTitle(QCoreApplication.translate("MainWindow", "绘图", None))

        # ========================= 工具栏翻译 =========================
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", "toolBar", None))

        # ========================= 左侧停靠窗口标题翻译 =========================
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MainWindow", "数据", None))
        self.dockWidget_2.setWindowTitle(QCoreApplication.translate("MainWindow", "设置", None))

        # ========================= 左侧停靠窗口 - 设置 - 3D Tab 翻译 =========================
        self.label_18.setText(QCoreApplication.translate("MainWindow", "散点", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", "钻孔", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", "X切片", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", "Y切片", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", "Z切片", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", "钻孔名", None))
        self.pushButton_1.setText(QCoreApplication.translate("MainWindow", "生成等值面", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", "删除等值面", None))

        # ========================= 左侧停靠窗口 - 设置 - 属性 Tab 翻译 =========================
        # 显示等值线
        self.label_9.setText(QCoreApplication.translate("MainWindow", "显示等值线", None))
        self.checkBox_4.setText("")
        # 平滑
        self.label_13.setText(QCoreApplication.translate("MainWindow", "平滑", None))
        # 等值线间隔
        self.label_10.setText(QCoreApplication.translate("MainWindow", "等值线间隔", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", "100", None))
        # 标签
        self.label_4.setText(QCoreApplication.translate("MainWindow", "标签", None))
        self.checkBox.setText("")
        # 色卡
        self.label_7.setText(QCoreApplication.translate("MainWindow", "色卡", None))
        self.checkBox_3.setText("")
        # 填充
        self.label_5.setText(QCoreApplication.translate("MainWindow", "填充", None))
        self.checkBox_2.setText("")
        # 填充颜色
        # self.label_6.setText(QCoreApplication.translate("MainWindow", "填充颜色", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", "彩虹1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", "彩虹2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", "冷色", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("MainWindow", "暖色", None))

        self.comboBox_1.setItemText(0, QCoreApplication.translate("MainWindow", "彩虹1", None))
        self.comboBox_1.setItemText(1, QCoreApplication.translate("MainWindow", "彩虹2", None))
        self.comboBox_1.setItemText(2, QCoreApplication.translate("MainWindow", "冷色", None))
        self.comboBox_1.setItemText(3, QCoreApplication.translate("MainWindow", "暖色", None))

        # 采集点
        self.label_12.setText(QCoreApplication.translate("MainWindow", "采集点", None))
        self.checkBox_5.setText("")
        # 钻孔投影
        self.label_15.setText(QCoreApplication.translate("MainWindow", "钻孔投影", None))
        self.checkBox_6.setText("")
        # 钻孔投影距离
        self.label_14.setText(QCoreApplication.translate("MainWindow", "钻孔投影距离", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", "10000", None))
        self.checkBox_7.setText("")
        # 钻孔名
        self.label_17.setText(QCoreApplication.translate("MainWindow", "钻孔名", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", "属性", None))

        # ========================= 左侧停靠窗口 - 设置 - 数据下载 Tab 翻译 =========================
        # 下载原始数据
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", "下载原始数据", None))
        # 下载处理数据
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.raw_data_tab),
                                      QCoreApplication.translate("MainWindow", "原始数据", None))
        self.dataTabWidget.setTabText(self.dataTabWidget.indexOf(self.processed_data_tab),
                                      QCoreApplication.translate("MainWindow", "处理数据", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "下载处理数据", None))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", "数据下载", None))
    # retranslateUi

    def toggle_maximize(self, MainWindow):
        if MainWindow.isMaximized():
            MainWindow.showNormal()
        else:
            MainWindow.showMaximized()