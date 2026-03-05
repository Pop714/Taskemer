from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QHBoxLayout, QLabel, QAbstractItemView
)
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
import database
from views.task_works_dialog import TaskWorksDialog
from views.edit_task_dialog import EditTaskDialog


class CurrentTasksView(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Your Active Tasks")
        title.setObjectName("Title")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Task Name", "Description", "Priority", "Status", "Actions"])

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        layout.addWidget(self.table)
        self.refresh_data()

    def refresh_data(self):
        self.table.setRowCount(0)
        tasks = database.get_current_tasks(self.user_id)

        for row_idx, task in enumerate(tasks):
            t_id, name, desc, priority = task
            self.table.insertRow(row_idx)

            p_map = {0: ("Low", "#f4f6f6"), 1: ("Medium", "#fcf3cf"), 2: ("High", "#fadbd8")}
            p_text, p_color = p_map.get(priority, ("Unknown", "#ffffff"))

            items = [
                QTableWidgetItem(name),
                QTableWidgetItem(desc),
                QTableWidgetItem(p_text),
                QTableWidgetItem("Active")
            ]

            for col_idx, item in enumerate(items):
                item.setBackground(QColor(p_color))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft if col_idx < 2 else Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

            action_widget = QWidget()
            action_widget.setStyleSheet(f"background-color: {p_color};")

            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(10, 5, 10, 5)
            action_layout.setSpacing(8)

            base_btn_style = """
                QPushButton { 
                    border-radius: 6px; 
                    padding: 6px 12px; 
                    font-weight: bold; 
                    font-size: 12px; 
                }
            """

            btn_works = QPushButton("📝 Log")
            btn_works.setCursor(Qt.PointingHandCursor)
            btn_works.setStyleSheet(
                base_btn_style + "QPushButton { background-color: #34495e; color: white; } QPushButton:hover { background-color: #2c3e50; }")
            btn_works.clicked.connect(lambda ch, tid=t_id, tname=name: self.open_works_dialog(tid, tname))

            btn_edit = QPushButton("✏️ Edit")
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setStyleSheet(
                base_btn_style + "QPushButton { background-color: #3498db; color: white; } QPushButton:hover { background-color: #2980b9; }")
            btn_edit.clicked.connect(lambda ch, tid=t_id, tn=name, td=desc: self.open_edit_dialog(tid, tn, td))

            btn_finish = QPushButton("✅ Done")
            btn_finish.setCursor(Qt.PointingHandCursor)
            btn_finish.setStyleSheet(
                base_btn_style + "QPushButton { background-color: #27ae60; color: white; } QPushButton:hover { background-color: #2ecc71; }")
            btn_finish.clicked.connect(lambda ch, tid=t_id: self.change_status(tid, 1))

            btn_del = QPushButton("🗑️")
            btn_del.setCursor(Qt.PointingHandCursor)
            btn_del.setToolTip("Remove Task")
            btn_del.setStyleSheet(
                base_btn_style + "QPushButton { background-color: #e74c3c; color: white; padding: 6px 10px; } QPushButton:hover { background-color: #c0392b; }")
            btn_del.clicked.connect(lambda ch, tid=t_id: self.change_status(tid, 2))

            action_layout.addWidget(btn_works)
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_finish)
            action_layout.addWidget(btn_del)

            self.table.setCellWidget(row_idx, 4, action_widget)

    def change_status(self, task_id, new_status):
        database.update_task_status(task_id, new_status)
        self.refresh_data()

    def open_works_dialog(self, task_id, task_name):
        dlg = TaskWorksDialog(task_id, task_name, self)
        dlg.exec()

    def open_edit_dialog(self, task_id, current_name, current_desc):
        dlg = EditTaskDialog(task_id, current_name, current_desc, self)
        if dlg.exec():
            self.refresh_data()