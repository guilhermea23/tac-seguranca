import os
import requests

BASE_URL: str = "https://localhost:4443"

cert_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cert", "cert.pem"))

session = requests.Session()
session.verify = cert_path

def cadastrar() -> bool:
    print("\n\t\t\t📋 Criar novo registro:")
    nome: str = input("\tNome completo: ")
    email: str = input("\tEmail: ")
    data_nascimento: str = input("\tData de nascimento (DD/MM/YYYY): ")
    telefone: str = input("\tTelefone: ")
    print("\t---------------------------------------------------------")
    usuario: str = input("\n\tNome de usuário: ")
    senha: str = input("\tSenha: ")

    dados = {
        "nome": nome,
        "email": email,
        "data_nascimento": data_nascimento,
        "telefone": telefone,
        "usuario": usuario,
        "senha": senha
    }

    try:
        resposta = session.post(f"{BASE_URL}/register", json=dados)
        if resposta:
            print("[INFO] 🟢 Requisição retorna:\n" + str(resposta.json().get("status", resposta.json().get("erro"))))
            return True
    except Exception as e:
        print("\n[INFO][ERROR] Erro na requisição:", e)
        return False

def fazer_login() -> tuple[str | None, str | None]:
    print("\t\t\t\t🔐 Login")
    usuario = input("\tNome de usuário: ")
    senha = input("\tSenha: ")

    dados = {"usuario": usuario, "senha": senha}

    try:
        resposta = session.post(f"{BASE_URL}/login", json=dados)
        if resposta.status_code == 200:
            token = resposta.json().get("token")
            print(f"[INFO] Login bem-sucedido! Bem-vindo, {usuario}.")
            return token, usuario
        else:
            print("[INFO] Erro:", resposta.json().get("erro"))
    except Exception as e:
        print("[INFO][ERRO] Erro na conexão:", e)

    return None, None

def editar_dados(token: str, usuario_logado: str) -> tuple[str | None, str | None]:
    print("\n\t\t\t✏️ Editar dados:")
    print("\tDeixe em branco os campos que não deseja alterar")

    nome: str = input("\tNome completo: ")
    email: str = input("\tEmail: ")
    data_nascimento: str = input("\tData de nascimento (DD/MM/YYYY): ")
    telefone: str = input("\tTelefone: ")
    senha_atual: str = input("\tSenha atual (obrigatória para alterações): ")

    nova_senha: str = input("\tNova senha (deixe em branco para não alterar): ")
    confirmar_senha: str = input("\tConfirmar nova senha: ") if nova_senha else ""

    if nova_senha and nova_senha != confirmar_senha:
        print("\n[INFO] As novas senhas não coincidem.")
        return token, usuario_logado

    dados: dict = {
        "usuario": usuario_logado,
        "senha_atual": senha_atual,
        "nome": nome if nome else None,
        "email": email if email else None,
        "data_nascimento": data_nascimento if data_nascimento else None,
        "telefone": telefone if telefone else None,
        "nova_senha": nova_senha if nova_senha else None
    }

    try:
        headers = {'Authorization': f'Bearer {token}'}
        resposta = session.put(
            f"{BASE_URL}/user",
            json=dados,
            headers=headers
        )

        resposta_json = resposta.json()
        if resposta.status_code == 200:
            print("\n✅ Dados atualizados com sucesso!")
            if nova_senha:
                print("⚠️ Sua senha foi alterada. Você precisará fazer login novamente.")
                return None, None
        else:
            print(f"\n[INFO][ERRO] Erro: {resposta_json.get('erro', 'Erro desconhecido')}")

    except Exception as e:
        print("\n[INFO][ERRO] Erro na conexão:", e)

    return token, usuario_logado

def menu_nao_logado():
    while True:
        print("\n\t\t\t\t=== MENU ===")
        print("\t1. Cadastrar")
        print("\t2. Login")
        print("\t0. Encerrar conexão")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            if cadastrar():
                print("\nCadastro realizado com sucesso! Faça login para continuar.")
        elif opcao == "2":
            token, usuario = fazer_login()
            if token and usuario:
                menu_logado(token, usuario)
                return
        elif opcao == "0":
            print("👋 Conexão encerrada. Até logo!")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

def mostrar_dados_usuario(token: str):
    headers = {'Authorization': f'Bearer {token}'}
    try:
        resposta = session.get(f"{BASE_URL}/me", headers=headers)
        if resposta.status_code == 200:
            dados = resposta.json()
            print("\n📄 Seus dados cadastrados:")
            print(f"\tNome: {dados.get('nome')}")
            print(f"\tEmail: {dados.get('email')}")
            print(f"\tData de nascimento: {dados.get('data_nascimento')}")
            print(f"\tTelefone: {dados.get('telefone')}")
            print(f"\tData de cadastro: {dados.get('data_cadastro')}")
        else:
            print(f"[INFO] Erro ao obter dados: {resposta.json().get('erro')}")
    except Exception as e:
        print("[ERRO] Falha ao buscar dados do usuário:", e)

def menu_logado(token: str, usuario: str):
    while True:
        mostrar_dados_usuario(token)
        print("\n\t\t\t\t=== MENU ===")
        print("\t1. Editar dados")
        print("\t0. Logout")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            token, usuario = editar_dados(token, usuario)
            if token is None:  # Se alterou a senha
                print("\nPor favor, faça login novamente.")
                menu_nao_logado()
                return
        elif opcao == "0":
            print(f"\n🔓 Logout do usuário {usuario} realizado.")
            menu_nao_logado()  # <-- aqui está o ajuste importante
            return  # sai do menu_logado após redirecionar
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == '__main__':
    menu_nao_logado()