
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from core.paths import APP_ICON, DB_PATH
from core.styles import APP_QSS
from ui.login_window import LoginWindow
from ui.products_window import ProductsWindow

class AppController:

    def __init__(self, app: QApplication):
        self.app = app
        self.products_window = None

    def start(self) -> None:
        self._show_login()

    def _show_login(self) -> None:
        dialog = LoginWindow()
        if dialog.exec() and dialog.current_user is not None:
            self._open_products(dialog.current_user)
        else:
            self.app.quit()

    def _open_products(self, user) -> None:
        self.products_window = ProductsWindow(
            user,
            on_logout=self._on_logout,
            on_request_login=self._on_request_login,
        )
        self.products_window.show()

    def _on_logout(self) -> None:
        if self.products_window is not None:
            self.products_window.deleteLater()
            self.products_window = None
        self._show_login()

    def _on_request_login(self) -> None:
        dialog = LoginWindow(parent=self.products_window)
        if dialog.exec() and dialog.current_user is not None:
            new_user = dialog.current_user
            if self.products_window is not None:
                self.products_window.close()
                self.products_window.deleteLater()
                self.products_window = None
            self._open_products(new_user)

def main() -> int:
    if not DB_PATH.exists():
        print(f"База данных не найдена: {DB_PATH}", file=sys.stderr)
        print("Сначала выполните: python3 db/seed.py", file=sys.stderr)
        return 1

    app = QApplication(sys.argv)
    app.setApplicationName("Магазин обуви")
    if APP_ICON.exists():
        app.setWindowIcon(QIcon(str(APP_ICON)))
    app.setStyleSheet(APP_QSS)

    controller = AppController(app)
    controller.start()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
