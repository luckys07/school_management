# lms_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton,
    QFileDialog, QDateEdit, QListWidget, QMessageBox
)
from PyQt5.QtCore import QDate
import db

class LMSModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Learning Management System")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Input: Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Assignment Title")
        layout.addWidget(self.title_input)

        # Input: Description
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Assignment Description")
        layout.addWidget(self.desc_input)

        # File Upload
        self.file_path = ""
        file_btn = QPushButton("Attach File")
        file_btn.clicked.connect(self.select_file)
        layout.addWidget(file_btn)

        # Due Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        layout.addWidget(self.date_input)

        # Submit Button
        submit_btn = QPushButton("Add Assignment")
        submit_btn.clicked.connect(self.add_assignment)
        layout.addWidget(submit_btn)

        # Assignment List
        self.assignment_list = QListWidget()
        layout.addWidget(QLabel("📄 All Assignments:"))
        layout.addWidget(self.assignment_list)

        self.setLayout(layout)
        self.load_assignments()

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.file_path = path

    def add_assignment(self):
        title = self.title_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        due_date = self.date_input.date().toString("yyyy-MM-dd")

        if not title:
            QMessageBox.warning(self, "Input Error", "Title is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO assignments (title, description, file_path, due_date)
            VALUES (?, ?, ?, ?)
        """, (title, desc, self.file_path, due_date))
        conn.commit()
        conn.close()

        self.title_input.clear()
        self.desc_input.clear()
        self.file_path = ""
        self.load_assignments()
        QMessageBox.information(self, "Success", "Assignment added!")

    def load_assignments(self):
        self.assignment_list.clear()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, due_date FROM assignments")
        for title, due in cursor.fetchall():
            self.assignment_list.addItem(f"{title} (Due: {due})")
        conn.close()
