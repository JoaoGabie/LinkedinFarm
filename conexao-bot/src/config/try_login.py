import json
import os
from playwright.sync_api import Playwright

JSON_FILE = r"C:\Users\Gaming\IdeaProjects\LinkedinFarm\conexao-bot\src\utils\linkedin_credentials.json"

def load_credentials():
    """Load credentials and auth token from the JSON file."""
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
    """Save credentials and auth token to the JSON file."""
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=2)

def try_login(p: Playwright):
    """Attempt to log in to LinkedIn using the provided Playwright instance."""
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    credentials = load_credentials()
    auth_token = credentials.get("auth", [])
    login = credentials.get("login")
    password = credentials.get("password")

    # Try logging in with auth token if it exists
    if auth_token:
        context.add_cookies([{"name": "li_at", "value": auth_token[0], "domain": ".linkedin.com", "path": "/"}])
        page.goto("https://www.linkedin.com/feed/")
        if "feed" in page.url:  # Check if login succeeded
            print("Login successful with auth token.")
            return True, page, browser
        else:
            print("Auth token invalid, attempting login with credentials.")

    # Check if credentials are available
    if not login or not password:
        raise ValueError("Credentials not provided in the JSON file.")

    # Login with credentials
    page.goto("https://www.linkedin.com/login")
    page.wait_for_load_state("networkidle")
    page.fill("input[name='session_key']", login)
    page.fill("input[name='session_password']", password)
    page.click("button[type='submit']")
    page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)

    if "feed" in page.url:
        print("Login successful with credentials.")
        cookies = context.cookies()
        auth_token = next((cookie["value"] for cookie in cookies if cookie["name"] == "li_at"), None)
        if auth_token:
            credentials["auth"] = [auth_token]
            save_credentials(credentials)
            print("Auth token captured and saved.")
        return True, page, browser
    else:
        print("Login failed.")
        browser.close()
        return False, None, None