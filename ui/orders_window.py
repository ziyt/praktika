
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QAbstractItemView, QHBoxLayout, QLabel, QMainWindow, QMessageBox,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
)

from core.auth import CurrentUser
from core.paths import APP_ICON
from core.repository import list_orders, order_items

ORDER_COLUMNS = [
    "ID", "Дата заказа", "Дата доставки", "Клиент",
    "Пункт выдачи", "Код получения", "Статус",
]
ITEM_COLUMNS = ["Артикул", "Наименование", "Кол-во", "Цена"]

class OrdersWindow(QMainWindow):
    def __init__(self, current_user: CurrentUser, parent=None):
        super().__init__(parent)
        self.current_user = current_user
        self.setWindowTitle("Магазин обуви — заказы")
        if APP_ICON.exists():
            self.setWindowIcon(QIcon(str(APP_ICON)))
        self.resize(1000, 620)
        self._build_ui()
        self._load_orders()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        top = QHBoxLayout()
        title = QLabel("Список заказов")
        title.setObjectName("header")
        top.addWidget(title)
        top.addStretch(1)
        back = QPushButton("Назад")
        back.clicked.connect(self.close)
        top.addWidget(back)
        root.addLayout(top)

        self.orders_table = QTableWidget(0, len(ORDER_COLUMNS))
        self.orders_table.setHorizontalHeaderLabels(ORDER_COLUMNS)
        self.orders_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.orders_table.horizontalHeader().setStretchLastSection(True)
        self.orders_table.itemSelectionChanged.connect(self._load_items)
        root.addWidget(self.orders_table, stretch=2)

        root.addWidget(QLabel("Состав выбранного заказа:"))
        self.items_table = QTableWidget(0, len(ITEM_COLUMNS))
        self.items_table.setHorizontalHeaderLabels(ITEM_COLUMNS)
        self.items_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.items_table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.items_table, stretch=1)

    def _load_orders(self) -> None:
        try:
            data = list_orders()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки заказов", str(e))
            return
        self.orders_table.setRowCount(len(data))
        for r, o in enumerate(data):
            values = [
                str(o["id"]), o["order_date"] or "", o["delivery_date"] or "",
                o["client_name"], o["pickup_address"],
                str(o["pickup_code"]), o["status"],
            ]
            for c, v in enumerate(values):
                item = QTableWidgetItem(v)
                if c == 0:
                    item.setData(Qt.ItemDataRole.UserRole, o["id"])
                self.orders_table.setItem(r, c, item)
        self.orders_table.resizeColumnsToContents()

    def _load_items(self) -> None:
        rows = self.orders_table.selectionModel().selectedRows()
        if not rows:
            self.items_table.setRowCount(0)
            return
        row = rows[0].row()
        order_id = self.orders_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        try:
            items = order_items(order_id)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
            return
        self.items_table.setRowCount(len(items))
        for r, it in enumerate(items):
            cells = [
                it["product_article"], it["product_name"],
                str(it["quantity"]), f"{float(it['price']):.2f} ₽",
            ]
            for c, v in enumerate(cells):
                self.items_table.setItem(r, c, QTableWidgetItem(v))
        self.items_table.resizeColumnsToContents()
