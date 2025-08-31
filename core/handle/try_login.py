import json
from dotenv import load_dotenv
import os
from playwright.sync_api import Playwright

# Constantes
FEED_URL = "https://www.linkedin.com/feed/"
LOGIN_URL = "https://www.linkedin.com/login"
SESSION_KEY_SELECTOR = "input[name='session_key']"
SESSION_PASSWORD_SELECTOR = "input[name='session_password']"
SUBMIT_BUTTON_SELECTOR = "button[type='submit']"
TIMEOUT = 10000  # 10 segundos
WAIT_AFTER_GOTO = 2000  # 2 segundos
WAIT_FOR_URL_TIMEOUT = 15000  # 15 segundos
JSON_FILE = "core/utils/linkedin_credentials.json"

def load_credentials():
    """Carrega as credenciais do arquivo JSON."""
    try:
        with open(JSON_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Arquivo {JSON_FILE} não encontrado. Criando um novo arquivo com credenciais vazias.")
        login = input("Por favor, insira seu email do LinkedIn: ").strip()
        password = input("Por favor, insira sua senha do LinkedIn: ").strip()
        if not login or not password:
            raise ValueError("Email e senha não podem estar vazios.")

        new_credentials = {
            "platform": "linkedin",
            "login": login,
            "password": password,
            "auth": []
        }
        os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
        with open(JSON_FILE, "w") as f:
            json.dump(new_credentials, f, indent=2)
            print(f"Novo arquivo {JSON_FILE} criado com sucesso.")
        return new_credentials

def save_credentials(data):
    """Salva as credenciais no arquivo JSON."""
    os.makedirs(os.path.dirname(JSON_FILE), exist_ok=True)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_auth_token(credentials):
    """Obtém o token de autenticação das credenciais, se existir e for válido."""
    auth_list = credentials.get("auth", [])
    return auth_list[0] if auth_list and auth_list[0].strip() else None

def are_credentials_valid(credentials):
    """Verifica se login e senha estão presentes."""
    return bool(credentials.get("login") and credentials.get("password"))

def attempt_token_login(context, page, token):
    """Tenta fazer login com um token de autenticação."""
    try:
        context.add_cookies([{"name": "li_at", "value": token, "domain": ".linkedin.com", "path": "/"}])
        page.goto(FEED_URL, timeout=TIMEOUT)
        page.wait_for_timeout(WAIT_AFTER_GOTO)
        if FEED_URL in page.url:
            print("Login bem-sucedido com token de autenticação.")
            return True
        else:
            print("Token de autenticação inválido.")
            return False
    except Exception as e:
        print(f"Falha no token de autenticação: {e}")
        return False

def attempt_credential_login(page, credentials):
    """Tenta fazer login com usuário e senha."""
    try:
        print("Tentando login com credenciais.")
        page.goto(LOGIN_URL, timeout=TIMEOUT)
        page.wait_for_selector(SESSION_KEY_SELECTOR, timeout=TIMEOUT)
        page.fill(SESSION_KEY_SELECTOR, credentials["login"])
        page.fill(SESSION_PASSWORD_SELECTOR, credentials["password"])
        page.click(SUBMIT_BUTTON_SELECTOR)
        page.wait_for_url(FEED_URL, timeout=WAIT_FOR_URL_TIMEOUT)
        if FEED_URL in page.url:
            print("Login bem-sucedido com credenciais.")
            return True
        else:
            print("Falha no login. URL atual:", page.url)
            page.screenshot(path="login_failure.png")
            if "checkpoint" in page.url:
                print("CAPTCHA detectado. Intervenção manual necessária.")
            elif page.query_selector("text=Incorrect email or password") or page.query_selector("text=Não foi possível fazer login"):
                print("Credenciais fornecidas inválidas.")
            return False
    except Exception as em:
        print(f"Erro no login: {em}")
        page.screenshot(path="login_error.png")
        return False

def save_new_token(context, credentials):
    """Salva um novo token de autenticação após login bem-sucedido."""
    cookies = context.cookies()
    auth_token = next((cookie["value"] for cookie in cookies if cookie["name"] == "li_at"), None)
    if auth_token:
        credentials["auth"] = [auth_token]
        save_credentials(credentials)
        print("Novo token de autenticação capturado e salvo.")

def try_login(page):
    """Tenta fazer login usando a Page já aberta no contexto do Core."""
    credentials = load_credentials()
    if not are_credentials_valid(credentials):
        print("Erro: Credenciais não fornecidas no arquivo JSON.")
        return False

    token = get_auth_token(credentials)
    if token and attempt_token_login(page.context, page, token):
        return True

    # Token falhou → limpa e tenta com credenciais
    credentials["auth"] = []
    save_credentials(credentials)
    page.context.clear_cookies()

    if attempt_credential_login(page, credentials):
        save_new_token(page.context, credentials)
        return True

    print("Falha no login com credenciais.")
    return False
