# hr_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
import db

class HRModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Management")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Input: Staff Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Staff Name")
        layout.addWidget(self.name_input)

        # Input: Role
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Role")
        layout.addWidget(self.role_input)

        # Input: Salary
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("Monthly Salary")
        layout.addWidget(self.salary_input)

        # Add Staff Button
        add_btn = QPushButton("Add Staff Member")
        add_btn.clicked.connect(self.add_staff)
        layout.addWidget(add_btn)

        # Staff List
        self.staff_list = QListWidget()
        layout.addWidget(QLabel("👨‍🏫 Staff List:"))
        layout.addWidget(self.staff_list)

        self.setLayout(layout)
        self.load_staff()

    def add_staff(self):
        name = self.name_input.text().strip()
        role = self.role_input.text().strip()
        try:
            salary = float(self.salary_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Salary must be a number.")
            return

        if not name or not role:
            QMessageBox.warning(self, "Input Error", "Name and Role are required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO staff (name, role, salary)
            VALUES (?, ?, ?)
        """, (name, role, salary))
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.role_input.clear()
        self.salary_input.clear()
        self.load_staff()
        QMessageBox.information(self, "Success", "Staff member added!")

    def load_staff(self):
        self.staff_list.clear()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, role, salary FROM staff")
        for name, role, salary in cursor.fetchall():
            self.staff_list.addItem(f"{name} - {role} (₹{salary:.2f})")
        conn.close()
