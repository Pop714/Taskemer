from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame
from views.add_task import AddTaskView
from views.current_tasks import CurrentTasksView
from views.old_tasks import OldTasksView


class DashboardView(QWidget):
    logout_requested = Signal()

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        self.setStyleSheet("background-color: #f4f6f8;")

        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50; 
                border-radius: 15px;
            }
        """)
        s_layout = QVBoxLayout(sidebar)
        s_layout.setContentsMargins(0, 20, 0, 0)

        logo_label = QLabel("🎯 Taskemer")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(
            "font-size: 24px; font-weight: 900; color: white; margin-bottom: 25px; margin-top: 10px;")
        s_layout.addWidget(logo_label)

        self.btn_curr = self.make_nav_btn("📋 Current Tasks")
        self.btn_add = self.make_nav_btn("➕ Add Task")
        self.btn_old = self.make_nav_btn("📁 Old Tasks")

        self.nav_buttons = [self.btn_curr, self.btn_add, self.btn_old]

        s_layout.addWidget(self.btn_curr)
        s_layout.addWidget(self.btn_add)
        s_layout.addWidget(self.btn_old)
        s_layout.addStretch()

        btn_logout = QPushButton("🚪 Logout")
        btn_logout.setCursor(Qt.PointingHandCursor)
        btn_logout.setStyleSheet("""
            QPushButton { 
                background-color: rgba(231, 76, 60, 0.1); color: #e74c3c; 
                padding: 12px 20px; text-align: left; border-radius: 8px; 
                font-size: 15px; font-weight: bold; margin: 10px 15px 20px 15px;
                border: 1px solid rgba(231, 76, 60, 0.3);
            }
            QPushButton:hover { background-color: #e74c3c; color: white; }
        """)
        s_layout.addWidget(btn_logout)

        content_container = QFrame()
        content_container.setStyleSheet("background-color: transparent;")
        c_layout = QVBoxLayout(content_container)
        c_layout.setContentsMargins(0, 0, 0, 0)

        self.content_stack = QStackedWidget()

        self.view_curr = CurrentTasksView(self.user_id)
        self.view_add = AddTaskView(self.user_id)
        self.view_old = OldTasksView(self.user_id)

        self.content_stack.addWidget(self.view_curr)
        self.content_stack.addWidget(self.view_add)
        self.content_stack.addWidget(self.view_old)

        c_layout.addWidget(self.content_stack)

        self.btn_curr.clicked.connect(lambda: self.switch_view(self.view_curr, self.btn_curr))
        self.btn_add.clicked.connect(lambda: self.switch_view(self.view_add, self.btn_add))
        self.btn_old.clicked.connect(lambda: self.switch_view(self.view_old, self.btn_old))
        btn_logout.clicked.connect(self.logout_requested.emit)

        layout.addWidget(sidebar)
        layout.addWidget(content_container)

        self.set_active_button(self.btn_curr)

    @staticmethod
    def make_nav_btn(text):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        return btn

    def set_active_button(self, active_btn):
        default_style = """
            QPushButton { 
                background-color: transparent; color: #bdc3c7; 
                padding: 12px 20px; text-align: left; border-radius: 8px; 
                font-size: 15px; font-weight: bold; margin: 2px 15px;
            }
            QPushButton:hover { background-color: #34495e; color: white; }
        """

        active_style = """
            QPushButton { 
                background-color: #3498db; color: white; 
                padding: 12px 20px; text-align: left; border-radius: 8px; 
                font-size: 15px; font-weight: bold; margin: 2px 15px;
            }
        """

        for btn in self.nav_buttons:
            if btn == active_btn:
                btn.setStyleSheet(active_style)
            else:
                btn.setStyleSheet(default_style)

    def switch_view(self, view_widget, button_widget):
        self.set_active_button(button_widget)

        if hasattr(view_widget, 'refresh_data'):
            view_widget.refresh_data()

        self.content_stack.setCurrentWidget(view_widget)