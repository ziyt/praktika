
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from core.auth import CurrentUser
from core.paths import APP_ICON, resolve_photo
from core.repository import (
    delete_product, list_lookup, list_products, product_in_orders,
)

SORT_LABELS = {
    "Без сортировки": None,
    "Кол-во на складе: по возрастанию": "asc",
    "Кол-во на складе: по убыванию": "desc",
}

class ProductCard(QFrame):

    def __init__(self, product: dict, can_edit: bool, can_delete: bool,
                 on_edit, on_delete, parent=None):
        super().__init__(parent)
        self.product = product
        self.setObjectName("card")
        self.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(12)

        photo = QLabel()
        photo.setFixedSize(160, 110)
        photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix = QPixmap(str(resolve_photo(product["photo_path"])))
        if not pix.isNull():
            pix = pix.scaled(
                160, 110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            photo.setPixmap(pix)
        layout.addWidget(photo)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        header = QLabel(f"<b>{product['category']} | {product['name']}</b>")
        header.setTextFormat(Qt.TextFormat.RichText)
        text_layout.addWidget(header)

        text_layout.addWidget(QLabel(f"Описание товара: {product['description']}"))
        text_layout.addWidget(QLabel(f"Производитель: {product['manufacturer']}"))
        text_layout.addWidget(QLabel(f"Поставщик: {product['supplier']}"))
        text_layout.addWidget(self._price_label(product))
        text_layout.addWidget(QLabel(f"Единица измерения: {product['unit']}"))
        text_layout.addWidget(QLabel(f"Количество на складе: {product['stock_qty']}"))
        text_layout.addWidget(QLabel(f"Артикул: {product['article']}"))
        layout.addLayout(text_layout, stretch=1)

        discount_box = QVBoxLayout()
        discount_caption = QLabel("Действующая\nскидка")
        discount_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)
        discount_box.addWidget(discount_caption)
        discount_value = QLabel(f"{product['discount']}%")
        discount_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont()
        f.setPointSize(20)
        f.setBold(True)
        discount_value.setFont(f)
        discount_box.addWidget(discount_value)
        discount_box.addStretch(1)
        discount_host = QWidget()
        discount_host.setLayout(discount_box)
        discount_host.setFixedWidth(120)
        layout.addWidget(discount_host)

        if can_edit or can_delete:
            actions = QVBoxLayout()
            if can_edit:
                edit_btn = QPushButton("Изменить")
                edit_btn.clicked.connect(lambda: on_edit(product["article"]))
                actions.addWidget(edit_btn)
            if can_delete:
                del_btn = QPushButton("Удалить")
                del_btn.clicked.connect(lambda: on_delete(product["article"]))
                actions.addWidget(del_btn)
            actions.addStretch(1)
            layout.addLayout(actions)

        discount = int(product["discount"] or 0)
        out_of_stock = int(product["stock_qty"] or 0) == 0
        if out_of_stock:
            self.setProperty("outOfStock", True)
        elif discount > 15:
            self.setProperty("discountHighlight", True)
        self.style().unpolish(self)
        self.style().polish(self)

    @staticmethod
    def _price_label(product: dict) -> QLabel:
        price = float(product["price"])
        discount = int(product["discount"] or 0)
        if discount > 0:
            final = round(price * (100 - discount) / 100, 2)
            html = (
                f"Цена: <span style='color:#c00;text-decoration:line-through'>"
                f"{price:.2f} ₽</span> "
                f"<span style='color:#000;font-weight:bold'>{final:.2f} ₽</span>"
            )
        else:
            html = f"Цена: {price:.2f} ₽"
        lbl = QLabel(html)
        lbl.setTextFormat(Qt.TextFormat.RichText)
        return lbl

