# hostel_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
import db

class HostelModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hostel Management")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Hostel name input
        self.hostel_input = QLineEdit()
        self.hostel_input.setPlaceholderText("Hostel Name")
        layout.addWidget(self.hostel_input)

        hostel_btn = QPushButton("Add Hostel")
        hostel_btn.clicked.connect(self.add_hostel)
        layout.addWidget(hostel_btn)

        # Room input
        self.room_input = QLineEdit()
        self.room_input.setPlaceholderText("Room Number")
        layout.addWidget(self.room_input)

        self.capacity_input = QLineEdit()
        self.capacity_input.setPlaceholderText("Capacity")
        layout.addWidget(self.capacity_input)

        room_btn = QPushButton("Add Room")
        room_btn.clicked.connect(self.add_room)
        layout.addWidget(room_btn)

        # Room list
        self.room_list = QListWidget()
        layout.addWidget(QLabel("🛏️ Hostel Rooms:"))
        layout.addWidget(self.room_list)

        self.setLayout(layout)
        self.load_rooms()

    def add_hostel(self):
        name = self.hostel_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Hostel name is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO hostels (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()

        self.hostel_input.clear()
        QMessageBox.information(self, "Success", "Hostel added!")

    def add_room(self):
        room = self.room_input.text().strip()
        try:
            capacity = int(self.capacity_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Capacity must be a number.")
            return

        if not room:
            QMessageBox.warning(self, "Input Error", "Room number is required.")
            return

        # For simplicity, assign to first hostel
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM hostels LIMIT 1")
        result = cursor.fetchone()
        if not result:
            QMessageBox.warning(self, "Missing Hostel", "Add at least one hostel first.")
            conn.close()
            return

        hostel_id = result[0]
        cursor.execute("""
            INSERT INTO rooms (hostel_id, room_number, capacity)
            VALUES (?, ?, ?)
        """, (hostel_id, room, capacity))
        conn.commit()
        conn.close()

        self.room_input.clear()
        self.capacity_input.clear()
        self.load_rooms()
        QMessageBox.information(self, "Success", "Room added!")

    def load_rooms(self):
        self.room_list.clear()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.room_number, r.capacity, h.name
            FROM rooms r
            JOIN hostels h ON r.hostel_id = h.id
        """)
        for room, cap, hostel in cursor.fetchall():
            self.room_list.addItem(f"{hostel} - Room {room} (Capacity: {cap})")
        conn.close()
