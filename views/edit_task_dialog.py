from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QMessageBox, QHBoxLayout, QFrame
)
from PySide6.QtCore import Qt
import database

DIALOG_STYLE = """
    QDialog { background-color: #f4f6f8; }
    QFrame#MainCard { background-color: white; border-radius: 12px; border: 1px solid #e0e0e0; }
    QLabel#Header { font-size: 20px; font-weight: 800; color: #2c3e50; }
    QLabel#Label { font-size: 14px; font-weight: bold; color: #34495e; margin-top: 10px; }
    QLineEdit, QTextEdit { padding: 10px; border: 1px solid #bdc3c7; border-radius: 6px; background: #fdfdfd; font-size: 14px; }
    QLineEdit:focus, QTextEdit:focus { border: 2px solid #3498db; }
    QPushButton { border-radius: 6px; padding: 8px 20px; font-weight: bold; font-size: 14px; }
    QPushButton#BtnPrimary { background-color: #3498db; color: white; border: none; }
    QPushButton#BtnPrimary:hover { background-color: #2980b9; }
    QPushButton#BtnCancel { background-color: transparent; color: #7f8c8d; border: 1px solid #bdc3c7; }
    QPushButton#BtnCancel:hover { background-color: #ecf0f1; color: #2c3e50; }
"""


class EditTaskDialog(QDialog):
    def __init__(self, task_id, current_name, current_desc, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.setWindowTitle("Edit Task")
        self.setFixedSize(450, 400)
        self.setStyleSheet(DIALOG_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        card = QFrame()
        card.setObjectName("MainCard")
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(25, 25, 25, 25)

        header = QLabel("✏️ Edit Task Details")
        header.setObjectName("Header")
        c_layout.addWidget(header)
        c_layout.addSpacing(10)

        c_layout.addWidget(QLabel("Task Name:", objectName="Label"))
        self.name_input = QLineEdit()
        self.name_input.setText(current_name)
        c_layout.addWidget(self.name_input)

        c_layout.addWidget(QLabel("Description:", objectName="Label"))
        self.desc_input = QTextEdit()
        self.desc_input.setText(current_desc)
        c_layout.addWidget(self.desc_input)

        c_layout.addStretch()

        btn_box = QHBoxLayout()
        btn_box.setSpacing(15)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("BtnCancel")
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("Save Changes")
        btn_save.setObjectName("BtnPrimary")
        btn_save.setCursor(Qt.PointingHandCursor)
        btn_save.clicked.connect(self.save_changes)

        btn_box.addStretch()
        btn_box.addWidget(btn_cancel)
        btn_box.addWidget(btn_save)

        c_layout.addLayout(btn_box)
        main_layout.addWidget(card)

    def save_changes(self):
        name = self.name_input.text().strip()
        desc = self.desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Error", "Name cannot be empty.")
            return

        database.update_task_details(self.task_id, name, desc)
        self.accept()