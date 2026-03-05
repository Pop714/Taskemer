from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QPushButton, QMessageBox, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
import database


class AddTaskView(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)

        title = QLabel("Create a New Task")
        title.setStyleSheet("font-size: 26px; font-weight: 900; color: #2c3e50;")

        sub_title = QLabel("Fill out the details below to add a new task to your active board.")
        sub_title.setStyleSheet("color: #7f8c8d; font-size: 14px;")

        header_layout.addWidget(title)
        header_layout.addWidget(sub_title)
        main_layout.addLayout(header_layout)

        card = QFrame()
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: 1px solid #e0e0e0; 
            }
        """)

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(35, 35, 35, 35)
        c_layout.setSpacing(15)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("E.g., Update Server Infrastructure")
        self.name_input.setFixedHeight(45)

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Detailed description of the task...")
        self.desc_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.initial_work_input = QTextEdit()
        self.initial_work_input.setPlaceholderText("Any initial progress or notes? (Leave empty if none)")
        self.initial_work_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.priority_cb = QComboBox()
        self.priority_cb.addItems(["🟢 Low Priority (2)", "🟡 Medium Priority (1)", "🔴 High Priority (0)"])
        self.priority_cb.setFixedHeight(45)

        btn_submit = QPushButton("➕ Add Task to Dashboard")
        btn_submit.setCursor(Qt.PointingHandCursor)
        btn_submit.setFixedHeight(50)
        btn_submit.setStyleSheet("""
            QPushButton { 
                background-color: #2980b9; 
                color: white; 
                border-radius: 8px; 
                font-weight: bold; 
                font-size: 16px; 
                border: none;
            }
            QPushButton:hover { background-color: #3498db; }
        """)
        btn_submit.clicked.connect(self.submit_task)

        def make_label(text, is_optional=False):
            lbl = QLabel()
            if is_optional:
                lbl.setText(
                    f"{text} <span style='color: #95a5a6; font-size: 13px; font-weight: normal;'>(Optional)</span>")
            else:
                lbl.setText(text)
            lbl.setStyleSheet("font-size: 15px; font-weight: bold; color: #34495e; border: none;")
            return lbl

        c_layout.addWidget(make_label("📌 Task Name:"))
        c_layout.addWidget(self.name_input)

        c_layout.addWidget(make_label("⚡ Priority Level:"))
        c_layout.addWidget(self.priority_cb)

        c_layout.addWidget(make_label("📝 Description:"))
        c_layout.addWidget(self.desc_input, 2)

        c_layout.addWidget(make_label("📖 Initial Log / Work", is_optional=True))
        c_layout.addWidget(self.initial_work_input, 1)

        c_layout.addSpacing(10)
        c_layout.addWidget(btn_submit)

        main_layout.addWidget(card)

    def submit_task(self):
        name = self.name_input.text().strip()
        desc = self.desc_input.toPlainText().strip()
        work = self.initial_work_input.toPlainText().strip()
        priority = self.priority_cb.currentIndex()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Task Name is required.")
            return

        database.add_task(self.user_id, name, desc, priority, work if work else None)

        QMessageBox.information(self, "Success", "Task created successfully!")

        self.name_input.clear()
        self.desc_input.clear()
        self.initial_work_input.clear()
        self.priority_cb.setCurrentIndex(0)