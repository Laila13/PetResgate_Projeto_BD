-- ============================================================
-- PetResgate - Sistema para ONG de Resgate e Adoção de Animais
-- Etapa 4 - Script de criação (DDL)
-- SGBD alvo: SQLite 3
-- ============================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS ADOCAO;
DROP TABLE IF EXISTS VISITA;
DROP TABLE IF EXISTS ABRIGAMENTO;
DROP TABLE IF EXISTS PRONTUARIO_MEDICO;
DROP TABLE IF EXISTS LAR_TEMPORARIO;
DROP TABLE IF EXISTS ADOTANTE;
DROP TABLE IF EXISTS VETERINARIO;
DROP TABLE IF EXISTS ANIMAL;

CREATE TABLE VETERINARIO (
    id_veterinario  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT    NOT NULL,
    crmv            TEXT    NOT NULL UNIQUE,
    telefone        TEXT
);

CREATE TABLE ANIMAL (
    id_animal       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT    NOT NULL,
    especie         TEXT    NOT NULL,
    raca            TEXT,
    porte           TEXT    NOT NULL CHECK (porte IN ('pequeno','medio','grande')),
    sexo            TEXT    NOT NULL CHECK (sexo IN ('M','F')),
    data_resgate    DATE    NOT NULL,
    local_resgate   TEXT    NOT NULL,
    status          TEXT    NOT NULL CHECK (status IN
                        ('resgatado','em_tratamento','disponivel','em_lar_temporario','adotado'))
                        DEFAULT 'resgatado',
    obs_saude       TEXT
);

CREATE TABLE PRONTUARIO_MEDICO (
    id_prontuario     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal         INTEGER NOT NULL,
    id_veterinario    INTEGER NOT NULL,
    data_atendimento  DATE    NOT NULL,
    tipo              TEXT    NOT NULL CHECK (tipo IN ('vacina','cirurgia','consulta','exame')),
    descricao         TEXT    NOT NULL,
    proxima_dose      DATE,
    FOREIGN KEY (id_animal) REFERENCES ANIMAL(id_animal) ON DELETE RESTRICT,
    FOREIGN KEY (id_veterinario) REFERENCES VETERINARIO(id_veterinario) ON DELETE RESTRICT
);

CREATE TABLE LAR_TEMPORARIO (
    id_lar           INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_voluntario  TEXT    NOT NULL,
    endereco         TEXT    NOT NULL,
    telefone         TEXT    NOT NULL,
    capacidade       INTEGER NOT NULL CHECK (capacidade > 0),
    ativo            INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1))
);

CREATE TABLE ABRIGAMENTO (
    id_abrigamento   INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal        INTEGER NOT NULL,
    id_lar           INTEGER NOT NULL,
    data_entrada     DATE    NOT NULL,
    data_saida       DATE,
    FOREIGN KEY (id_animal) REFERENCES ANIMAL(id_animal) ON DELETE RESTRICT,
    FOREIGN KEY (id_lar) REFERENCES LAR_TEMPORARIO(id_lar) ON DELETE RESTRICT,
    CHECK (data_saida IS NULL OR data_saida >= data_entrada)
);

CREATE TABLE ADOTANTE (
    id_adotante   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT    NOT NULL,
    cpf           TEXT    NOT NULL UNIQUE,
    endereco      TEXT    NOT NULL,
    telefone      TEXT    NOT NULL,
    email         TEXT
);

CREATE TABLE VISITA (
    id_visita      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_adotante    INTEGER NOT NULL,
    id_animal      INTEGER NOT NULL,
    data_visita    DATE    NOT NULL,
    observacoes    TEXT,
    resultado      TEXT    NOT NULL CHECK (resultado IN ('interessado','nao_interessado','pendente'))
                        DEFAULT 'pendente',
    FOREIGN KEY (id_adotante) REFERENCES ADOTANTE(id_adotante) ON DELETE RESTRICT,
    FOREIGN KEY (id_animal) REFERENCES ANIMAL(id_animal) ON DELETE RESTRICT
);

CREATE TABLE ADOCAO (
    id_adocao        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal        INTEGER NOT NULL,
    id_adotante      INTEGER NOT NULL,
    data_adocao      DATE    NOT NULL,
    termo_assinado   INTEGER NOT NULL DEFAULT 0 CHECK (termo_assinado IN (0,1)),
    status           TEXT    NOT NULL CHECK (status IN ('ativa','devolvida')) DEFAULT 'ativa',
    FOREIGN KEY (id_animal) REFERENCES ANIMAL(id_animal) ON DELETE RESTRICT,
    FOREIGN KEY (id_adotante) REFERENCES ADOTANTE(id_adotante) ON DELETE RESTRICT
);

-- Garante no máximo uma adoção ATIVA por animal (RN05)
CREATE UNIQUE INDEX idx_adocao_ativa_unica
    ON ADOCAO (id_animal)
    WHERE status = 'ativa';

-- Índices auxiliares para consultas frequentes
CREATE INDEX idx_animal_status ON ANIMAL(status);
CREATE INDEX idx_prontuario_animal ON PRONTUARIO_MEDICO(id_animal);
CREATE INDEX idx_abrigamento_animal ON ABRIGAMENTO(id_animal);
CREATE INDEX idx_visita_animal ON VISITA(id_animal);
