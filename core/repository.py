
from typing import Optional

from .db import get_connection

def list_products(search: str = "",
                  supplier_id: Optional[int] = None,
                  sort_by_stock: Optional[str] = None) -> list:
    """Получить список товаров.

    sort_by_stock — None | 'asc' | 'desc'.
    Поиск — по всем текстовым полям одновременно (article/name/description
    и связанным справочникам).
    """
    sql = ["""SELECT p.article, p.name, p.description, p.photo_path,
                     p.price, p.discount, p.stock_qty,
                     c.name AS category,
                     m.name AS manufacturer,
                     s.name AS supplier,
                     u.name AS unit,
                     p.category_id, p.manufacturer_id, p.supplier_id, p.unit_id
                FROM products p
                JOIN categories    c ON c.id = p.category_id
                JOIN manufacturers m ON m.id = p.manufacturer_id
                JOIN suppliers     s ON s.id = p.supplier_id
                JOIN units         u ON u.id = p.unit_id"""]
    where = []
    params = []
    if supplier_id is not None:
        where.append("p.supplier_id = ?")
        params.append(supplier_id)
    if search:
        like = f"%{search.lower()}%"
        where.append("""(
            LOWER(p.article)     LIKE ? OR
            LOWER(p.name)        LIKE ? OR
            LOWER(p.description) LIKE ? OR
            LOWER(c.name)        LIKE ? OR
            LOWER(m.name)        LIKE ? OR
            LOWER(s.name)        LIKE ? OR
            LOWER(u.name)        LIKE ?
        )""")
        params.extend([like] * 7)
    if where:
        sql.append("WHERE " + " AND ".join(where))
    if sort_by_stock == "asc":
        sql.append("ORDER BY p.stock_qty ASC, p.name")
    elif sort_by_stock == "desc":
        sql.append("ORDER BY p.stock_qty DESC, p.name")
    else:
        sql.append("ORDER BY p.name")

    conn = get_connection()
    try:
        return [dict(row) for row in conn.execute(" ".join(sql), params).fetchall()]
    finally:
        conn.close()

def get_product(article: str) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            """SELECT p.article, p.name, p.description, p.photo_path,
                      p.price, p.discount, p.stock_qty,
                      p.category_id, p.manufacturer_id, p.supplier_id, p.unit_id
                 FROM products p WHERE p.article = ?""",
            (article,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def list_lookup(table: str) -> list:
    conn = get_connection()
    try:
        rows = conn.execute(f"SELECT id, name FROM {table} ORDER BY name").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def next_article_suggestion() -> str:
    conn = get_connection()
    try:
        n = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        return f"NEW{n + 1:04d}"
    finally:
        conn.close()

def insert_product(data: dict) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO products(article, name, description, photo_path,
                                    price, discount, stock_qty,
                                    category_id, manufacturer_id, supplier_id, unit_id)
               VALUES (:article, :name, :description, :photo_path,
                       :price, :discount, :stock_qty,
                       :category_id, :manufacturer_id, :supplier_id, :unit_id)""",
            data,
        )
        conn.commit()
    finally:
        conn.close()

def update_product(data: dict) -> None:
    conn = get_connection()
    try:
        conn.execute(
            """UPDATE products
                  SET name = :name,
                      description = :description,
                      photo_path = :photo_path,
                      price = :price,
                      discount = :discount,
                      stock_qty = :stock_qty,
                      category_id = :category_id,
                      manufacturer_id = :manufacturer_id,
                      supplier_id = :supplier_id,
                      unit_id = :unit_id
                WHERE article = :article""",
            data,
        )
        conn.commit()
    finally:
        conn.close()

def product_in_orders(article: str) -> bool:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT 1 FROM order_items WHERE product_article = ? LIMIT 1",
            (article,),
        ).fetchone()
        return row is not None
    finally:
        conn.close()

def delete_product(article: str) -> None:
    conn = get_connection()
    try:
        conn.execute("DELETE FROM products WHERE article = ?", (article,))
        conn.commit()
    finally:
        conn.close()

def list_orders() -> list:
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT o.id, o.order_date, o.delivery_date,
                      o.pickup_code, o.status,
                      pp.address AS pickup_address,
                      u.full_name AS client_name
                 FROM orders o
                 JOIN pickup_points pp ON pp.id = o.pickup_point_id
                 JOIN users u ON u.id = o.client_id
                ORDER BY o.id"""
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def order_items(order_id: int) -> list:
    conn = get_connection()
    try:
        rows = conn.execute(
            """SELECT oi.product_article, oi.quantity,
                      p.name AS product_name, p.price
                 FROM order_items oi
                 JOIN products p ON p.article = oi.product_article
                WHERE oi.order_id = ?""",
            (order_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
