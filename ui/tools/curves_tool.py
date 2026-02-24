from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from algorithms.parametric_curves import (
    bezier_curve,
    bspline_curve,
    hermite_curve,
)
from ui.tools.base_tool import BaseTool


class CurvesTool(BaseTool):
    def __init__(self, canvas):
        super().__init__(canvas)
        self._create_settings_widget()

    def _create_settings_widget(self):
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        title_label = QLabel("Parametric Curves")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        layout.addWidget(self._create_separator())

        curve_group = QGroupBox("Method")
        curve_layout = QVBoxLayout()
        curve_layout.setSpacing(5)

        self.curve_combo = QComboBox()
        self.curve_combo.addItem("Hermite", "hermite")
        self.curve_combo.addItem("Bezier", "bezier")
        self.curve_combo.addItem("B-spline", "bspline")
        self.curve_combo.setCurrentIndex(0)
        self.curve_combo.currentIndexChanged.connect(self._on_curve_changed)

        curve_layout.addWidget(self.curve_combo)
        curve_group.setLayout(curve_layout)
        layout.addWidget(curve_group)

        self.hint_label = QLabel()
        self.hint_label.setStyleSheet("color: #666; font-size: 9pt;")
        self.hint_label.setWordWrap(True)
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hint_label)
        self._update_hint()

        params_group = QGroupBox("Parameters")
        params_layout = QVBoxLayout()
        params_layout.setSpacing(5)

        params_layout.addWidget(QLabel("Segments:"))
        self.segments_spin = QSpinBox()
        self.segments_spin.setMinimum(1)
        self.segments_spin.setMaximum(100)
        self.segments_spin.setValue(20)
        params_layout.addWidget(self.segments_spin)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        self.draw_btn = QPushButton("▶ Draw Curve")
        self.draw_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """
        )
        self.draw_btn.clicked.connect(self.on_draw)
        layout.addWidget(self.draw_btn)

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.on_clear)
        layout.addWidget(self.clear_btn)

        layout.addWidget(self._create_separator())

        debug_group = QGroupBox("Debug Mode")
        debug_layout = QVBoxLayout()
        debug_layout.setSpacing(5)

        self.debug_checkbox = QCheckBox("Step-by-step")
        self.debug_checkbox.setChecked(False)
        self.debug_checkbox.stateChanged.connect(self.on_debug_mode_changed)
        debug_layout.addWidget(self.debug_checkbox)

        self.step_label = QLabel("Step: 0 / 0")
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        debug_layout.addWidget(self.step_label)

        self.step_slider = QSlider(Qt.Orientation.Horizontal)
        self.step_slider.setMinimum(0)
        self.step_slider.setMaximum(0)
        self.step_slider.setValue(0)
        self.step_slider.setEnabled(False)
        self.step_slider.valueChanged.connect(self.on_step_changed)
        debug_layout.addWidget(self.step_slider)

        step_buttons_layout = QHBoxLayout()
        self.prev_btn = QPushButton("◄")
        self.prev_btn.setEnabled(False)
        self.prev_btn.clicked.connect(self.on_prev_step)

        self.next_btn = QPushButton("►")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(self.on_next_step)

        step_buttons_layout.addWidget(self.prev_btn)
        step_buttons_layout.addWidget(self.next_btn)
        debug_layout.addLayout(step_buttons_layout)

        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)

        layout.addWidget(self._create_separator())

        zoom_group = QGroupBox("Zoom")
        zoom_layout = QVBoxLayout()
        zoom_layout.setSpacing(5)

        self.scale_label = QLabel()
        self.scale_label.setStyleSheet("font-weight: bold;")
        self.scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_scale_label()

        zoom_buttons_layout = QHBoxLayout()
        self.zoom_out_btn = QPushButton("−")
        self.zoom_out_btn.setFixedSize(35, 35)
        self.zoom_out_btn.clicked.connect(self.on_zoom_out)

        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(35, 35)
        self.zoom_in_btn.clicked.connect(self.on_zoom_in)

        zoom_buttons_layout.addStretch()
        zoom_buttons_layout.addWidget(self.zoom_out_btn)
        zoom_buttons_layout.addWidget(self.scale_label)
        zoom_buttons_layout.addWidget(self.zoom_in_btn)
        zoom_buttons_layout.addStretch()

        zoom_layout.addLayout(zoom_buttons_layout)
        zoom_group.setLayout(zoom_layout)
        layout.addWidget(zoom_group)

        self.reset_btn = QPushButton("🎯 Reset Camera")
        self.reset_btn.clicked.connect(self.on_reset_camera)
        layout.addWidget(self.reset_btn)

        layout.addStretch()

        info_label = QLabel(
            "Controls:\n• RMB - select points\n• MMB - edit point\n• LMB - pan\n• Wheel - zoom"
        )
        info_label.setStyleSheet("color: gray; font-size: 9pt;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self._settings_widget = widget

    def _create_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        return line

    def _update_hint(self):
        curve_type = self.curve_combo.currentData()
        hints = {
            "hermite": "Click 4 points: P0, P1 (endpoints) + M0, M1 (tangent vectors)",
            "bezier": "Click 4 points: P0, P1, P2, P3 (control points)",
            "bspline": "Click 4+ points: control polygon vertices",
        }
        self.hint_label.setText(hints.get(curve_type, ""))

    def _on_curve_changed(self):
        self._update_hint()

    def get_settings_widget(self) -> QWidget:
        return self._settings_widget

    def activate(self):
        self.update_scale_label()

    def update_scale_label(self):
        self.scale_label.setText(f"{self.canvas.cell_size} px")

    def on_zoom_in(self):
        self.canvas.zoom_in()
        self.update_scale_label()

    def on_zoom_out(self):
        self.canvas.zoom_out()
        self.update_scale_label()

    def on_reset_camera(self):
        self.canvas.reset_view()
        self.update_scale_label()

    def on_clear(self):
        self.canvas.clear_all()
        self.step_slider.setMaximum(0)
        self.step_slider.setValue(0)
        self.step_label.setText("Step: 0 / 0")
        self._update_step_buttons()

    def on_debug_mode_changed(self, state):
        enabled = state == Qt.CheckState.Checked.value
        self.step_slider.setEnabled(enabled)
        self.prev_btn.setEnabled(enabled and self.step_slider.value() > 0)
        self.next_btn.setEnabled(
            enabled and self.step_slider.value() < self.step_slider.maximum()
        )

    def on_step_changed(self, value):
        self.canvas.set_debug_step(value)
        max_steps = self.step_slider.maximum()
        self.step_label.setText(f"Step: {value} / {max_steps}")
        self._update_step_buttons()

    def on_prev_step(self):
        self.step_slider.setValue(self.step_slider.value() - 1)

    def on_next_step(self):
        self.step_slider.setValue(self.step_slider.value() + 1)

    def _update_step_buttons(self):
        if self.debug_checkbox.isChecked():
            self.prev_btn.setEnabled(self.step_slider.value() > 0)
            self.next_btn.setEnabled(
                self.step_slider.value() < self.step_slider.maximum()
            )

    def on_draw(self):
        points = self.canvas.get_clicked_points()
        curve_type = self.curve_combo.currentData()
        segments = self.segments_spin.value()
        generator = None

        if curve_type == "hermite":
            if len(points) < 4:
                return
            p0 = points[0]
            p1 = points[1]
            m0 = points[2]
            m1 = points[3]
            generator = hermite_curve(p0, p1, m0, m1, steps=segments)

        elif curve_type == "bezier":
            if len(points) < 4:
                return
            p0 = points[0]
            p1 = points[1]
            p2 = points[2]
            p3 = points[3]
            generator = bezier_curve(p0, p1, p2, p3, steps=segments)

        elif curve_type == "bspline":
            if len(points) < 4:
                return
            generator = bspline_curve(points, steps=segments)

        if generator:
            self.canvas.run_algorithm(generator)
            self.canvas.clear_clicked_points()

            max_steps = self.canvas.get_max_steps()
            self.step_slider.setMaximum(max_steps)
            if self.debug_checkbox.isChecked():
                self.step_slider.setValue(0)
            else:
                self.step_slider.setValue(max_steps)
            self.step_label.setText(f"Step: {self.step_slider.value()} / {max_steps}")
            self._update_step_buttons()
