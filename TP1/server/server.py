from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

from ssl_tls.certificate import gerar_certificados

import base64
import hashlib
import json
import sqlite3
import ssl


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def gerar_token(usuario):
    return base64.urlsafe_b64encode(usuario.encode()).decode()


class Servidor(BaseHTTPRequestHandler):
    def _responder(self, status: int, dados: dict):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(dados).encode())

    def do_OPTIONS(self):
        self._responder(200, {'status':'Servidor seguro funcionando com OPTIONS'})

    def do_GET(self):
        if self.path == "/":
            self._responder(200, {'status': 'Servidor seguro funcionando com GET'})
            return

        if self.path == "/me":
            auth_header = self.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                self._responder(401, {'erro': 'Token de autenticação ausente ou inválido'})
                return

            token = auth_header.split(' ')[1]
            try:
                usuario = base64.urlsafe_b64decode(token.encode()).decode()

                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT u.nome, u.email, u.data_nasc, u.telefone, u.data_cadastro
                    FROM usuarios u
                    JOIN login l ON l.id_usuario = u.id_usuario
                    WHERE l.nome_usuario = ?
                """, (usuario,))
                resultado = cursor.fetchone()
                conn.close()

                if not resultado:
                    self._responder(404, {'erro': 'Usuário não encontrado'})
                    return

                dados_usuario = {
                    "nome": resultado[0],
                    "email": resultado[1],
                    "data_nascimento": resultado[2],
                    "telefone": resultado[3],
                    "data_cadastro": resultado[4]
                }

                self._responder(200, dados_usuario)

            except Exception as e:
                self._responder(401, {'erro': 'Token inválido', 'detalhes': str(e)})
            return

        # Qualquer outro caminho GET
        self._responder(404, {'erro': 'Endpoint não encontrado'})

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode()

        try:
            data = json.loads(post_data)
        except json.JSONDecodeError as e:
            self._responder(400, {'erro': 'JSON inválido', 'detalhes':e})
            return

        match self.path:
            case '/login':
                self.login(data)
            case '/register':
                self.register(data)
            case _:
                self._responder(404, {'erro': 'Endpoint não encontrado'})

    def do_PUT(self):
        if self.path != '/user':
            self._responder(404, {'erro': 'Endpoint não encontrado', 'detalhes':e})
            return

        auth_header = self.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            self._responder(401, {'erro': 'Token de autenticação ausente ou inválido','detalhes':e})
            return

        token = auth_header.split(' ')[1]

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode()

        try:
            data = json.loads(post_data)
            self.editar_usuario(token, data)
        except json.JSONDecodeError as e:
            self._responder(400, {'erro': 'JSON inválido', 'detalhes':e})

    def login(self, data:dict):
        usuario = data.get('usuario')
        senha = data.get('senha')
        if not usuario or not senha:
            self._responder(400, {'erro': 'Usuário e senha são obrigatórios'})
            return

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id_usuario, senha_hash FROM login WHERE nome_usuario = ?", (usuario,))
        resultado = cursor.fetchone()

        if resultado and resultado[1] == hash_password(senha):
            cursor.execute("UPDATE login SET ultimo_login = CURRENT_TIMESTAMP WHERE nome_usuario = ?", (usuario,))
            conn.commit()
            self._responder(200, {'token': gerar_token(usuario)})
        else:
            self._responder(401, {'erro': 'Usuário ou senha inválidos'})

        conn.close()

    def register(self, data: dict):
        try:
            # Corrige a desserialização do JSON
            if isinstance(data, str):
                data = json.loads(data)

            nome = data.get('nome')
            email = data.get('email')
            data_nasc = data.get('data_nascimento')
            telefone = data.get('telefone')
            nome_usuario = data.get('usuario')
            senha = data.get('senha')

            if not all([nome, email, nome_usuario, senha]):
                self._responder(400, {'erro': 'Campos obrigatórios faltando'})
                return

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            try:
                # Verifica primeiro se o usuário ou email já existem
                cursor.execute("SELECT id_usuario FROM usuarios WHERE email = ?", (email,))
                if cursor.fetchone():
                    self._responder(409, {'erro': 'Email já registrado'})
                    return

                cursor.execute("SELECT id_login FROM login WHERE nome_usuario = ?", (nome_usuario,))
                if cursor.fetchone():
                    self._responder(409, {'erro': 'Nome de usuário já existe'})
                    return

                # Se não existir, insere
                cursor.execute("INSERT INTO usuarios (nome,email,data_nasc,telefone) VALUES (?,?,?,?)",
                               (nome, email, data_nasc, telefone))

                id_usuario = cursor.lastrowid
                cursor.execute("INSERT INTO login (id_usuario, nome_usuario, senha_hash) VALUES (?, ?, ?)",
                               (id_usuario, nome_usuario, hash_password(senha)))

                conn.commit()
                self._responder(201, {'status': 'Usuário registrado com sucesso'})

            except sqlite3.Error as e:
                conn.rollback()
                self._responder(500, {'erro': 'Erro no servidor', 'detalhes': str(e)})
            finally:
                conn.close()
        except Exception as e:
            self._responder(400, {'erro': 'Dados inválidos', 'detalhes': str(e)})

    def editar_usuario(self, token: str, data: dict):
        try:
            usuario = base64.urlsafe_b64decode(token.encode()).decode()

            senha_atual = data.get('senha_atual')  # Corrigido para senha_atual
            if not senha_atual:
                self._responder(400, {'erro': 'Senha atual é obrigatória'})
                return

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            try:
                # Verifica credenciais
                cursor.execute("""
                    SELECT l.id_usuario, l.senha_hash 
                    FROM login l 
                    WHERE l.nome_usuario = ?
                """, (usuario,))
                resultado = cursor.fetchone()

                if not resultado or resultado[1] != hash_password(senha_atual):
                    self._responder(401, {'erro': 'Senha atual incorreta'})
                    return

                id_usuario = resultado[0]
                updates = []
                params = []

                # Atualizações dos campos
                if 'nome' in data and data['nome']:
                    updates.append("nome = ?")
                    params.append(data['nome'])

                if 'email' in data and data['email']:
                    # Verifica se o novo email já existe para outro usuário
                    cursor.execute("SELECT id_usuario FROM usuarios WHERE email = ? AND id_usuario != ?",
                                   (data['email'], id_usuario))
                    if cursor.fetchone():
                        self._responder(409, {'erro': 'Email já está em uso por outro usuário'})
                        return
                    updates.append("email = ?")
                    params.append(data['email'])

                if 'data_nascimento' in data and data['data_nascimento']:
                    updates.append("data_nasc = ?")
                    params.append(data['data_nascimento'])

                if 'telefone' in data and data['telefone']:
                    updates.append("telefone = ?")
                    params.append(data['telefone'])

                if updates:
                    query = "UPDATE usuarios SET " + ", ".join(updates) + " WHERE id_usuario = ?"
                    params.append(id_usuario)
                    cursor.execute(query, params)

                # Atualização de senha
                if 'nova_senha' in data and data['nova_senha']:
                    cursor.execute("""
                        UPDATE login 
                        SET senha_hash = ? 
                        WHERE id_usuario = ?
                    """, (hash_password(data['nova_senha']), id_usuario))

                conn.commit()
                self._responder(200, {'status': 'Dados atualizados com sucesso'})

            except sqlite3.Error as e:
                conn.rollback()
                self._responder(500, {'erro': 'Erro ao atualizar dados', 'detalhes': str(e)})
            finally:
                conn.close()
        except Exception as e:
            self._responder(401, {'erro': 'Token inválido', 'detalhes': str(e)})


def iniciar_servidor():
    cert_path, key_path = gerar_certificados(cert_dir='../cert')

    session = requests.Session()
    session.verify = cert_path
    # Configuração SSL moderna
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)


    # Configurações recomendadas para segurança
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.set_ciphers('ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384')
    context.options |= (
            ssl.OP_NO_COMPRESSION |
            ssl.OP_SINGLE_DH_USE |
            ssl.OP_SINGLE_ECDH_USE
    )

    httpd = HTTPServer(('localhost', 4443), Servidor)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    print("Servidor HTTPS rodando em https://localhost:4443")
    httpd.serve_forever()


if __name__ == '__main__':
    iniciar_servidor()
