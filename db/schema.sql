PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT    NOT NULL,
    login     TEXT    NOT NULL UNIQUE,
    password  TEXT    NOT NULL,
    role_id   INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE manufacturers (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE units (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    article         TEXT    PRIMARY KEY,
    name            TEXT    NOT NULL,
    description     TEXT    NOT NULL DEFAULT '',
    photo_path      TEXT,
    price           REAL    NOT NULL CHECK (price >= 0),
    discount        INTEGER NOT NULL DEFAULT 0 CHECK (discount >= 0 AND discount <= 100),
    stock_qty       INTEGER NOT NULL DEFAULT 0 CHECK (stock_qty >= 0),
    category_id     INTEGER NOT NULL,
    manufacturer_id INTEGER NOT NULL,
    supplier_id     INTEGER NOT NULL,
    unit_id         INTEGER NOT NULL,
    FOREIGN KEY (category_id)     REFERENCES categories(id)     ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)  ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (supplier_id)     REFERENCES suppliers(id)      ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (unit_id)         REFERENCES units(id)          ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE pickup_points (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL UNIQUE
);

CREATE TABLE orders (
    id              INTEGER PRIMARY KEY,
    order_date      TEXT    NOT NULL,
    delivery_date   TEXT,
    pickup_point_id INTEGER NOT NULL,
    client_id       INTEGER NOT NULL,
    pickup_code     INTEGER NOT NULL,
    status          TEXT    NOT NULL DEFAULT 'Новый',
    FOREIGN KEY (pickup_point_id) REFERENCES pickup_points(id) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (client_id)       REFERENCES users(id)         ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE order_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL,
    product_article TEXT    NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id)        REFERENCES orders(id)   ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (product_article) REFERENCES products(article) ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX idx_products_category     ON products(category_id);
CREATE INDEX idx_products_supplier     ON products(supplier_id);
CREATE INDEX idx_products_manufacturer ON products(manufacturer_id);
CREATE INDEX idx_order_items_order     ON order_items(order_id);
CREATE INDEX idx_order_items_product   ON order_items(product_article);
CREATE INDEX idx_users_role            ON users(role_id);
