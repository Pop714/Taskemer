from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHeaderView, QLineEdit, QPushButton,
    QAbstractItemView, QFrame, QWidget, QFileDialog
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QDesktopServices
import database

DIALOG_STYLE = """
    QDialog { background-color: #f4f6f8; }
    QFrame#MainCard { background-color: white; border-radius: 12px; border: 1px solid #e0e0e0; }
    QLabel#Header { font-size: 20px; font-weight: 800; color: #2c3e50; }
    QLabel#SubHeader { font-size: 14px; color: #7f8c8d; margin-bottom: 10px; }
    QLineEdit { padding: 10px; border: 1px solid #bdc3c7; border-radius: 6px; background: #fdfdfd; font-size: 13px; }
    QLineEdit:focus { border: 2px solid #3498db; }
    QPushButton { border-radius: 6px; font-weight: bold; font-size: 13px; border: none; }
    QPushButton#BtnPrimary { background-color: #3498db; color: white; padding: 10px 15px; }
    QPushButton#BtnPrimary:hover { background-color: #2980b9; }
    QPushButton#BtnBrowse { background-color: #ecf0f1; color: #2c3e50; padding: 10px; border: 1px solid #bdc3c7; }
    QPushButton#BtnBrowse:hover { background-color: #bdc3c7; }
    QTableWidget { border: 1px solid #ecf0f1; border-radius: 6px; background: white; }
    QHeaderView::section { background-color: #f8f9fa; padding: 10px; border-bottom: 2px solid #eaeded; font-weight: bold; color: #5d6d7e; }
"""


def open_attachment(path):
    if path.startswith("http://") or path.startswith("https://"):
        QDesktopServices.openUrl(QUrl(path))
    else:
        QDesktopServices.openUrl(QUrl.fromLocalFile(path))


class TaskWorksDialog(QDialog):
    def __init__(self, task_id, task_name, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.setWindowTitle("Log Works")
        self.setMinimumSize(750, 500)
        self.setStyleSheet(DIALOG_STYLE)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        card = QFrame()
        card.setObjectName("MainCard")
        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(25, 25, 25, 25)

        header = QLabel("📝 Task Activity Log")
        header.setObjectName("Header")
        sub_header = QLabel(f"Currently tracking works for: <b>{task_name}</b>")
        sub_header.setObjectName("SubHeader")

        c_layout.addWidget(header)
        c_layout.addWidget(sub_header)
        c_layout.addSpacing(10)

        input_layout = QVBoxLayout()

        self.work_input = QLineEdit()
        self.work_input.setPlaceholderText("Describe the work done or progress made...")

        attach_layout = QHBoxLayout()
        self.attach_input = QLineEdit()
        self.attach_input.setPlaceholderText("Paste URL / File Path here, or browse...")

        btn_browse = QPushButton("📎 Browse")
        btn_browse.setObjectName("BtnBrowse")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.clicked.connect(self.browse_file)

        btn_add = QPushButton("➕ Add Log")
        btn_add.setObjectName("BtnPrimary")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self.add_work)

        attach_layout.addWidget(self.attach_input)
        attach_layout.addWidget(btn_browse)
        attach_layout.addWidget(btn_add)

        input_layout.addWidget(self.work_input)
        input_layout.addLayout(attach_layout)

        c_layout.addLayout(input_layout)
        c_layout.addSpacing(15)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date Recorded", "Work Description", "Attachment", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.verticalHeader().setDefaultSectionSize(45)

        c_layout.addWidget(self.table)
        main_layout.addWidget(card)

        self.refresh_table()

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Attach")
        if file_path:
            self.attach_input.setText(file_path)

    def refresh_table(self):
        self.table.setRowCount(0)
        works = database.get_task_works(self.task_id)

        for row_idx, work in enumerate(works):
            # Unpack 4 variables now
            w_id, desc, date, attachment = work
            self.table.insertRow(row_idx)

            date_item = QTableWidgetItem(date)
            date_item.setTextAlignment(Qt.AlignCenter)
            date_item.setForeground(QColor("#7f8c8d"))

            desc_item = QTableWidgetItem(desc)
            desc_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)

            self.table.setItem(row_idx, 0, date_item)
            self.table.setItem(row_idx, 1, desc_item)

            attach_widget = QWidget()
            attach_layout = QHBoxLayout(attach_widget)
            attach_layout.setContentsMargins(5, 5, 5, 5)

            if attachment:
                btn_open = QPushButton("🔗 Open")
                btn_open.setCursor(Qt.PointingHandCursor)
                btn_open.setStyleSheet("""
                    QPushButton { background-color: #e8f4f8; color: #2980b9; padding: 5px 10px; border-radius: 4px; }
                    QPushButton:hover { background-color: #d6eaf8; }
                """)
                btn_open.clicked.connect(lambda ch, p=attachment: open_attachment(p))
                attach_layout.addWidget(btn_open)
            else:
                attach_layout.addWidget(QLabel("-", alignment=Qt.AlignCenter))
            self.table.setCellWidget(row_idx, 2, attach_widget)

            btn_del = QPushButton("🗑️")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setToolTip("Delete this log entry")
            btn_del.setStyleSheet("""
                QPushButton { background-color: transparent; border-radius: 4px; font-size: 16px; padding: 5px; }
                QPushButton:hover { background-color: #fadbd8; }
            """)
            btn_del.clicked.connect(lambda ch, wid=w_id: self.delete_work(wid))

            del_widget = QWidget()
            del_layout = QHBoxLayout(del_widget)
            del_layout.setContentsMargins(0, 0, 0, 0)
            del_layout.addWidget(btn_del, alignment=Qt.AlignCenter)
            self.table.setCellWidget(row_idx, 3, del_widget)

    def add_work(self):
        desc = self.work_input.text().strip()
        attach = self.attach_input.text().strip()

        if desc:
            database.add_task_work(self.task_id, desc, attach)
            self.work_input.clear()
            self.attach_input.clear()
            self.refresh_table()

    def delete_work(self, work_id):
        database.delete_task_work(work_id)
        self.refresh_table()