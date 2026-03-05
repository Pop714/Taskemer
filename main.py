import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
import database
from styles import THEME
from views.login import LoginView
from views.dashboard import DashboardView

class TaskemerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taskemer - Task Management")
        self.setMinimumSize(1000, 650)
        self.setStyleSheet(THEME)

        database.init_db()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.login_view = LoginView()
        self.login_view.login_successful.connect(self.load_dashboard)
        self.stack.addWidget(self.login_view)

    def load_dashboard(self, user_id):
        self.dashboard_view = DashboardView(user_id, self)
        self.dashboard_view.logout_requested.connect(self.logout)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentWidget(self.dashboard_view)

    def logout(self):
        self.stack.removeWidget(self.dashboard_view)
        self.dashboard_view.deleteLater()
        self.stack.setCurrentWidget(self.login_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))

    window = TaskemerApp()
    window.show()
    sys.exit(app.exec())