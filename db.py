# db.py
import sqlite3

def get_connection():
    return sqlite3.connect("school.db")

def setup_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Assignments Table (LMS)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            file_path TEXT,
            due_date TEXT
        )
    """)

    # Library Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            isbn TEXT,
            quantity INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            student_name TEXT,
            issue_date TEXT,
            return_date TEXT,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    """)

    # Transport Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            driver_name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT NOT NULL,
            pickup_time TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_assignment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            bus_id INTEGER,
            route_id INTEGER,
            FOREIGN KEY(bus_id) REFERENCES buses(id),
            FOREIGN KEY(route_id) REFERENCES routes(id)
        )
    """)

    # Hostel Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostel_id INTEGER,
            room_number TEXT,
            capacity INTEGER,
            FOREIGN KEY(hostel_id) REFERENCES hostels(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hostel_allocation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            room_id INTEGER,
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )
    """)

    # Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER,
            location TEXT
        )
    """)

    # HR Tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            salary REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER,
            pay_date TEXT,
            amount REAL,
            FOREIGN KEY(staff_id) REFERENCES staff(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER,
            leave_date TEXT,
            reason TEXT,
            FOREIGN KEY(staff_id) REFERENCES staff(id)
        )
    """)

    # Biometric Attendance Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            date TEXT,
            time TEXT,
            status TEXT
        )
    """)

    conn.commit()
    conn.close()
