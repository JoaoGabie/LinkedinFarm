from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
import json
import os
from shared.linkedin.actions import load_credentials, save_credentials, get_auth_token, attempt_token_login, attempt_credential_login, save_new_token

JSON_FILE = "utils/linkedin_credentials.json"
FEED_URL = "https://www.linkedin.com/feed/"
TIMEOUT = 10000  # 10 segundos

class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.logged_in = False

    def launch_browser(self):
        self.playwright = sync_playwright().start()
        # Usa launch_persistent_context para sessão persistente
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="persistent",
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        # Tenta carregar storage state se existir
        if os.path.exists("storage_state.json"):
            self.context.add_init_script(path="storage_state.json")  # Não é direto; melhor salvar cookies via login
        self.try_login()

    def save_storage_state(self):
        self.context.storage_state(path="storage_state.json")

    def try_login(self):
        page = self.context.new_page()
        credentials = load_credentials()
        token = get_auth_token(credentials)
        if token and attempt_token_login(self.context, page, token):
            self.logged_in = True
            self.save_storage_state()
            page.close()
            return

        # Token falhou, tenta com credenciais
        if attempt_credential_login(page, credentials):
            save_new_token(self.context, credentials)
            self.logged_in = True
            self.save_storage_state()
        page.close()

    def get_new_page(self) -> Page:
        if not self.logged_in:
            raise Exception("Not logged in")
        return self.context.new_page()

    def close(self):
        if self.context:
            self.save_storage_state()
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

browser_manager = BrowserManager()