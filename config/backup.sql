CREATE TABLE IF NOT EXISTS t001_users(
    f001_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f001_username  TEXT NOT NULL UNIQUE,
    f001_password  TEXT NOT NULL,
    f001_active    BOOLEAN DEFAULT FALSE,
    f001_delete    BOOLEAN DEFAULT FALSE,
    f001_create_at DATETIME default (datetime('now', 'localtime'))
);

INSERT INTO t001_users (f001_username, f001_password, f001_active)
VALUES ('admin', 'admin', true);

CREATE TABLE t002_types_documents(
    f002_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f002_code      VARCHAR(10 ) NOT NULL UNIQUE,
    f002_name      VARCHAR(250) NOT NULL,
    f002_active    BOOLEAN  DEFAULT FALSE,
    f002_delete    BOOLEAN  DEFAULT FALSE,
    f002_create_at DATETIME DEFAULT (datetime('now', 'localtime')),
    f002_f001_id   INTEGER  DEFAULT 1,
    FOREIGN KEY (f002_f001_id)
        REFERENCES t001_users (f001_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

INSERT INTO t002_types_documents (f002_code, f002_name, f002_active)
VALUES ('NA', 'NO APLICA', TRUE);

CREATE TABLE IF NOT EXISTS t003_patients (
    f003_id              INTEGER PRIMARY KEY AUTOINCREMENT,
    f003_f002_id         INTEGER NOT NULL,
    f003_number          VARCHAR(25 ) NOT NULL,
    f003_first_name      VARCHAR(50 ) NOT NULL,
    f003_second_name     VARCHAR(50 ) DEFAULT NULL,
    f003_last_name       VARCHAR(50 ) NOT NULL,
    f003_middle_name     VARCHAR(50 ) DEFAULT NULL,
    f003_birth_date      DATE DEFAULT NULL,
    f003_gender          VARCHAR(1) DEFAULT NULL,
    f003_expedition_date DATE DEFAULT NULL,
    f003_blood_type      VARCHAR(10 ) DEFAULT NULL,
    f003_address         VARCHAR(250) DEFAULT NULL,
    f003_phone           VARCHAR(50 ) DEFAULT NULL,
    f003_cell_phone      VARCHAR(50 ) DEFAULT NULL,
    f003_email           VARCHAR(250) DEFAULT NULL,
    f003_create_at       DATETIME DEFAULT (datetime('now', 'localtime')),
    f003_update_at       DATETIME DEFAULT (datetime('now', 'localtime')),
    f003_active          BOOLEAN DEFAULT FALSE,
    f003_delete          BOOLEAN DEFAULT FALSE,
    f003_f001_id         INTEGER NOT NULL,
    FOREIGN KEY (f003_f002_id)
        REFERENCES t002_types_documents (f002_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    FOREIGN KEY (f003_f001_id)
        REFERENCES t001_users (f001_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS t004_locations(
    f004_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f004_create_at DATETIME DEFAULT (datetime('now', 'localtime')),
    f004_code      VARCHAR(50 ) NOT NULL UNIQUE,
    f004_name      VARCHAR(250) NOT NULL,
    f004_active    BOOLEAN DEFAULT FALSE,
    f004_delete    BOOLEAN DEFAULT FALSE,
    f004_f001_id   INTEGER DEFAULT 1,
    FOREIGN KEY (f004_f001_id)
        REFERENCES t001_users (f001_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

INSERT INTO t004_locations (f004_code, f004_name, f004_active)
VALUES
('CEXT', 'CONSULTA EXTERNA', TRUE),
('CIRA', 'CIRUGIA AMBULATORIA', TRUE),
('DT05', 'LABORATORIO CLINICO', TRUE),
('DT11', 'SALA DE TRABAJO DE PARTO', TRUE),
('FEXT', 'FIBROSIS CONSULTA EXTERNA', TRUE),
('GO01', 'RECUPERACION OBSTETRICIA', TRUE),
('HOS2', 'HOSPITALIZACION PISO 2', TRUE),
('HOS3', 'HOSPITALIZACION PISO 3', TRUE),
('HOS4', 'HOSPITALIZACION PISO 4', TRUE),
('HOS5', 'HOSPITALIZACION PISO 5', TRUE),
('ONCO', 'ONCOLOGIA', TRUE),
('OU'  , 'URGENCIAS OBSTETRICIA', TRUE),
('PD01', 'CONSULTORIO PEDIATRICA', TRUE),
('PD14', 'PEDIATRIA', TRUE),
('RADI', 'RADIOLOGIA', TRUE),
('RQX2', 'RECUPERACION CIRUGIA 2 PISO', TRUE),
('RQX4', 'RECUPERACION CIRUGIA 4 PISO', TRUE),
('SA05', 'HEMODINAMIA', TRUE),
('UADG', 'U DE ALTA DEPENDENCIA GINECO', TRUE),
('UC01', 'UNIDAD CUIDADO BASICO NEONATAL', TRUE),
('UC02', 'UCI ADULTOS', TRUE),
('UC03', 'UCI NEONATOS', TRUE),
('UC04', 'UCI PEDIATRICA', TRUE),
('UC06', 'UNIDAD CUIDADO INTERM. NEONATO', TRUE),
('UQX2', 'UNIDAD QUIRURGICA 2 PISO', TRUE),
('UQX4', 'UNIDAD QUIRURGICA 4 PISO', TRUE),
('UR03', 'SALA DE REANIMACION PEDIATRICA', TRUE),
('UR06', 'CONSULTORIO ADULTOS', TRUE),
('UR07', 'SALA DE REANIMACION ADULTOS', TRUE),
('UR09', 'OBSERVACION PEDIATRIA', TRUE),
('UR10', 'OBSERVACION ADULTOS', TRUE),
('UR12', 'SALA DE TRAUMA', TRUE);

CREATE TABLE IF NOT EXISTS t005_services(
    f005_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f005_create_at DATETIME DEFAULT (datetime('now', 'localtime')),
    f005_code      VARCHAR(50 ) NOT NULL UNIQUE,
    f005_name      VARCHAR(250) NOT NULL,
    f005_active    BOOLEAN DEFAULT FALSE,
    f005_delete    BOOLEAN DEFAULT FALSE,
    f005_f001_id   INTEGER DEFAULT 1,
    FOREIGN KEY (f005_f001_id)
        REFERENCES t001_users (f001_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

INSERT INTO t005_services (f005_code, f005_name, f005_active)
VALUES
('NA', 'NO APLICA', TRUE),
('23', 'HEMODINAMIA', TRUE),
('24', 'RADIOLOGIA', TRUE),
('27', 'LABORATORIO CLINICO ESPECIALIZ', TRUE),
('40', 'OBSTETRICIA', TRUE),
('44', 'PEDIATRIA', TRUE),
('57', 'UCI NEONATAL', TRUE),
('58', 'UCI PEDIATRICA', TRUE),
('60', 'UNIDAD CUIDADO INTERMEDIO NEON', TRUE),
('61', 'URGENCIAS', TRUE),
('68', 'CONSULTA EXTERNA', TRUE),
('69', 'HOSPITALIZACION PISO 4', TRUE),
('71', 'HOSPITALIZACION PISO 3', TRUE),
('72', 'UNIDAD DE CUIDADO CRITICO', TRUE),
('77', 'ONCOLOGIA', TRUE),
('81', 'HOSPITALIZACION PISO 2', TRUE),
('83', 'CIRUGIA AMBULATORIA', TRUE),
('85', 'HOSPITALIZACION PISO 5', TRUE),
('87', 'UN. ALTA DEPENDENCIA GINECO', TRUE),
('91', 'FIBROSIS CONSULTA EXTERNA', TRUE);

CREATE TABLE IF NOT EXISTS t006_companies (
    f006_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f006_create_at DATETIME DEFAULT (datetime('now', 'localtime')),
    f006_code      VARCHAR(50 ) NOT NULL UNIQUE,
    f006_name      VARCHAR(50 ) NOT NULL,
    f006_active    BOOLEAN DEFAULT FALSE,
    f006_delete    BOOLEAN DEFAULT FALSE,
    f006_f001_id   INTEGER DEFAULT 1,
    FOREIGN KEY (f006_f001_id)
        REFERENCES t001_users (f001_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS t007_messages (
    f007_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    f007_create_at          DATETIME     DEFAULT (datetime('now', 'localtime')),
    f007_create_by          VARCHAR(50 ) DEFAULT '__system__',
    f007_sender             VARCHAR(50 ) DEFAULT NULL,
    f007_sender_facility    VARCHAR(50 ) DEFAULT NULL,
    f007_reception          VARCHAR(50 ) DEFAULT NULL,
    f007_reception_facility VARCHAR(50 ) DEFAULT NULL,
    f007_control_id         VARCHAR(250) NOT NULL,
    f007_content           TEXT        DEFAULT NULL,
    f007_response          TEXT        DEFAULT NULL,
    f007_type_message      VARCHAR(50) DEFAULT NULL, -- ORM^O01 | ORU^O01
    f007_delete            BOOLEAN  DEFAULT FALSE,
    f007_process_at        DATETIME DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS t008_orders (
    f008_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    f008_number       VARCHAR(50) NOT NULL,
    f008_date         DATE NOT NULL,
    f008_time         TIME NOT NULL,
    f008_f007_id      INTEGER NOT NULL,         -- id del mensaje
    f008_f003_id      INTEGER NOT NULL,         -- id del paciente
    f008_f004_id      INTEGER NOT NULL,         -- id de la ubicación
    f008_f005_id      INTEGER NOT NULL,         -- id del servicio
    f008_f006_id      INTEGER NOT NULL,         -- id de la empresa
    f008_priority     INTEGER DEFAULT 0,        -- prioridad de la orden segun el primer examen
    f008_bed          VARCHAR(50) DEFAULT NULL, -- codigo de cama
    f008_type_service VARCHAR(1),               -- E: empresa | P: Particular
    f008_entity       VARCHAR(500),             -- tipo de entidad
    f008_create_at    DATETIME DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (f008_f007_id)
        REFERENCES t007_messages (f007_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    FOREIGN KEY (f008_f003_id)
        REFERENCES t003_patients
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    FOREIGN KEY (f008_f004_id)
        REFERENCES t004_locations(f004_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    FOREIGN KEY (f008_f005_id)
        REFERENCES t005_services (f005_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    FOREIGN KEY (f008_f006_id)
        REFERENCES t006_companies (f006_id)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS t009_details (
    f009_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    f009_create_at DATETIME DEFAULT (datetime('now', 'localtime')),
    f009_f008_id   INTEGER NOT NULL,
    f009_barcode   VARCHAR(50 ) NOT NULL,
    f009_sequence  INTEGER NOT NULL,
    f009_test      VARCHAR(20 ) NOT NULL,
    f009_name      VARCHAR(250) NOT NULL,
    f009_date_test DATETIME DEFAULT NULL,
    f009_process   BOOLEAN DEFAULT FALSE,
    f009_date_process DATETIME DEFAULT NULL,
    FOREIGN KEY (f009_f008_id)
        REFERENCES t008_orders (t008_orders)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT
);
