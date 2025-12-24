BEGIN TRANSACTION;
CREATE TABLE accounts (
	id INTEGER NOT NULL, 
	account VARCHAR(100) NOT NULL, 
	bank_name VARCHAR(200) NOT NULL, 
	bank_identity_number VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO accounts VALUES(1,'1','Т-Банк','213482034924');
CREATE TABLE organizations (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	address VARCHAR(255) NOT NULL, 
	account_id INTEGER, 
	chief VARCHAR(100) NOT NULL, 
	financial_chief VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES accounts (id)
);
INSERT INTO organizations VALUES(1,'ООО "Модуль-решение"','Красная 87',1,'Иванов Иван Сергеевич','Жукова Анна Ивановна');
CREATE TABLE employees (
	id INTEGER NOT NULL, 
	last_name VARCHAR(100) NOT NULL, 
	first_name VARCHAR(100) NOT NULL, 
	middle_name VARCHAR(100), 
	post VARCHAR(200) NOT NULL, 
	passport_series VARCHAR(10) NOT NULL, 
	passport_number VARCHAR(20) NOT NULL, 
	passport_issued_by VARCHAR(255) NOT NULL, 
	passport_date_of_issue DATE NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO employees VALUES(1,'Петров ','Федор','Николаевич','Менеджер','1093','123678','РФ','2003-12-23');
CREATE TABLE units (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO units VALUES(1,'шт');
INSERT INTO units VALUES(2,'кг');
INSERT INTO units VALUES(3,'м');
CREATE TABLE products (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	price NUMERIC(10, 2) NOT NULL, 
	unit_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(unit_id) REFERENCES units (id)
);
INSERT INTO products VALUES(1,'Карандаши',120,1);
INSERT INTO products VALUES(2,'Рис',70,2);
CREATE TABLE customers (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO customers VALUES(1,'ПАО "КуБАЗА"');
INSERT INTO customers VALUES(2,'ИП "ЗДвид"');
CREATE TABLE departments (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO departments VALUES(1,'Маркетинг');
INSERT INTO departments VALUES(2,'Бухгалтерия');
INSERT INTO departments VALUES(3,'Мониторинг трафика сети');
CREATE TABLE positions (
	id INTEGER NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO positions VALUES(1,'Бухгалтер');
INSERT INTO positions VALUES(2,'Разработчик');
INSERT INTO positions VALUES(3,'Директор');
CREATE TABLE proxies (
	id INTEGER NOT NULL, 
	organization_id INTEGER NOT NULL, 
	employee_id INTEGER NOT NULL, 
	customer_id INTEGER NOT NULL, 
	date_of_issue DATE NOT NULL, 
	is_valid_until DATE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(organization_id) REFERENCES organizations (id), 
	FOREIGN KEY(employee_id) REFERENCES employees (id), 
	FOREIGN KEY(customer_id) REFERENCES customers (id)
);
INSERT INTO proxies VALUES(1,1,1,2,'2021-11-07','2025-09-11');
CREATE TABLE proxy_items (
	id INTEGER NOT NULL, 
	proxy_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	amount INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(proxy_id) REFERENCES proxies (id), 
	FOREIGN KEY(product_id) REFERENCES products (id)
);
INSERT INTO proxy_items VALUES(1,1,1,12);
INSERT INTO proxy_items VALUES(2,1,2,200);
CREATE INDEX ix_accounts_id ON accounts (id);
CREATE INDEX ix_organizations_id ON organizations (id);
CREATE INDEX ix_employees_id ON employees (id);
CREATE INDEX ix_units_id ON units (id);
CREATE INDEX ix_products_id ON products (id);
CREATE INDEX ix_customers_id ON customers (id);
CREATE INDEX ix_departments_id ON departments (id);
CREATE INDEX ix_positions_id ON positions (id);
CREATE INDEX ix_proxies_id ON proxies (id);
CREATE INDEX ix_proxy_items_id ON proxy_items (id);
COMMIT;

CREATE TABLE orders (
    id INTEGER NOT NULL, 
    organization_id INTEGER NOT NULL, 
    department_id INTEGER NOT NULL, 
    employee_id INTEGER NOT NULL, 
    order_date DATE NOT NULL, 
    order_number VARCHAR(50) NOT NULL, 
    purpose VARCHAR(500), 
    PRIMARY KEY (id), 
    FOREIGN KEY(organization_id) REFERENCES organizations (id), 
    FOREIGN KEY(department_id) REFERENCES departments (id), 
    FOREIGN KEY(employee_id) REFERENCES employees (id)
);

CREATE TABLE order_items (
    id INTEGER NOT NULL, 
    order_id INTEGER NOT NULL, 
    product_id INTEGER NOT NULL, 
    amount INTEGER NOT NULL, 
    price NUMERIC(10, 2), 
    PRIMARY KEY (id), 
    FOREIGN KEY(order_id) REFERENCES orders (id), 
    FOREIGN KEY(product_id) REFERENCES products (id)
);

CREATE INDEX ix_orders_id ON orders (id);
CREATE INDEX ix_order_items_id ON order_items (id);

CREATE TABLE material_requisitions (
	id INTEGER NOT NULL,
	organization_id INTEGER NOT NULL,
	warehouse_id VARCHAR(255) NOT NULL,
	department_id INTEGER NOT NULL,
	employee_id INTEGER NOT NULL,
	requisition_number VARCHAR(50) NOT NULL,
	requisition_date DATE NOT NULL,
	production_order_id INTEGER,
	purpose TEXT,
	status VARCHAR(50),
	issued_by_id INTEGER,
	received_by_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(organization_id) REFERENCES organizations (id),
	FOREIGN KEY(department_id) REFERENCES departments (id),
	FOREIGN KEY(employee_id) REFERENCES employees (id)
);

CREATE TABLE material_requisition_items (
	id INTEGER NOT NULL,
	requisition_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	product_name VARCHAR(500) NOT NULL,
	unit VARCHAR(50) NOT NULL,
	requested_quantity NUMERIC(10,3) NOT NULL,
	issued_quantity NUMERIC(10,3) NOT NULL,
	price NUMERIC(15,2) NOT NULL,
	amount NUMERIC(15,2) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(requisition_id) REFERENCES material_requisitions (id),
	FOREIGN KEY(product_id) REFERENCES products (id)
);

-- sample requisition to ensure print shows warehouse, product names and correct columns
INSERT INTO material_requisitions VALUES(1,1,'Краснодар',1,1,'MR-001','2025-12-17',NULL,'Для производства','утвержден',1,2);

INSERT INTO material_requisition_items VALUES(1,1,1,'Карандаши','шт',10.000,10.000,120.00,1200.00);
INSERT INTO material_requisition_items VALUES(2,1,2,'Рис','кг',5.000,5.000,70.00,350.00);

CREATE INDEX ix_material_requisitions_id ON material_requisitions (id);
CREATE INDEX ix_material_requisition_items_id ON material_requisition_items (id);