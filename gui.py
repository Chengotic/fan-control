from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QGridLayout
)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
import sys
import json
from pathlib import Path
import subprocess

CONFIG_PATH = Path(__file__).parent / "config.json"

class FanControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fan Control")
        self.setFixedSize(400, 300)

        layout = QGridLayout()

        # Create labels and sliders
        self.cpu_min_label = QLabel("CPU Min Temp: 40°C")
        self.cpu_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.cpu_min_slider.setRange(20, 80)
        self.cpu_min_slider.setValue(40)
        self.cpu_min_slider.valueChanged.connect(self.update_labels)

        self.cpu_max_label = QLabel("CPU Max Temp: 80°C")
        self.cpu_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.cpu_max_slider.setRange(40, 100)
        self.cpu_max_slider.setValue(80)
        self.cpu_max_slider.valueChanged.connect(self.update_labels)

        self.gpu_min_label = QLabel("GPU Min Temp: 40°C")
        self.gpu_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.gpu_min_slider.setRange(20, 80)
        self.gpu_min_slider.setValue(40)
        self.gpu_min_slider.valueChanged.connect(self.update_labels)

        self.gpu_max_label = QLabel("GPU Max Temp: 80°C")
        self.gpu_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.gpu_max_slider.setRange(40, 100)
        self.gpu_max_slider.setValue(80)
        self.gpu_max_slider.valueChanged.connect(self.update_labels)

        self.controller_process = None

        # Add widgets to layout
        layout.addWidget(self.cpu_min_label, 0, 0)
        layout.addWidget(self.cpu_min_slider, 0, 1)
        layout.addWidget(self.cpu_max_label, 1, 0)
        layout.addWidget(self.cpu_max_slider, 1, 1)
        layout.addWidget(self.gpu_min_label, 2, 0)
        layout.addWidget(self.gpu_min_slider, 2, 1)
        layout.addWidget(self.gpu_max_label, 3, 0)
        layout.addWidget(self.gpu_max_slider, 3, 1)

        # Apply button
        self.apply_button = QPushButton("Apply Settings")
        self.apply_button.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_button, 4, 0, 1, 2)

        self.setLayout(layout)

    def update_labels(self):
        self.cpu_min_label.setText(f"CPU Min Temp: {self.cpu_min_slider.value()}°C")
        self.cpu_max_label.setText(f"CPU Max Temp: {self.cpu_max_slider.value()}°C")
        self.gpu_min_label.setText(f"GPU Min Temp: {self.gpu_min_slider.value()}°C")
        self.gpu_max_label.setText(f"GPU Max Temp: {self.gpu_max_slider.value()}°C")

    def apply_settings(self):
        cpu_min = self.cpu_min_slider.value()
        cpu_max = self.cpu_max_slider.value()
        gpu_min = self.gpu_min_slider.value()
        gpu_max = self.gpu_max_slider.value()

        config = {
            "cpu_min": cpu_min,
            "cpu_max": cpu_max,
            "gpu_min": gpu_min,
            "gpu_max": gpu_max,
        }

        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)

        if self.controller_process is None or self.controller_process.poll() is not None:
            self.controller_process = subprocess.Popen(["sudo", sys.executable, str(Path(__file__).parent / "fan-controller.py")])
        print(f"Saved settings to {CONFIG_PATH}")

        print(f"CPU: {cpu_min}–{cpu_max}°C | GPU: {gpu_min}–{gpu_max}°C")
    def closeEvent(self, event):
        if self.controller_process is not None:
            self.controller_process.terminate()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FanControlApp()
    window.show()
    sys.exit(app.exec())
