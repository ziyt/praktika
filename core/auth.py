
from dataclasses import dataclass
from typing import Optional

from .db import get_connection

@dataclass
class CurrentUser:
    user_id: Optional[int]
    full_name: str
    role: str

    @property
    def is_guest(self) -> bool:
        return self.role == "Гость"

    @property
    def is_client(self) -> bool:
        return self.role == "Клиент"

    @property
    def is_manager(self) -> bool:
        return self.role == "Менеджер"

    @property
    def is_admin(self) -> bool:
        return self.role == "Администратор"

    @property
    def can_view_orders(self) -> bool:
        return self.is_manager or self.is_admin

    @property
    def can_edit_products(self) -> bool:
        return self.is_admin

    @property
    def can_filter_sort_search(self) -> bool:
        return self.is_manager or self.is_admin

def guest_user() -> CurrentUser:
    return CurrentUser(user_id=None, full_name="Гость", role="Гость")

def authenticate(login: str, password: str) -> Optional[CurrentUser]:
    conn = get_connection()
    try:
        row = conn.execute(
            """SELECT u.id, u.full_name, r.name AS role
                 FROM users u
                 JOIN roles r ON r.id = u.role_id
                WHERE u.login = ? AND u.password = ?""",
            (login.strip(), password),
        ).fetchone()
        if not row:
            return None
        return CurrentUser(user_id=row["id"], full_name=row["full_name"], role=row["role"])
    finally:
        conn.close()
