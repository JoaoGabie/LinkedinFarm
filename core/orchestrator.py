from core.session_manager import SessionManager
from core.tab_manager import TabManager

class BrowserOrchestrator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BrowserOrchestrator, cls).__new__(cls)
            cls._instance.session_manager = SessionManager()
            cls._instance.tabs = TabManager(cls._instance.session_manager)
        return cls._instance

    @classmethod
    def instance(cls):
        return cls()

    def start(self):
        """Inicia o browser e a sessão."""
        self.session_manager.start()

    def open_page(self):
        """Retorna uma nova aba."""
        return self.tabs.open_page()

    def close_page(self, page):
        """Fecha uma aba."""
        self.tabs.close_page(page)

    def stop(self):
        """Encerra a sessão e o browser."""
        self.session_manager.stop()