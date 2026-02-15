from abc import ABC, abstractmethod

from PyQt6.QtWidgets import QWidget


class BaseTool(ABC):
    def __init__(self, canvas):
        self.canvas = canvas
        self._settings_widget = None

    @abstractmethod
    def get_settings_widget(self) -> QWidget:
        pass

    def activate(self):
        pass

    def deactivate(self):
        pass
