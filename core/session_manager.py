from playwright.sync_api import sync_playwright, BrowserContext
from core.handle.try_login import load_credentials, attempt_token_login, attempt_credential_login, save_new_token
import os

class SessionManager:
    def __init__(self):
        self.playwright = None
        self.context: BrowserContext = None
        self.logged_in = False

    def start(self):
        """Inicia o browser com sessão persistente e tenta login."""
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="persistent",
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        self.try_login()

    def try_login(self):
        """Tenta login com token ou credenciais."""
        page = self.context.new_page()
        credentials = load_credentials()
        token = credentials.get("auth", [None])[0]
        if token and attempt_token_login(self.context, page, token):
            self.logged_in = True
        else:
            if attempt_credential_login(page, credentials):
                save_new_token(self.context, credentials)
                self.logged_in = True
        page.close()

    def save_storage_state(self):
        """Salva o estado da sessão."""
        if self.context:
            self.context.storage_state(path="storage_state.json")

    def stop(self):
        """Encerra o browser e Playwright."""
        if self.context:
            self.save_storage_state()
            self.context.close()
        if self.playwright:
            self.playwright.stop()