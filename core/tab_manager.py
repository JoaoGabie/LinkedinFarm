from playwright.sync_api import Page
from core.session_manager import SessionManager  # Adicionada para tipagem, se necessário

class TabManager:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager

    def open_page(self) -> Page:
        """Fornece uma nova aba se a sessão estiver ativa."""
        if not self.session_manager.logged_in:
            raise Exception("Not logged in")
        return self.session_manager.context.new_page()

    def close_page(self, page: Page):
        """Fecha uma aba específica."""
        if page:
            page.close()