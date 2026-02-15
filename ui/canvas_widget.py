from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 600)
        self.setMouseTracking(True)

        self.cell_size = 25
        self.offset_x = 150.0
        self.offset_y = 150.0

        self.is_panning = False
        self.last_pan_pos = QPoint()

        self.lines = []
        self.clicked_points = []

        self.current_line_pixels = []
        self.current_step = 0

        self.bg_color = QColor(255, 255, 255)
        self.grid_color = QColor(220, 220, 220)
        self.axis_color = QColor(0, 0, 0)
        self.pixel_color = QColor(66, 165, 245)
        self.point_color = QColor(255, 87, 34)

    def world_to_screen(self, world_x: float, world_y: float):
        h = self.height()
        sx = self.offset_x + (world_x * self.cell_size)
        sy = h - self.offset_y - (world_y * self.cell_size)
        return sx, sy

    def screen_to_world(self, screen_x: float, screen_y: float):
        h = self.height()
        world_x = int((screen_x - self.offset_x) // self.cell_size)
        world_y = int((h - screen_y - self.offset_y) // self.cell_size)
        return world_x, world_y

    def zoom_in(self):
        if self.cell_size < 150:
            self.cell_size += 2
            self.update()

    def zoom_out(self):
        if self.cell_size > 4:
            self.cell_size -= 2
            self.update()

    def reset_view(self):
        self.offset_x = 150.0
        self.offset_y = 150.0
        self.cell_size = 25
        self.update()

    def clear_all(self):
        self.lines.clear()
        self.clicked_points.clear()
        self.current_line_pixels.clear()
        self.current_step = 0
        self.update()

    def clear_clicked_points(self):
        self.clicked_points.clear()
        self.update()

    def get_clicked_points(self):
        return self.clicked_points.copy()

    def run_algorithm(self, generator):
        self.current_line_pixels = list(generator)
        self.current_step = len(self.current_line_pixels)
        self.lines.append(self.current_line_pixels.copy())
        self.update()

    def set_debug_step(self, step):
        self.current_step = max(0, min(step, len(self.current_line_pixels)))
        self.update()

    def get_max_steps(self):
        return len(self.current_line_pixels)

    def wheelEvent(self, a0):
        if a0 is not None and a0.angleDelta().y() > 0:
            self.zoom_in()
        elif a0 is not None:
            self.zoom_out()

    def mousePressEvent(self, a0):
        if a0 is None:
            return

        if a0.button() == Qt.MouseButton.LeftButton:
            wx, wy = self.screen_to_world(a0.pos().x(), a0.pos().y())
            self.clicked_points.append((wx, wy))
            self.update()
        elif (
            a0.button() == Qt.MouseButton.MiddleButton
            or a0.button() == Qt.MouseButton.RightButton
        ):
            self.is_panning = True
            self.last_pan_pos = a0.pos()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, a0):
        if self.is_panning and a0 is not None:
            delta = a0.pos() - self.last_pan_pos
            self.offset_x += delta.x()
            self.offset_y -= delta.y()
            self.last_pan_pos = a0.pos()
            self.update()

    def mouseReleaseEvent(self, a0):
        if a0 is not None and (
            a0.button() == Qt.MouseButton.MiddleButton
            or a0.button() == Qt.MouseButton.RightButton
        ):
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        w = self.width()
        h = self.height()

        painter.fillRect(0, 0, w, h, self.bg_color)

        self._draw_grid(painter, w, h)
        self._draw_axes(painter, w, h)
        self._draw_all_lines(painter)
        self._draw_current_line(painter)
        self._draw_clicked_points(painter)

        painter.end()

    def _draw_grid(self, painter: QPainter, w: int, h: int):
        pen = QPen(self.grid_color, 1)
        painter.setPen(pen)

        x_start = self.offset_x % self.cell_size
        x = x_start
        while x < w:
            painter.drawLine(int(x), 0, int(x), h)
            x += self.cell_size

        y_start = (h - self.offset_y) % self.cell_size
        y = y_start
        while y < h:
            painter.drawLine(0, int(y), w, int(y))
            y += self.cell_size

    def _draw_axes(self, painter: QPainter, w: int, h: int):
        pen = QPen(self.axis_color, 2)
        painter.setPen(pen)

        ax_y = int(h - self.offset_y)
        painter.drawLine(0, ax_y, w, ax_y)

        ax_x = int(self.offset_x)
        painter.drawLine(ax_x, 0, ax_x, h)

    def _draw_all_lines(self, painter: QPainter):
        if len(self.lines) == 0:
            return

        for line_pixels in self.lines[:-1]:
            for grid_x, grid_y, opacity in line_pixels:
                self._draw_pixel(painter, grid_x, grid_y, opacity)

    def _draw_current_line(self, painter: QPainter):
        if len(self.current_line_pixels) == 0:
            return

        for i in range(min(self.current_step, len(self.current_line_pixels))):
            grid_x, grid_y, opacity = self.current_line_pixels[i]
            self._draw_pixel(painter, grid_x, grid_y, opacity)

    def _draw_pixel(self, painter: QPainter, grid_x: int, grid_y: int, opacity: float):
        sx, sy = self.world_to_screen(grid_x, grid_y)
        x = int(sx)
        y = int(sy - self.cell_size)
        size = int(self.cell_size)

        color = QColor(self.pixel_color)
        color.setAlphaF(opacity)
        painter.fillRect(x, y, size, size, color)

    def _draw_clicked_points(self, painter: QPainter):
        for grid_x, grid_y in self.clicked_points:
            sx, sy = self.world_to_screen(grid_x, grid_y)
            x = int(sx)
            y = int(sy - self.cell_size)
            size = int(self.cell_size)

            color = QColor(self.point_color)
            color.setAlphaF(0.7)
            painter.fillRect(x, y, size, size, color)

            painter.setPen(QPen(QColor(255, 255, 255), 2))
            center_x = x + size // 2
            center_y = y + size // 2
            offset = size // 4
            painter.drawLine(center_x - offset, center_y, center_x + offset, center_y)
            painter.drawLine(center_x, center_y - offset, center_x, center_y + offset)
