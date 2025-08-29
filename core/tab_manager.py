from playwright.sync_api import BrowserContext, Page

class TabManager:
    def __init__(self):
        self.ctx: BrowserContext | None = None

    def attach(self, ctx: BrowserContext):
        """Conecta o TabManager a um contexto já inicializado."""
        self.ctx = ctx

    def open_page(self) -> Page:
        if self.ctx is None:
            raise RuntimeError("TabManager não está ligado a um BrowserContext. Chame orchestrator.start() antes.")
        page = self.ctx.new_page()
        page.set_default_timeout(60_000)
        return page

    def close_page(self, page: Page):
        try:
            page.close()
        except Exception:
            pass