class ProductsWindow(QMainWindow):
    def __init__(self, current_user: CurrentUser, on_logout, on_request_login):
        super().__init__()
        self.current_user = current_user
        self.on_logout = on_logout
        self.on_request_login = on_request_login
        self._edit_window = None

        self.setWindowTitle("Магазин обуви — каталог товаров")
        if APP_ICON.exists():
            self.setWindowIcon(QIcon(str(APP_ICON)))
        self.resize(1100, 720)

        self._build_ui()
        self._reload_suppliers()
        self.reload_products()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        top = QHBoxLayout()
        title = QLabel("Каталог товаров")
        title.setObjectName("header")
        top.addWidget(title)
        top.addStretch(1)

        if self.current_user.can_view_orders:
            orders_btn = QPushButton("Заказы")
            orders_btn.clicked.connect(self._open_orders)
            top.addWidget(orders_btn)

        if self.current_user.can_edit_products:
            add_btn = QPushButton("Добавить товар")
            add_btn.clicked.connect(self._add_product)
            top.addWidget(add_btn)

        user_label = QLabel(f"<b>{self.current_user.full_name}</b> ({self.current_user.role})")
        user_label.setTextFormat(Qt.TextFormat.RichText)
        top.addWidget(user_label)
        if self.current_user.is_guest:
            login_btn = QPushButton("Войти")
            login_btn.clicked.connect(self._request_login)
            top.addWidget(login_btn)
        else:
            logout_btn = QPushButton("Выйти")
            logout_btn.clicked.connect(self._logout)
            top.addWidget(logout_btn)
        root.addLayout(top)

        if self.current_user.can_filter_sort_search:
            controls = QHBoxLayout()
            self.search_edit = QLineEdit()
            self.search_edit.setPlaceholderText("Поиск по всем текстовым полям…")
            controls.addWidget(self.search_edit, stretch=2)

            controls.addWidget(QLabel("Сортировка:"))
            self.sort_combo = QComboBox()
            for label in SORT_LABELS:
                self.sort_combo.addItem(label)
            controls.addWidget(self.sort_combo)

            controls.addWidget(QLabel("Поставщик:"))
            self.supplier_combo = QComboBox()
            controls.addWidget(self.supplier_combo)
            root.addLayout(controls)

            self._debounce = QTimer(self)
            self._debounce.setSingleShot(True)
            self._debounce.setInterval(150)
            self._debounce.timeout.connect(self.reload_products)
            self.search_edit.textChanged.connect(lambda *_: self._debounce.start())
            self.sort_combo.currentIndexChanged.connect(self.reload_products)
            self.supplier_combo.currentIndexChanged.connect(self.reload_products)
        else:
            self.search_edit = None
            self.sort_combo = None
            self.supplier_combo = None

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.cards_host = QWidget()
        self.cards_layout = QVBoxLayout(self.cards_host)
        self.cards_layout.setSpacing(6)
        self.cards_layout.addStretch(1)
        self.scroll.setWidget(self.cards_host)
        root.addWidget(self.scroll, stretch=1)

        self.status_label = QLabel("")
        root.addWidget(self.status_label)

    def _reload_suppliers(self) -> None:
        if self.supplier_combo is None:
            return
        self.supplier_combo.blockSignals(True)
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Все поставщики", None)
        for sup in list_lookup("suppliers"):
            self.supplier_combo.addItem(sup["name"], sup["id"])
        self.supplier_combo.blockSignals(False)

    def reload_products(self) -> None:
        search = ""
        supplier_id = None
        sort = None
        if self.current_user.can_filter_sort_search:
            search = self.search_edit.text().strip()
            supplier_id = self.supplier_combo.currentData()
            sort = SORT_LABELS[self.sort_combo.currentText()]

        try:
            products = list_products(
                search=search, supplier_id=supplier_id, sort_by_stock=sort,
            )
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", str(e))
            return

        while self.cards_layout.count() > 0:
            item = self.cards_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for p in products:
            card = ProductCard(
                p,
                can_edit=self.current_user.can_edit_products,
                can_delete=self.current_user.can_edit_products,
                on_edit=self._edit_product,
                on_delete=self._delete_product,
            )
            self.cards_layout.addWidget(card)
        self.cards_layout.addStretch(1)
        self.status_label.setText(f"Товаров: {len(products)}")

    def _logout(self) -> None:
        self.close()
        self.on_logout()

    def _request_login(self) -> None:
        self.on_request_login()

    def _open_orders(self) -> None:
        from ui.orders_window import OrdersWindow
        self._orders = OrdersWindow(self.current_user, self)
        self._orders.show()

    def _add_product(self) -> None:
        self._open_edit_window(article=None)

    def _edit_product(self, article: str) -> None:
        self._open_edit_window(article=article)

    def _open_edit_window(self, article) -> None:
        if self._edit_window is not None and self._edit_window.isVisible():
            QMessageBox.information(
                self, "Окно уже открыто",
                "Закройте текущее окно редактирования, прежде чем открыть новое.",
            )
            self._edit_window.raise_()
            self._edit_window.activateWindow()
            return
        from ui.product_edit_window import ProductEditWindow
        self._edit_window = ProductEditWindow(article=article, parent=self)
        self._edit_window.saved.connect(self.reload_products)
        self._edit_window.show()

    def _delete_product(self, article: str) -> None:
        if product_in_orders(article):
            QMessageBox.warning(
                self, "Удаление запрещено",
                "Этот товар присутствует в одном или нескольких заказах и не может быть удалён.",
            )
            return
        answer = QMessageBox.question(
            self, "Подтверждение удаления",
            f"Удалить товар «{article}»? Действие нельзя отменить.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            delete_product(article)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка удаления", str(e))
            return
        self.reload_products()
