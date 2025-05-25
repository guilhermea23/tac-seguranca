import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Tabela de usuários
cursor.execute("""
CREATE TABLE usuarios (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    data_nasc TEXT,
    telefone TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Tabela de login
cursor.execute("""
CREATE TABLE login (
    id_login INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nome_usuario TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    ultimo_login TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
)
""")

# Tabela de formações
cursor.execute("""
CREATE TABLE formacoes (
    id_formacao INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    instituicao TEXT,
    carga_horaria INTEGER,
    data_inicio TEXT,
    data_fim TEXT,
    descricao TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

print("✅ Banco de dados SQLite criado com sucesso!")
