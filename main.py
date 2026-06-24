# main.py

import sys

print(sys.executable)
print(sys.version)


import sys
import os
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from utils.logger_config import logger

# 如果使用 PyInstaller 的 --splash 参数，启动时会自动设置 PYI_SPLASH 环境变量
try:
    from pyi_splash import update_text, close
except ImportError:
    update_text = None
    close = None

def main():
    logger.info("-------------Starting the application-------------")

    # 检查是否有启动页面
    if os.getenv("PYI_SPLASH"):
        logger.info("Splash screen is displayed.")
        # 可选：更新启动页面的文字
        if update_text:
            update_text("Loading... Initializing the application.")

    app = QApplication(sys.argv)
    window = MainWindow()

    # 主窗口加载完成
    logger.info("Showing the main window ······")
    window.showMaximized()

    # 关闭启动页面
    if close:
        logger.info("Closing the splash screen.")
        close()

    # 启动主程序事件循环
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
