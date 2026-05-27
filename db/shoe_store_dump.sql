BEGIN TRANSACTION;
CREATE TABLE categories (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "categories" VALUES(1,'Женская обувь');
INSERT INTO "categories" VALUES(2,'Мужская обувь');
CREATE TABLE manufacturers (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "manufacturers" VALUES(1,'Kari');
INSERT INTO "manufacturers" VALUES(2,'Marco Tozzi');
INSERT INTO "manufacturers" VALUES(3,'Рос');
INSERT INTO "manufacturers" VALUES(4,'Rieker');
INSERT INTO "manufacturers" VALUES(5,'Alessio Nesca');
INSERT INTO "manufacturers" VALUES(6,'CROSBY');
CREATE TABLE order_items (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id        INTEGER NOT NULL,
    product_article TEXT    NOT NULL,
    quantity        INTEGER NOT NULL CHECK (quantity > 0),
    FOREIGN KEY (order_id)        REFERENCES orders(id)   ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (product_article) REFERENCES products(article) ON UPDATE CASCADE ON DELETE RESTRICT
);
INSERT INTO "order_items" VALUES(1,1,'А112Т4',2);
INSERT INTO "order_items" VALUES(2,1,'F635R4',2);
INSERT INTO "order_items" VALUES(3,2,'H782T5',1);
INSERT INTO "order_items" VALUES(4,2,'G783F5',1);
INSERT INTO "order_items" VALUES(5,3,'J384T6',10);
INSERT INTO "order_items" VALUES(6,3,'D572U8',10);
INSERT INTO "order_items" VALUES(7,4,'F572H7',5);
INSERT INTO "order_items" VALUES(8,4,'D329H3',4);
INSERT INTO "order_items" VALUES(9,5,'А112Т4',2);
INSERT INTO "order_items" VALUES(10,5,'F635R4',2);
INSERT INTO "order_items" VALUES(11,6,'H782T5',1);
INSERT INTO "order_items" VALUES(12,6,'G783F5',1);
INSERT INTO "order_items" VALUES(13,7,'J384T6',10);
INSERT INTO "order_items" VALUES(14,7,'D572U8',10);
INSERT INTO "order_items" VALUES(15,8,'F572H7',5);
INSERT INTO "order_items" VALUES(16,8,'D329H3',4);
INSERT INTO "order_items" VALUES(17,9,'B320R5',5);
INSERT INTO "order_items" VALUES(18,9,'G432E4',1);
INSERT INTO "order_items" VALUES(19,10,'S213E3',5);
INSERT INTO "order_items" VALUES(20,10,'E482R4',5);
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
INSERT INTO "orders" VALUES(1,'2025-02-27','2025-04-20',1,4,901,'Завершен');
INSERT INTO "orders" VALUES(2,'2022-09-28','2025-04-21',11,1,902,'Завершен');
INSERT INTO "orders" VALUES(3,'2025-03-21','2025-04-22',2,2,903,'Завершен');
INSERT INTO "orders" VALUES(4,'2025-02-20','2025-04-23',11,3,904,'Завершен');
INSERT INTO "orders" VALUES(5,'2025-03-17','2025-04-24',2,4,905,'Завершен');
INSERT INTO "orders" VALUES(6,'2025-03-01','2025-04-25',15,1,906,'Завершен');
INSERT INTO "orders" VALUES(7,'30.02.2025','2025-04-26',3,2,907,'Завершен');
INSERT INTO "orders" VALUES(8,'2025-03-31','2025-04-27',19,3,908,'Новый');
INSERT INTO "orders" VALUES(9,'2025-04-02','2025-04-28',5,4,909,'Новый');
INSERT INTO "orders" VALUES(10,'2025-04-03','2025-04-29',19,4,910,'Новый');
CREATE TABLE pickup_points (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL UNIQUE
);
INSERT INTO "pickup_points" VALUES(1,'420151, г. Лесной, ул. Вишневая, 32');
INSERT INTO "pickup_points" VALUES(2,'125061, г. Лесной, ул. Подгорная, 8');
INSERT INTO "pickup_points" VALUES(3,'630370, г. Лесной, ул. Шоссейная, 24');
INSERT INTO "pickup_points" VALUES(4,'400562, г. Лесной, ул. Зеленая, 32');
INSERT INTO "pickup_points" VALUES(5,'614510, г. Лесной, ул. Маяковского, 47');
INSERT INTO "pickup_points" VALUES(6,'410542, г. Лесной, ул. Светлая, 46');
INSERT INTO "pickup_points" VALUES(7,'620839, г. Лесной, ул. Цветочная, 8');
INSERT INTO "pickup_points" VALUES(8,'443890, г. Лесной, ул. Коммунистическая, 1');
INSERT INTO "pickup_points" VALUES(9,'603379, г. Лесной, ул. Спортивная, 46');
INSERT INTO "pickup_points" VALUES(10,'603721, г. Лесной, ул. Гоголя, 41');
INSERT INTO "pickup_points" VALUES(11,'410172, г. Лесной, ул. Северная, 13');
INSERT INTO "pickup_points" VALUES(12,'614611, г. Лесной, ул. Молодежная, 50');
INSERT INTO "pickup_points" VALUES(13,'454311, г.Лесной, ул. Новая, 19');
INSERT INTO "pickup_points" VALUES(14,'660007, г.Лесной, ул. Октябрьская, 19');
INSERT INTO "pickup_points" VALUES(15,'603036, г. Лесной, ул. Садовая, 4');
INSERT INTO "pickup_points" VALUES(16,'394060, г.Лесной, ул. Фрунзе, 43');
INSERT INTO "pickup_points" VALUES(17,'410661, г. Лесной, ул. Школьная, 50');
INSERT INTO "pickup_points" VALUES(18,'625590, г. Лесной, ул. Коммунистическая, 20');
INSERT INTO "pickup_points" VALUES(19,'625683, г. Лесной, ул. 8 Марта');
INSERT INTO "pickup_points" VALUES(20,'450983, г.Лесной, ул. Комсомольская, 26');
INSERT INTO "pickup_points" VALUES(21,'394782, г. Лесной, ул. Чехова, 3');
INSERT INTO "pickup_points" VALUES(22,'603002, г. Лесной, ул. Дзержинского, 28');
INSERT INTO "pickup_points" VALUES(23,'450558, г. Лесной, ул. Набережная, 30');
INSERT INTO "pickup_points" VALUES(24,'344288, г. Лесной, ул. Чехова, 1');
INSERT INTO "pickup_points" VALUES(25,'614164, г.Лесной,  ул. Степная, 30');
INSERT INTO "pickup_points" VALUES(26,'394242, г. Лесной, ул. Коммунистическая, 43');
INSERT INTO "pickup_points" VALUES(27,'660540, г. Лесной, ул. Солнечная, 25');
INSERT INTO "pickup_points" VALUES(28,'125837, г. Лесной, ул. Шоссейная, 40');
INSERT INTO "pickup_points" VALUES(29,'125703, г. Лесной, ул. Партизанская, 49');
INSERT INTO "pickup_points" VALUES(30,'625283, г. Лесной, ул. Победы, 46');
INSERT INTO "pickup_points" VALUES(31,'614753, г. Лесной, ул. Полевая, 35');
INSERT INTO "pickup_points" VALUES(32,'426030, г. Лесной, ул. Маяковского, 44');
INSERT INTO "pickup_points" VALUES(33,'450375, г. Лесной ул. Клубная, 44');
INSERT INTO "pickup_points" VALUES(34,'625560, г. Лесной, ул. Некрасова, 12');
INSERT INTO "pickup_points" VALUES(35,'630201, г. Лесной, ул. Комсомольская, 17');
INSERT INTO "pickup_points" VALUES(36,'190949, г. Лесной, ул. Мичурина, 26');
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
INSERT INTO "products" VALUES('А112Т4','Ботинки','Женские Ботинки демисезонные kari','resources/products/1.jpg',4990.0,3,6,1,1,1,1);
INSERT INTO "products" VALUES('F635R4','Ботинки','Ботинки Marco Tozzi женские демисезонные, размер 39, цвет бежевый','resources/products/2.jpg',3244.0,2,13,1,2,2,1);
INSERT INTO "products" VALUES('H782T5','Туфли','Туфли kari мужские классика MYZ21AW-450A, размер 43, цвет: черный','resources/products/3.jpg',4499.0,4,5,2,1,1,1);
INSERT INTO "products" VALUES('G783F5','Ботинки','Мужские ботинки Рос-Обувь кожаные с натуральным мехом','resources/products/4.jpg',5900.0,2,8,2,3,1,1);
INSERT INTO "products" VALUES('J384T6','Ботинки','B3430/14 Полуботинки мужские Rieker','resources/products/5.jpg',3800.0,2,16,2,4,2,1);
INSERT INTO "products" VALUES('D572U8','Кроссовки','129615-4 Кроссовки мужские','resources/products/6.jpg',4100.0,3,6,2,3,2,1);
INSERT INTO "products" VALUES('F572H7','Туфли','Туфли Marco Tozzi женские летние, размер 39, цвет черный','resources/products/7.jpg',2700.0,2,14,1,2,1,1);
INSERT INTO "products" VALUES('D329H3','Полуботинки','Полуботинки Alessio Nesca женские 3-30797-47, размер 37, цвет: бордовый','resources/products/8.jpg',1890.0,4,4,1,5,2,1);
INSERT INTO "products" VALUES('B320R5','Туфли','Туфли Rieker женские демисезонные, размер 41, цвет коричневый','resources/products/9.jpg',4300.0,2,6,1,4,1,1);
INSERT INTO "products" VALUES('G432E4','Туфли','Туфли kari женские TR-YR-413017, размер 37, цвет: черный','resources/products/10.jpg',2800.0,3,15,1,1,1,1);
INSERT INTO "products" VALUES('S213E3','Полуботинки','407700/01-01 Полуботинки мужские CROSBY',NULL,2156.0,3,6,2,6,2,1);
INSERT INTO "products" VALUES('E482R4','Полуботинки','Полуботинки kari женские MYZ20S-149, размер 41, цвет: черный',NULL,1800.0,2,14,1,1,1,1);
INSERT INTO "products" VALUES('S634B5','Кеды','Кеды Caprice мужские демисезонные, размер 42, цвет черный',NULL,5500.0,3,0,2,6,2,1);
INSERT INTO "products" VALUES('K345R4','Полуботинки','407700/01-02 Полуботинки мужские CROSBY',NULL,2100.0,2,3,2,6,2,1);
INSERT INTO "products" VALUES('O754F4','Туфли','Туфли женские демисезонные Rieker артикул 55073-68/37',NULL,5400.0,4,18,1,4,2,1);
INSERT INTO "products" VALUES('G531F4','Ботинки','Ботинки женские зимние ROMER арт. 893167-01 Черный',NULL,6600.0,12,9,1,1,1,1);
INSERT INTO "products" VALUES('J542F5','Тапочки','Тапочки мужские Арт.70701-55-67син р.41',NULL,500.0,13,0,2,1,1,1);
INSERT INTO "products" VALUES('B431R5','Ботинки','Мужские кожаные ботинки/мужские ботинки',NULL,2700.0,2,5,2,4,2,1);
INSERT INTO "products" VALUES('P764G4','Туфли','Туфли женские, ARGO, размер 38',NULL,6800.0,15,15,1,6,1,1);
INSERT INTO "products" VALUES('C436G5','Ботинки','Ботинки женские, ARGO, размер 40',NULL,10200.0,15,9,1,5,1,1);
INSERT INTO "products" VALUES('F427R5','Ботинки','Ботинки на молнии с декоративной пряжкой FRAU',NULL,11800.0,15,11,1,4,2,1);
INSERT INTO "products" VALUES('N457T5','Полуботинки','Полуботинки Ботинки черные зимние, мех',NULL,4600.0,3,13,1,6,1,1);
INSERT INTO "products" VALUES('D364R4','Туфли','Туфли Luiza Belly женские Kate-lazo черные из натуральной замши',NULL,12400.0,16,5,1,1,1,1);
INSERT INTO "products" VALUES('S326R5','Тапочки','Мужские кожаные тапочки "Профиль С.Дали"',NULL,9900.0,17,15,2,6,2,1);
INSERT INTO "products" VALUES('L754R4','Полуботинки','Полуботинки kari женские WB2020SS-26, размер 38, цвет: черный',NULL,1700.0,2,7,1,1,1,1);
INSERT INTO "products" VALUES('M542T5','Кроссовки','Кроссовки мужские TOFA',NULL,2800.0,18,3,2,4,2,1);
INSERT INTO "products" VALUES('D268G5','Туфли','Туфли Rieker женские демисезонные, размер 36, цвет коричневый',NULL,4399.0,3,12,1,4,2,1);
INSERT INTO "products" VALUES('T324F5','Сапоги','Сапоги замша Цвет: синий',NULL,4699.0,2,5,1,6,1,1);
INSERT INTO "products" VALUES('K358H6','Тапочки','Тапочки мужские син р.41',NULL,599.0,20,2,2,4,1,1);
INSERT INTO "products" VALUES('H535R5','Ботинки','Женские Ботинки демисезонные',NULL,2300.0,2,7,1,4,2,1);
CREATE TABLE roles (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "roles" VALUES(1,'Гость');
INSERT INTO "roles" VALUES(2,'Клиент');
INSERT INTO "roles" VALUES(3,'Менеджер');
INSERT INTO "roles" VALUES(4,'Администратор');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('roles',4);
INSERT INTO "sqlite_sequence" VALUES('users',10);
INSERT INTO "sqlite_sequence" VALUES('pickup_points',36);
INSERT INTO "sqlite_sequence" VALUES('categories',2);
INSERT INTO "sqlite_sequence" VALUES('manufacturers',6);
INSERT INTO "sqlite_sequence" VALUES('suppliers',2);
INSERT INTO "sqlite_sequence" VALUES('units',1);
INSERT INTO "sqlite_sequence" VALUES('order_items',20);
CREATE TABLE suppliers (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "suppliers" VALUES(1,'Kari');
INSERT INTO "suppliers" VALUES(2,'Обувь для вас');
CREATE TABLE units (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "units" VALUES(1,'шт.');
CREATE TABLE users (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT    NOT NULL,
    login     TEXT    NOT NULL UNIQUE,
    password  TEXT    NOT NULL,
    role_id   INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON UPDATE CASCADE ON DELETE RESTRICT
);
INSERT INTO "users" VALUES(1,'Никифорова Весения Николаевна','94d5ous@gmail.com','uzWC67',4);
INSERT INTO "users" VALUES(2,'Сазонов Руслан Германович','uth4iz@mail.com','2L6KZG',4);
INSERT INTO "users" VALUES(3,'Одинцов Серафим Артёмович','yzls62@outlook.com','JlFRCZ',4);
INSERT INTO "users" VALUES(4,'Степанов Михаил Артёмович','1diph5e@tutanota.com','8ntwUp',3);
INSERT INTO "users" VALUES(5,'Ворсин Петр Евгеньевич','tjde7c@yahoo.com','YOyhfR',3);
INSERT INTO "users" VALUES(6,'Старикова Елена Павловна','wpmrc3do@tutanota.com','RSbvHv',3);
INSERT INTO "users" VALUES(7,'Михайлюк Анна Вячеславовна','5d4zbu@tutanota.com','rwVDh9',2);
INSERT INTO "users" VALUES(8,'Ситдикова Елена Анатольевна','ptec8ym@yahoo.com','LdNyos',2);
INSERT INTO "users" VALUES(9,'Ворсин Петр Евгеньевич','1qz4kw@mail.com','gynQMT',2);
INSERT INTO "users" VALUES(10,'Старикова Елена Павловна','4np6se@mail.com','AtnDjr',2);
CREATE INDEX idx_products_category     ON products(category_id);
CREATE INDEX idx_products_supplier     ON products(supplier_id);
CREATE INDEX idx_products_manufacturer ON products(manufacturer_id);
CREATE INDEX idx_order_items_order     ON order_items(order_id);
CREATE INDEX idx_order_items_product   ON order_items(product_article);
CREATE INDEX idx_users_role            ON users(role_id);
COMMIT;
