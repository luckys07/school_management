# transport_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout
)
import db

class TransportModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transport Management")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # --- Add Bus Section ---
        layout.addWidget(QLabel("➕ Add Bus"))
        self.bus_number_input = QLineEdit()
        self.bus_number_input.setPlaceholderText("Bus Number")
        layout.addWidget(self.bus_number_input)

        self.driver_name_input = QLineEdit()
        self.driver_name_input.setPlaceholderText("Driver Name")
        layout.addWidget(self.driver_name_input)

        add_bus_btn = QPushButton("Add Bus")
        add_bus_btn.clicked.connect(self.add_bus)
        layout.addWidget(add_bus_btn)

        # --- Add Route Section ---
        layout.addWidget(QLabel("🛣️ Add Route"))
        self.route_name_input = QLineEdit()
        self.route_name_input.setPlaceholderText("Route Name")
        layout.addWidget(self.route_name_input)

        self.pickup_time_input = QLineEdit()
        self.pickup_time_input.setPlaceholderText("Pickup Time (e.g. 7:30 AM)")
        layout.addWidget(self.pickup_time_input)

        add_route_btn = QPushButton("Add Route")
        add_route_btn.clicked.connect(self.add_route)
        layout.addWidget(add_route_btn)

        # --- List Buses & Routes ---
        layout.addWidget(QLabel("🚌 Buses:"))
        self.bus_list = QListWidget()
        layout.addWidget(self.bus_list)

        layout.addWidget(QLabel("🛣️ Routes:"))
        self.route_list = QListWidget()
        layout.addWidget(self.route_list)

        self.setLayout(layout)
        self.load_data()

    def add_bus(self):
        number = self.bus_number_input.text().strip()
        driver = self.driver_name_input.text().strip()
        if not number:
            QMessageBox.warning(self, "Input Error", "Bus number is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO buses (bus_number, driver_name) VALUES (?, ?)", (number, driver))
        conn.commit()
        conn.close()

        self.bus_number_input.clear()
        self.driver_name_input.clear()
        self.load_data()
        QMessageBox.information(self, "Success", "Bus added successfully.")

    def add_route(self):
        route = self.route_name_input.text().strip()
        pickup = self.pickup_time_input.text().strip()
        if not route:
            QMessageBox.warning(self, "Input Error", "Route name is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO routes (route_name, pickup_time) VALUES (?, ?)", (route, pickup))
        conn.commit()
        conn.close()

        self.route_name_input.clear()
        self.pickup_time_input.clear()
        self.load_data()
        QMessageBox.information(self, "Success", "Route added successfully.")

    def load_data(self):
        self.bus_list.clear()
        self.route_list.clear()

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT bus_number, driver_name FROM buses")
        for bus_number, driver in cursor.fetchall():
            self.bus_list.addItem(f"{bus_number} (Driver: {driver})")

        cursor.execute("SELECT route_name, pickup_time FROM routes")
        for route, pickup in cursor.fetchall():
            self.route_list.addItem(f"{route} (Pickup: {pickup})")
        conn.close()
