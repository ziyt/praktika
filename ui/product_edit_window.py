
from typing import Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QComboBox, QDialog, QDoubleSpinBox, QFileDialog, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPlainTextEdit, QPushButton, QSpinBox,
    QVBoxLayout,
)

from core.image_utils import import_product_photo, remove_product_photo
from core.paths import APP_DIR, APP_ICON, resolve_photo
from core.repository import (
    get_product, insert_product, list_lookup, next_article_suggestion,
    update_product,
)

class ProductEditWindow(QDialog):

    saved = pyqtSignal()

    def __init__(self, article: Optional[str], parent=None):
        super().__init__(parent)
        self.article = article
        self.is_edit = article is not None
        self.original_photo_path = None
        self.new_photo_source = None

        title = "Редактирование товара" if self.is_edit else "Добавление товара"
        self.setWindowTitle(f"Магазин обуви — {title}")
        if APP_ICON.exists():
            self.setWindowIcon(QIcon(str(APP_ICON)))
        self.setMinimumWidth(520)
        self._build_ui()
        self._load_lookups()
        if self.is_edit:
            self._load_existing()
        else:
            self.article_edit.setText(next_article_suggestion())
            self.article_edit.setReadOnly(False)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        form = QFormLayout()

        self.article_edit = QLineEdit()
        self.article_edit.setReadOnly(True)
        form.addRow("Артикул (ID):", self.article_edit)

        self.name_edit = QLineEdit()
        form.addRow("Наименование:", self.name_edit)

        self.category_combo = QComboBox()
        form.addRow("Категория:", self.category_combo)

        self.manufacturer_combo = QComboBox()
        form.addRow("Производитель:", self.manufacturer_combo)

        self.supplier_combo = QComboBox()
        form.addRow("Поставщик:", self.supplier_combo)

        self.unit_combo = QComboBox()
        form.addRow("Единица измерения:", self.unit_combo)

        self.description_edit = QPlainTextEdit()
        self.description_edit.setFixedHeight(80)
        form.addRow("Описание:", self.description_edit)

        self.price_spin = QDoubleSpinBox()
        self.price_spin.setMaximum(10_000_000)
        self.price_spin.setMinimum(0)
        self.price_spin.setDecimals(2)
        self.price_spin.setSuffix(" ₽")
        form.addRow("Цена:", self.price_spin)

        self.discount_spin = QSpinBox()
        self.discount_spin.setRange(0, 100)
        self.discount_spin.setSuffix(" %")
        form.addRow("Действующая скидка:", self.discount_spin)

        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 1_000_000)
        form.addRow("Количество на складе:", self.stock_spin)

        photo_box = QHBoxLayout()
        self.photo_preview = QLabel()
        self.photo_preview.setFixedSize(160, 110)
        self.photo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_preview.setStyleSheet("border: 1px solid #999;")
        photo_box.addWidget(self.photo_preview)

        photo_buttons = QVBoxLayout()
        choose_btn = QPushButton("Выбрать фото…")
        choose_btn.clicked.connect(self._choose_photo)
        clear_btn = QPushButton("Без фото")
        clear_btn.clicked.connect(self._clear_photo)
        photo_buttons.addWidget(choose_btn)
        photo_buttons.addWidget(clear_btn)
        photo_buttons.addStretch(1)
        photo_box.addLayout(photo_buttons)
        form.addRow("Фото товара:", photo_box)

        root.addLayout(form)

        actions = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        actions.addStretch(1)
        actions.addWidget(self.save_btn)
        actions.addWidget(self.cancel_btn)
        root.addLayout(actions)

        self.save_btn.clicked.connect(self._on_save)
        self.cancel_btn.clicked.connect(self.reject)

        self._update_preview(None)

    def _load_lookups(self) -> None:
        for combo, table in [
            (self.category_combo, "categories"),
            (self.manufacturer_combo, "manufacturers"),
            (self.supplier_combo, "suppliers"),
            (self.unit_combo, "units"),
        ]:
            combo.clear()
            for row in list_lookup(table):
                combo.addItem(row["name"], row["id"])

    def _load_existing(self) -> None:
        data = get_product(self.article)
        if data is None:
            QMessageBox.critical(self, "Ошибка", "Товар не найден.")
            self.reject()
            return
        self.article_edit.setText(data["article"])
        self.article_edit.setReadOnly(True)
        self.name_edit.setText(data["name"])
        self.description_edit.setPlainText(data["description"] or "")
        self.price_spin.setValue(float(data["price"]))
        self.discount_spin.setValue(int(data["discount"]))
        self.stock_spin.setValue(int(data["stock_qty"]))
        self._set_combo_by_id(self.category_combo, data["category_id"])
        self._set_combo_by_id(self.manufacturer_combo, data["manufacturer_id"])
        self._set_combo_by_id(self.supplier_combo, data["supplier_id"])
        self._set_combo_by_id(self.unit_combo, data["unit_id"])
        self.original_photo_path = data["photo_path"]
        self._update_preview(data["photo_path"])

    @staticmethod
    def _set_combo_by_id(combo: QComboBox, id_value) -> None:
        for i in range(combo.count()):
            if combo.itemData(i) == id_value:
                combo.setCurrentIndex(i)
                return

    def _choose_photo(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Выберите изображение", str(APP_DIR),
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)",
        )
        if not path:
            return
        self.new_photo_source = path
        self._update_preview(path)

    def _clear_photo(self) -> None:
        self.new_photo_source = ""
        self._update_preview(None)

    def _update_preview(self, path_or_relative) -> None:
        if path_or_relative is None:
            target = resolve_photo(None)
        elif isinstance(path_or_relative, str) and "/" not in path_or_relative \
                and "\\" not in path_or_relative:
            target = resolve_photo(path_or_relative)
        else:
            from pathlib import Path as _P
            p = _P(path_or_relative)
            target = p if p.is_absolute() else resolve_photo(path_or_relative)
        pix = QPixmap(str(target))
        if pix.isNull():
            self.photo_preview.setText("нет фото")
        else:
            self.photo_preview.setPixmap(pix.scaled(
                160, 110,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ))

    def _validate(self):
        errors = []
        if not self.article_edit.text().strip():
            errors.append("Артикул не может быть пустым.")
        if not self.name_edit.text().strip():
            errors.append("Введите наименование товара.")
        if self.category_combo.currentData() is None:
            errors.append("Выберите категорию.")
        if self.manufacturer_combo.currentData() is None:
            errors.append("Выберите производителя.")
        if self.supplier_combo.currentData() is None:
            errors.append("Выберите поставщика.")
        if self.unit_combo.currentData() is None:
            errors.append("Выберите единицу измерения.")
        return errors

    def _on_save(self) -> None:
        errors = self._validate()
        if errors:
            QMessageBox.warning(self, "Заполнены не все поля", "\n".join(errors))
            return

        new_photo_path = self.original_photo_path
        if self.new_photo_source == "":
            if self.original_photo_path:
                remove_product_photo(self.original_photo_path)
            new_photo_path = None
        elif self.new_photo_source:
            try:
                new_photo_path = import_product_photo(self.new_photo_source)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка загрузки фото", str(e))
                return
            if self.original_photo_path and self.original_photo_path != new_photo_path:
                remove_product_photo(self.original_photo_path)

        data = {
            "article":          self.article_edit.text().strip(),
            "name":             self.name_edit.text().strip(),
            "description":      self.description_edit.toPlainText().strip(),
            "photo_path":       new_photo_path,
            "price":            float(self.price_spin.value()),
            "discount":         int(self.discount_spin.value()),
            "stock_qty":        int(self.stock_spin.value()),
            "category_id":      self.category_combo.currentData(),
            "manufacturer_id":  self.manufacturer_combo.currentData(),
            "supplier_id":      self.supplier_combo.currentData(),
            "unit_id":          self.unit_combo.currentData(),
        }

        try:
            if self.is_edit:
                update_product(data)
            else:
                insert_product(data)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка сохранения", str(e))
            return

        self.saved.emit()
        self.accept()
