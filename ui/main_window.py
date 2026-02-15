from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QWidget

from ui.canvas_widget import CanvasWidget
from ui.sidebar_widget import SidebarWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphical Editor")
        self.setMinimumSize(1200, 800)

        self.settings = QSettings("BSUIR", "GraphicsEditor")

        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.canvas = CanvasWidget()

        self.sidebar = SidebarWidget(self.canvas)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.canvas, stretch=1)

    def closeEvent(self, a0):
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(a0)
