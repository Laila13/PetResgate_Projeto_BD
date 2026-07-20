import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "petresgate.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "01_schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "sql", "02_seed.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed: bool = False):
    """Cria o banco de dados a partir do script DDL. Se seed=True e o banco
    ainda não existir, também executa o script de povoamento inicial."""
    is_new = not os.path.exists(DB_PATH)
    conn = get_connection()
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        conn.executescript(f.read())
    if seed and is_new:
        with open(SEED_PATH, encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()


def execute(sql: str, params: tuple = ()):
    """Executa um comando de escrita (INSERT/UPDATE/DELETE) via SQL puro."""
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def query(sql: str, params: tuple = ()):
    """Executa uma consulta (SELECT) via SQL puro e retorna as linhas."""
    conn = get_connection()
    try:
        cur = conn.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


# ------------------------------------------------------------------
# Funções específicas de cada entidade (todo o SQL fica centralizado aqui)
# ------------------------------------------------------------------

# ---- ANIMAL ----
def inserir_animal(nome, especie, raca, porte, sexo, data_resgate,
                    local_resgate, status, obs_saude):
    sql = """INSERT INTO ANIMAL
             (nome, especie, raca, porte, sexo, data_resgate, local_resgate, status, obs_saude)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    return execute(sql, (nome, especie, raca, porte, sexo, data_resgate,
                          local_resgate, status, obs_saude))


def listar_animais(filtro_status=None, filtro_nome=None):
    sql = "SELECT * FROM ANIMAL WHERE 1=1"
    params = []
    if filtro_status:
        sql += " AND status = ?"
        params.append(filtro_status)
    if filtro_nome:
        sql += " AND nome LIKE ?"
        params.append(f"%{filtro_nome}%")
    sql += " ORDER BY id_animal DESC"
    return query(sql, tuple(params))


def listar_animais_simples():
    return query("SELECT id_animal, nome FROM ANIMAL ORDER BY nome")


# ---- VETERINARIO ----
def inserir_veterinario(nome, crmv, telefone):
    sql = "INSERT INTO VETERINARIO (nome, crmv, telefone) VALUES (?, ?, ?)"
    return execute(sql, (nome, crmv, telefone))


def listar_veterinarios():
    return query("SELECT * FROM VETERINARIO ORDER BY nome")


# ---- PRONTUARIO_MEDICO ----
def inserir_prontuario(id_animal, id_veterinario, data_atendimento, tipo,
                        descricao, proxima_dose):
    sql = """INSERT INTO PRONTUARIO_MEDICO
             (id_animal, id_veterinario, data_atendimento, tipo, descricao, proxima_dose)
             VALUES (?, ?, ?, ?, ?, ?)"""
    return execute(sql, (id_animal, id_veterinario, data_atendimento, tipo,
                          descricao, proxima_dose))


def listar_prontuarios(id_animal=None):
    sql = """SELECT p.id_prontuario, a.nome AS animal, v.nome AS veterinario,
                     p.data_atendimento, p.tipo, p.descricao, p.proxima_dose
              FROM PRONTUARIO_MEDICO p
              JOIN ANIMAL a ON a.id_animal = p.id_animal
              JOIN VETERINARIO v ON v.id_veterinario = p.id_veterinario"""
    params = ()
    if id_animal:
        sql += " WHERE p.id_animal = ?"
        params = (id_animal,)
    sql += " ORDER BY p.data_atendimento DESC"
    return query(sql, params)


# ---- LAR_TEMPORARIO ----
def inserir_lar(nome_voluntario, endereco, telefone, capacidade, ativo):
    sql = """INSERT INTO LAR_TEMPORARIO
             (nome_voluntario, endereco, telefone, capacidade, ativo)
             VALUES (?, ?, ?, ?, ?)"""
    return execute(sql, (nome_voluntario, endereco, telefone, capacidade, ativo))


def listar_lares():
    return query("SELECT * FROM LAR_TEMPORARIO ORDER BY nome_voluntario")


# ---- ABRIGAMENTO ----
def inserir_abrigamento(id_animal, id_lar, data_entrada, data_saida):
    sql = """INSERT INTO ABRIGAMENTO (id_animal, id_lar, data_entrada, data_saida)
             VALUES (?, ?, ?, ?)"""
    rowid = execute(sql, (id_animal, id_lar, data_entrada, data_saida or None))
    execute("UPDATE ANIMAL SET status = 'em_lar_temporario' WHERE id_animal = ?",
            (id_animal,))
    return rowid


def listar_abrigamentos(id_animal=None):
    sql = """SELECT ab.id_abrigamento, a.nome AS animal, l.nome_voluntario AS lar,
                     ab.data_entrada, ab.data_saida
              FROM ABRIGAMENTO ab
              JOIN ANIMAL a ON a.id_animal = ab.id_animal
              JOIN LAR_TEMPORARIO l ON l.id_lar = ab.id_lar"""
    params = ()
    if id_animal:
        sql += " WHERE ab.id_animal = ?"
        params = (id_animal,)
    sql += " ORDER BY ab.data_entrada DESC"
    return query(sql, params)


# ---- ADOTANTE ----
def inserir_adotante(nome, cpf, endereco, telefone, email):
    sql = """INSERT INTO ADOTANTE (nome, cpf, endereco, telefone, email)
             VALUES (?, ?, ?, ?, ?)"""
    return execute(sql, (nome, cpf, endereco, telefone, email))


def listar_adotantes():
    return query("SELECT * FROM ADOTANTE ORDER BY nome")


# ---- VISITA ----
def inserir_visita(id_adotante, id_animal, data_visita, observacoes, resultado):
    sql = """INSERT INTO VISITA (id_adotante, id_animal, data_visita, observacoes, resultado)
             VALUES (?, ?, ?, ?, ?)"""
    return execute(sql, (id_adotante, id_animal, data_visita, observacoes, resultado))


def listar_visitas(id_animal=None):
    sql = """SELECT vi.id_visita, ad.nome AS adotante, a.nome AS animal,
                     vi.data_visita, vi.observacoes, vi.resultado
              FROM VISITA vi
              JOIN ADOTANTE ad ON ad.id_adotante = vi.id_adotante
              JOIN ANIMAL a ON a.id_animal = vi.id_animal"""
    params = ()
    if id_animal:
        sql += " WHERE vi.id_animal = ?"
        params = (id_animal,)
    sql += " ORDER BY vi.data_visita DESC"
    return query(sql, params)


# ---- ADOCAO ----
def inserir_adocao(id_animal, id_adotante, data_adocao, termo_assinado):
    sql = """INSERT INTO ADOCAO (id_animal, id_adotante, data_adocao, termo_assinado, status)
             VALUES (?, ?, ?, ?, 'ativa')"""
    rowid = execute(sql, (id_animal, id_adotante, data_adocao, termo_assinado))
    execute("UPDATE ANIMAL SET status = 'adotado' WHERE id_animal = ?", (id_animal,))
    return rowid


def listar_adocoes(id_adotante=None):
    sql = """SELECT ado.id_adocao, a.nome AS animal, ad.nome AS adotante,
                     ado.data_adocao, ado.termo_assinado, ado.status
              FROM ADOCAO ado
              JOIN ANIMAL a ON a.id_animal = ado.id_animal
              JOIN ADOTANTE ad ON ad.id_adotante = ado.id_adotante"""
    params = ()
    if id_adotante:
        sql += " WHERE ado.id_adotante = ?"
        params = (id_adotante,)
    sql += " ORDER BY ado.data_adocao DESC"
    return query(sql, params)
