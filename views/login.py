import os
from PySide6.QtCore import Signal, Qt, QEvent
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QMessageBox, QFrame
)
from PySide6.QtGui import QPixmap
import database


class LoginView(QWidget):
    login_successful = Signal(int)

    def __init__(self):
        super().__init__()

        self.setObjectName("LoginScreen")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("QWidget#LoginScreen { background-color: #ffffff; }")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setFixedSize(400, 500)
        card.setStyleSheet("QFrame { background-color: transparent; border: none; }")

        c_layout = QVBoxLayout(card)
        c_layout.setContentsMargins(20, 20, 20, 20)
        c_layout.setSpacing(15)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        logo_path = os.path.join("assets", "logo.png")

        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaledToHeight(85, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("🎯")
            self.logo_label.setStyleSheet("font-size: 55px; background: transparent;")

        c_layout.addWidget(self.logo_label)
        c_layout.addSpacing(15)

        title = QLabel("Welcome Back")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 26px; font-weight: 900; color: #111827; background: transparent;")

        subtitle = QLabel("Please enter your details to sign in.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #6b7280; margin-bottom: 15px; background: transparent;")

        c_layout.addWidget(title)
        c_layout.addWidget(subtitle)

        input_style = """
            QLineEdit {
                padding: 12px 15px;
                border: 1.5px solid #e5e7eb;
                border-radius: 10px;
                background-color: #f9fafb;
                font-size: 14px;
                color: #111827;
            }
            QLineEdit:focus {
                border: 1.5px solid #3b82f6;
                background-color: #ffffff;
            }
        """

        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setFixedHeight(48)
        self.username.setStyleSheet(input_style)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedHeight(48)
        self.password.setStyleSheet(input_style)

        self.username.returnPressed.connect(self.handle_login)
        self.password.returnPressed.connect(self.handle_login)

        self.username.installEventFilter(self)
        self.password.installEventFilter(self)

        c_layout.addWidget(self.username)
        c_layout.addWidget(self.password)
        c_layout.addSpacing(15)

        btn_login = QPushButton("Sign In")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.setFixedHeight(48)
        btn_login.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border-radius: 10px;
                font-weight: bold;
                font-size: 15px;
                border: none;
            }
            QPushButton:hover { background-color: #2563eb; }
            QPushButton:pressed { background-color: #1d4ed8; }
        """)
        btn_login.clicked.connect(self.handle_login)
        c_layout.addWidget(btn_login)

        register_layout = QHBoxLayout()
        register_layout.setAlignment(Qt.AlignCenter)

        lbl_new = QLabel("Don't have an account?")
        lbl_new.setStyleSheet("color: #6b7280; font-size: 13px; background: transparent;")

        btn_register = QPushButton("Create one")
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #3b82f6;
                font-weight: bold;
                font-size: 13px;
                border: none;
                text-align: left;
            }
            QPushButton:hover { color: #2563eb; text-decoration: underline; }
        """)
        btn_register.clicked.connect(self.handle_register)

        register_layout.addWidget(lbl_new)
        register_layout.addWidget(btn_register)

        c_layout.addStretch()
        c_layout.addLayout(register_layout)

        layout.addWidget(card)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down and obj == self.username:
                self.password.setFocus()
                return True  # Consume the event
            elif event.key() == Qt.Key_Up and obj == self.password:
                self.username.setFocus()
                return True  # Consume the event

        return super().eventFilter(obj, event)

    def handle_login(self):
        u, p = self.username.text(), self.password.text()
        user_id = database.authenticate(u, p)
        if user_id:
            self.login_successful.emit(user_id)
            self.username.clear()
            self.password.clear()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.\nPlease try again.")

    def handle_register(self):
        u, p = self.username.text(), self.password.text()
        if not u or not p:
            QMessageBox.warning(self, "Registration Error",
                                "Please fill in both username and password fields to register.")
            return

        if database.add_user(u, p):
            QMessageBox.information(self, "Welcome!",
                                    "Your account has been created successfully.\nYou can now sign in.")
        else:
            QMessageBox.warning(self, "Registration Error",
                                "That username is already taken. Please choose another one.")