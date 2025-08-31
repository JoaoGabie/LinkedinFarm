from playwright.sync_api import sync_playwright
from core.handle.try_login import try_login
import os

class SessionManager:
    def __init__(self, user_data_dir=None, headless=False):
        if user_data_dir is None:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            user_data_dir = os.path.join(BASE_DIR, "core", ".user_data")
        self.user_data_dir = user_data_dir
        self.headless = headless
        self._playwright = None
        self._ctx = None

    def start(self):
        if self._ctx:
            return self._ctx

        self._playwright = sync_playwright().start()
        self._ctx = self._playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=self.headless,
        )

        # garante login
        page = self._ctx.new_page()
        try:
            page.goto("https://www.linkedin.com/feed/", timeout=60_000)
            if "login" in page.url:
                try_login(page)   # <<< usa a Page do contexto atual
        finally:
            page.close()

        return self._ctx

    def stop(self):
        if self._ctx:
            self._ctx.close()
            self._playwright.stop()
            self._ctx = None
