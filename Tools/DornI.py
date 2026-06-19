import sys
import random
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QProgressBar, QFrame
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QPen


# ------------------ Drone Database (Simulation) ------------------

DRONE_DATABASE = [
    ("Consumer", "DJI Mini 3"),
    ("Consumer", "DJI Air 2S"),
    ("Commercial", "DJI Matrice 300"),
    ("Commercial", "Autel EVO II"),
    ("Military", "RQ-20 Puma"),
    ("Unknown", "Unidentified UAV"),
]


# ------------------ Radar Widget ------------------

class RadarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.target_distance_km = None
        self.setMinimumSize(220, 220)
        self.setStyleSheet("background-color: #0b0f14;")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_radar)
        self.timer.start(40)

    def update_radar(self):
        self.angle = (self.angle + 3) % 360
        self.update()

    def set_target(self, distance_km):
        self.target_distance_km = distance_km

    def clear_target(self):
        self.target_distance_km = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 12

        painter.setPen(QPen(Qt.green, 2))
        painter.drawEllipse(cx - radius, cy - radius, radius * 2, radius * 2)
        painter.drawLine(cx - radius, cy, cx + radius, cy)
        painter.drawLine(cx, cy - radius, cx, cy + radius)

        angle_rad = math.radians(self.angle)
        sx = cx + radius * math.cos(angle_rad)
        sy = cy - radius * math.sin(angle_rad)
        painter.drawLine(cx, cy, int(sx), int(sy))

        if self.target_distance_km is not None:
            blip_radius = int((self.target_distance_km / 15.0) * radius)
            bx = cx + blip_radius * math.cos(angle_rad)
            by = cy - blip_radius * math.sin(angle_rad)

            painter.setPen(QPen(Qt.red, 6))
            painter.drawPoint(int(bx), int(by))


# ------------------ Main Application ------------------

class DroneSignalDetector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drone Detection Radar System (15 km)")
        self.setGeometry(200, 150, 640, 560)

        self.setStyleSheet("""
            QWidget {
                background-color: #0e1117;
                color: #e6edf3;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1f2933;
                border: 1px solid #00ff99;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #263241;
            }
            QProgressBar {
                border: 1px solid #00ff99;
                height: 14px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00ff99;
            }
        """)

        # Labels
        self.status_label = QLabel("Status: Idle")
        self.altitude_label = QLabel("Altitude: --- m")
        self.distance_label = QLabel("Drone Distance: --- km")
        self.signal_label = QLabel("Signal Strength: --- %")
        self.type_label = QLabel("Drone Type: ---")
        self.model_label = QLabel("Drone Model: ---")
        self.sensor_distance_label = QLabel("Sensor A ↔ B Distance: --- km")
        self.flight_distance_label = QLabel("Drone Flight Distance: 0.00 km")

        self.signal_bar = QProgressBar()
        self.signal_bar.setRange(0, 100)

        # Radar
        self.radar = RadarWidget()

        radar_box = QFrame()
        radar_box.setStyleSheet("""
            QFrame {
                background-color: #121821;
                border: 2px solid #00ff99;
                border-radius: 8px;
            }
        """)

        radar_layout = QVBoxLayout()
        radar_title = QLabel("Radar Signal Display")
        radar_title.setStyleSheet("color: #00ff99; font-weight: bold;")
        radar_layout.addWidget(radar_title, alignment=Qt.AlignCenter)
        radar_layout.addWidget(self.radar)
        radar_box.setLayout(radar_layout)

        # Buttons
        self.scan_btn = QPushButton("Start Scan")
        self.stop_btn = QPushButton("Stop Scan")
        self.stop_btn.setEnabled(False)

        self.scan_btn.clicked.connect(self.start_scan)
        self.stop_btn.clicked.connect(self.stop_scan)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.scan_btn)
        btn_layout.addWidget(self.stop_btn)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.altitude_label)
        layout.addWidget(self.distance_label)
        layout.addWidget(self.signal_label)
        layout.addWidget(self.signal_bar)
        layout.addWidget(self.type_label)
        layout.addWidget(self.model_label)
        layout.addWidget(self.sensor_distance_label)
        layout.addWidget(self.flight_distance_label)
        layout.addWidget(radar_box)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # Timers & state
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.detect_signal)

        self.last_position = None
        self.total_flight_distance_km = 0.0
        self.alert_triggered = False

    def start_scan(self):
        self.status_label.setText("Status: Scanning...")
        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.timer.start(1000)

    def stop_scan(self):
        self.timer.stop()
        self.status_label.setText("Status: Scan Stopped")
        self.scan_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        self.signal_bar.setValue(0)
        self.radar.clear_target()

        self.last_position = None
        self.total_flight_distance_km = 0.0
        self.flight_distance_label.setText("Drone Flight Distance: 0.00 km")
        self.alert_triggered = False

    def detect_signal(self):
        altitude = random.randint(100, 1000)
        drone_distance_m = random.randint(1000, 15000)

        current_position = (
            random.uniform(0, 15),
            random.uniform(0, 15)
        )

        if self.last_position is not None:
            self.total_flight_distance_km += math.dist(
                self.last_position, current_position
            )
        self.last_position = current_position

        sensor_distance = math.dist((0, 0), (random.uniform(1, 5), random.uniform(1, 5)))
        signal_strength = max(0, int(100 - drone_distance_m / 150))

        self.altitude_label.setText(f"Altitude: {altitude} m")
        self.distance_label.setText(f"Drone Distance: {drone_distance_m / 1000:.2f} km")
        self.signal_label.setText(f"Signal Strength: {signal_strength} %")
        self.sensor_distance_label.setText(
            f"Sensor A ↔ B Distance: {sensor_distance:.2f} km"
        )
        self.flight_distance_label.setText(
            f"Drone Flight Distance: {self.total_flight_distance_km:.2f} km"
        )
        self.signal_bar.setValue(signal_strength)

        if 480 <= altitude <= 520 and signal_strength >= 55:
            drone_type, drone_model = random.choice(DRONE_DATABASE)
            self.type_label.setText(f"Drone Type: {drone_type}")
            self.model_label.setText(f"Drone Model: {drone_model}")
            self.status_label.setText("🚨 Drone Detected")

            self.radar.set_target(drone_distance_m / 1000)

            if not self.alert_triggered:
                QApplication.beep()
                self.alert_triggered = True
        else:
            self.status_label.setText("Status: Scanning...")
            self.type_label.setText("Drone Type: ---")
            self.model_label.setText("Drone Model: ---")
            self.radar.clear_target()
            self.alert_triggered = False


# ------------------ Run Application ------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DroneSignalDetector()
    window.show()
    sys.exit(app.exec_())
