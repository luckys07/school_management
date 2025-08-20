# biometric_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
from PyQt5.QtCore import QDateTime
import db
import datetime

class BiometricModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biometric/RFID Attendance")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Student input
        self.student_input = QLineEdit()
        self.student_input.setPlaceholderText("Enter Student Name (Simulated Scan)")
        layout.addWidget(self.student_input)

        # Mark Present Button
        mark_btn = QPushButton("Mark Attendance")
        mark_btn.clicked.connect(self.mark_attendance)
        layout.addWidget(mark_btn)

        # Attendance List
        self.attendance_list = QListWidget()
        layout.addWidget(QLabel("📅 Today's Attendance:"))
        layout.addWidget(self.attendance_list)

        self.setLayout(layout)
        self.load_today_attendance()

    def mark_attendance(self):
        name = self.student_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Student name is required.")
            return

        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        status = "Present"

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO attendance (student_name, date, time, status)
            VALUES (?, ?, ?, ?)
        """, (name, date, time, status))
        conn.commit()
        conn.close()

        self.student_input.clear()
        self.load_today_attendance()
        QMessageBox.information(self, "Success", f"{name}'s attendance marked.")

    def load_today_attendance(self):
        self.attendance_list.clear()
        today = datetime.date.today().strftime("%Y-%m-%d")
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT student_name, time FROM attendance WHERE date = ?", (today,))
        for name, time in cursor.fetchall():
            self.attendance_list.addItem(f"{name} - {time}")
        conn.close()
