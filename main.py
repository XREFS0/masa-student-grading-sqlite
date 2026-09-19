"""
Developed by MASA
All Rights Reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class StudentGradingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("MASA - Student Grading & Academic Evaluation System")
        self.root.geometry("1100x660")
        self.root.configure(bg="#111827")

        self.init_db()
        self.setup_ui()
        self.fetch_grades()

    def init_db(self):
        self.conn = sqlite3.connect("grading_matrix.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                stu_id TEXT PRIMARY KEY,
                stu_name TEXT NOT NULL,
                course TEXT NOT NULL,
                midterm REAL NOT NULL,
                final_exam REAL NOT NULL,
                gpa REAL NOT NULL,
                letter_grade TEXT NOT NULL
            )
        """)
        self.cur.execute("SELECT COUNT(*) FROM grades")
        if self.cur.fetchone()[0] == 0:
            sample = [
                ("STU-8801", "Lucas Sterling", "Advanced Algorithms", 94.0, 96.5, 3.95, "A+"),
                ("STU-8802", "Natalie Portman", "Database Engineering", 88.5, 91.0, 3.75, "A"),
                ("STU-8803", "Victor Reznov", "Computer Networks", 78.0, 82.0, 3.20, "B+"),
                ("STU-8804", "Claire Redfield", "Cybersecurity Protocols", 91.0, 94.0, 3.88, "A"),
                ("STU-8805", "Leon Kennedy", "Software Architecture", 84.0, 86.5, 3.45, "B+"),
            ]
            self.cur.executemany("INSERT INTO grades VALUES (?, ?, ?, ?, ?, ?, ?)", sample)
            self.conn.commit()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1f2937", foreground="#f9fafb", fieldbackground="#1f2937", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#374151", foreground="#10b981", font=("Segoe UI", 10, "bold"))

        hdr = tk.Frame(self.root, bg="#059669", height=65)
        hdr.pack(fill="x")
        tk.Label(hdr, text="MASA Student Grading & Evaluation Engine", font=("Segoe UI", 19, "bold"), fg="#ffffff", bg="#059669").pack(side="left", padx=25, pady=15)
        tk.Label(hdr, text="Architect: MASA | License: XREFS0", font=("Segoe UI", 10), fg="#a7f3d0", bg="#059669").pack(side="right", padx=25, pady=20)

        body = tk.Frame(self.root, bg="#111827")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        sidebar = tk.Frame(body, bg="#1f2937", width=220)
        sidebar.pack(side="left", fill="y", padx=(0, 15))

        for btn_t in ["Grading Records", "Enter Course Marks", "GPA Calculator", "Curve Distribution", "Generate Transcripts", "Export Excel"]:
            tk.Button(sidebar, text=btn_t, font=("Segoe UI", 10, "bold"), fg="#f9fafb", bg="#374151", relief="flat", pady=9, cursor="hand2").pack(fill="x", padx=10, pady=5)

        content = tk.Frame(body, bg="#1f2937")
        content.pack(side="right", fill="both", expand=True)

        stats = tk.Frame(content, bg="#1f2937")
        stats.pack(fill="x", padx=15, pady=15)

        for t, v, c in [("Class Average", "88.4%", "#10b981"), ("Highest GPA", "3.95", "#38bdf8"), ("Total Students", "320", "#facc15"), ("Honor Roll", "48", "#ec4899")]:
            f = tk.Frame(stats, bg="#374151", padx=14, pady=9)
            f.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(f, text=t, font=("Segoe UI", 9), fg="#9ca3af", bg="#374151").pack(anchor="w")
            tk.Label(f, text=v, font=("Segoe UI", 15, "bold"), fg=c, bg="#374151").pack(anchor="w")

        cols = ("Student ID", "Student Name", "Course Registered", "Midterm Score", "Final Exam", "Cumulative GPA", "Grade")
        self.tree = ttk.Treeview(content, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="center")
        self.tree.column("Student Name", width=160, anchor="w")
        self.tree.column("Course Registered", width=180, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def fetch_grades(self):
        self.cur.execute("SELECT * FROM grades")
        for row in self.cur.fetchall():
            self.tree.insert("", "end", values=row)

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGradingSystem(root)
    root.mainloop()
