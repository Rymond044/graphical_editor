from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.canvas_widget import CanvasWidget
from ui.tools.conic_tool import ConicsToolWidget
from ui.tools.curves_tool import CurvesTool
from ui.tools.line_tool import LineTool


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graphics Editor")
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

        self.tool_panel = self._create_tool_panel()
        main_layout.addWidget(self.tool_panel)

        self.canvas = CanvasWidget()
        main_layout.addWidget(self.canvas, stretch=1)

        self.settings_panel = QWidget()
        self.settings_panel.setFixedWidth(280)
        self.settings_layout = QVBoxLayout(self.settings_panel)
        self.settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_layout.setSpacing(0)
        main_layout.addWidget(self.settings_panel)

        self.tools = {}
        self.current_tool = None
        self._register_tools()

        self._activate_tool("line")

    def _create_tool_panel(self):
        panel = QWidget()
        panel.setFixedWidth(80)
        panel.setStyleSheet("background-color: #2d2d2d;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 10, 5, 10)
        layout.setSpacing(5)

        title = QLabel("Tools")
        title.setStyleSheet(
            "color: white; font-size: 11pt; font-weight: bold; padding: 5px;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.tool_button_group = QButtonGroup()
        self.tool_button_group.setExclusive(True)

        self.line_tool_btn = self._create_tool_button("Lines", "line")
        layout.addWidget(self.line_tool_btn)

        self.conics_tool_btn = self._create_tool_button("Curves", "conics")
        layout.addWidget(self.conics_tool_btn)

        self.parametric_tool_btn = self._create_tool_button("Parametric", "parametric")
        layout.addWidget(self.parametric_tool_btn)

        layout.addStretch()
        return panel

    def _create_tool_button(self, text, tool_id):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setStyleSheet(
            """
            QPushButton {
                background-color: #393939;
                border: none;
                padding: 10px 5px;
                font-size: 9pt;
                min-height: 50px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3e3e3e;
            }
            QPushButton:checked {
                font-weight: bold;
            }
        """
        )
        self.tool_button_group.addButton(btn)
        btn.clicked.connect(lambda: self._activate_tool(tool_id))
        return btn

    def _register_tools(self):
        self.tools["line"] = LineTool(self.canvas)
        self.tools["conics"] = ConicsToolWidget(self.canvas)
        self.tools["parametric"] = CurvesTool(self.canvas)

    def _activate_tool(self, tool_id):
        if tool_id not in self.tools:
            return

        if self.current_tool:
            self.current_tool.deactivate()

        self.current_tool = self.tools[tool_id]
        self.current_tool.activate()

        self._update_settings_panel()

    def _update_settings_panel(self):
        while self.settings_layout.count():
            item = self.settings_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        if self.current_tool:
            settings_widget = self.current_tool.get_settings_widget()
            self.settings_layout.addWidget(settings_widget)

    def closeEvent(self, a0):
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(a0)
