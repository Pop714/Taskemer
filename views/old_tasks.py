from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
import database
from views.task_works_dialog import TaskWorksDialog


class OldTasksView(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(15)

        header_layout = QVBoxLayout()
        header_layout.setSpacing(5)

        title = QLabel("Archived & Old Tasks")
        title.setObjectName("Title")
        title.setStyleSheet("font-size: 26px; font-weight: 900; color: #2c3e50;")

        sub_title = QLabel("A history of all tasks you have finished or removed.")
        sub_title.setStyleSheet("color: #7f8c8d; font-size: 14px;")

        header_layout.addWidget(title)
        header_layout.addWidget(sub_title)
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Task Name", "Description", "Priority", "Final Status", "Actions"])

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        self.table.verticalHeader().setDefaultSectionSize(50)

        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)

        layout.addWidget(self.table)

    def refresh_data(self):
        self.table.setRowCount(0)
        tasks = database.get_old_tasks(self.user_id)

        for row_idx, task in enumerate(tasks):
            t_id, name, desc, priority, status = task
            self.table.insertRow(row_idx)

            p_map = {0: "🟢 Low", 1: "🟡 Medium", 2: "🔴 High"}
            p_text = p_map.get(priority, "⚪ Unknown")

            s_map = {
                1: ("✅ Finished", "#f4fdf8", "#27ae60"),
                2: ("🗑️ Removed", "#fdfefe", "#c0392b")
            }
            s_text, bg_color, text_color = s_map.get(status, ("Unknown", "#ffffff", "#333333"))

            item_name = QTableWidgetItem(name)
            item_desc = QTableWidgetItem(desc)
            item_prio = QTableWidgetItem(p_text)

            item_status = QTableWidgetItem(s_text)
            status_font = QFont()
            status_font.setBold(True)
            item_status.setFont(status_font)
            item_status.setForeground(QColor(text_color))

            items = [item_name, item_desc, item_prio, item_status]

            for col_idx, item in enumerate(items):
                item.setBackground(QColor(bg_color))

                alignment = Qt.AlignVCenter | (Qt.AlignCenter if col_idx >= 2 else Qt.AlignLeft)
                item.setTextAlignment(alignment)

                self.table.setItem(row_idx, col_idx, item)

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(10, 5, 10, 5)

            btn_log = QPushButton("📖 View Log")
            btn_log.setCursor(Qt.PointingHandCursor)
            btn_log.setStyleSheet("""
                QPushButton { 
                    background-color: #34495e; 
                    color: white; 
                    border-radius: 6px; 
                    padding: 6px 12px; 
                    font-weight: bold; 
                    font-size: 12px; 
                }
                QPushButton:hover { background-color: #2c3e50; }
            """)
            btn_log.clicked.connect(lambda ch, tid=t_id, tn=name: self.open_works_dialog(tid, tn))

            action_layout.addWidget(btn_log)
            action_widget.setStyleSheet(f"background-color: {bg_color};")

            self.table.setCellWidget(row_idx, 4, action_widget)

    def open_works_dialog(self, task_id, task_name):
        dlg = TaskWorksDialog(task_id, task_name, self)
        dlg.exec()