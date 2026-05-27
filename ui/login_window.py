
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox,
    QPushButton, QVBoxLayout, QWidget,
)

from core.auth import CurrentUser, authenticate, guest_user
from core.paths import APP_ICON, LOGO_IMAGE

class LoginWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Магазин обуви — вход")
        if APP_ICON.exists():
            self.setWindowIcon(QIcon(str(APP_ICON)))
        self.setMinimumWidth(380)
        self.current_user: CurrentUser | None = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        if LOGO_IMAGE.exists():
            logo = QLabel()
            pix = QPixmap(str(LOGO_IMAGE)).scaledToHeight(
                80, Qt.TransformationMode.SmoothTransformation,
            )
            logo.setPixmap(pix)
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            root.addWidget(logo)

        title = QLabel("ООО «Обувь»")
        title.setObjectName("header")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        form = QFormLayout()
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Логин")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Пароль")
        form.addRow("Логин:", self.login_edit)
        form.addRow("Пароль:", self.password_edit)
        root.addLayout(form)

        buttons = QHBoxLayout()
        self.login_button = QPushButton("Войти")
        self.guest_button = QPushButton("Войти как гость")
        buttons.addWidget(self.login_button)
        buttons.addWidget(self.guest_button)
        root.addLayout(buttons)

        self.login_button.clicked.connect(self._on_login)
        self.guest_button.clicked.connect(self._on_guest)
        self.password_edit.returnPressed.connect(self._on_login)
        self.login_edit.returnPressed.connect(self.password_edit.setFocus)

    def _on_login(self) -> None:
        login = self.login_edit.text().strip()
        password = self.password_edit.text()
        if not login or not password:
            QMessageBox.warning(
                self, "Заполните поля",
                "Введите логин и пароль или войдите как гость.",
            )
            return
        user = authenticate(login, password)
        if user is None:
            QMessageBox.critical(
                self, "Ошибка авторизации",
                "Неверный логин или пароль. Проверьте раскладку клавиатуры.",
            )
            self.password_edit.clear()
            self.password_edit.setFocus()
            return
        self.current_user = user
        self.accept()

    def _on_guest(self) -> None:
        self.current_user = guest_user()
        self.accept()
