import json
import os
from playwright.sync_api import sync_playwright

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


def try_login():
    """Attempt to log in to LinkedIn using auth token or credentials."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Load credentials from JSON
        credentials = load_credentials()
        auth_token = credentials.get("auth", [])
        login = credentials.get("login")
        password = credentials.get("password")

        # Try login with auth token if available
        if auth_token:
            context.add_cookies([{"name": "li_at", "value": auth_token[0], "domain": ".linkedin.com", "path": "/"}])
            page.goto("https://www.linkedin.com/feed/")
            if "login" not in page.url:
                print("Login successful with auth token.")
                browser.close()
                return True

        # If auth token fails or isn’t available, use credentials
        if not login or not password:
            raise ValueError("Credentials not provided in the JSON file.")

        page.goto("https://www.linkedin.com/login")
        page.wait_for_load_state("networkidle")
        page.fill("input[name='session_key']", login)
        page.fill("input[name='session_password']", password)
        page.click("button[type='submit']")
        page.wait_for_url("https://www.linkedin.com/feed/", timeout=10000)

        if "feed" in page.url:
            print("Login successful with credentials.")
            # Capture new auth token from cookies
            cookies = context.cookies()
            auth_token = next((cookie["value"] for cookie in cookies if cookie["name"] == "li_at"), None)
            if auth_token:
                credentials["auth"] = [auth_token]
                save_credentials(credentials)
                print("Auth token captured and saved.")
            else:
                print("Auth token not found in cookies.")
        else:
            print("Login failed.")

        browser.close()
        return "feed" in page.url

if __name__ == "__main__":
    success = try_login()
    print(f"Login attempt: {'Success' if success else 'Failure'}")