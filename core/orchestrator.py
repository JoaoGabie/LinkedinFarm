from threading import Lock
from core.session_manager import SessionManager
from core.tab_manager import TabManager

class BrowserOrchestrator:
    _instance = None
    _lock = Lock()

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.session_manager = SessionManager()
        self.tabs = TabManager()
        self._started = False
        self._initialized = True

    @classmethod
    def instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def start(self):
        """Inicializa o contexto e liga o TabManager (idempotente)."""
        if self._started:
            return
        ctx = self.session_manager.start()
        self.tabs.attach(ctx)      # <<< liga o ctx no TabManager
        self._started = True

    def open_page(self):
        """Retorna uma nova aba (Page)."""
        if not self._started:
            self.start()
        return self.tabs.open_page()

    def close_page(self, page):
        self.tabs.close_page(page)

    def stop(self):
        if self._started:
            try:
                self.session_manager.stop()
            finally:
                self._started = False
        # opcional: resetar singleton
        with self._lock:
            type(self)._instance = None
