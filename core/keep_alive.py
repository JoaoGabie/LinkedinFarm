from core.orchestrator import BrowserOrchestrator
import time


def main():
    # Obtém a instância singleton do BrowserOrchestrator e inicia a sessão
    orchestrator = BrowserOrchestrator.instance()
    orchestrator.start()
    print("Browser launched and kept alive. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(60)  # Loop de keep-alive, mantendo o browser vivo
    except KeyboardInterrupt:
        print("Shutting down...")
        orchestrator.stop()  # Encerra a sessão e o browser


if __name__ == "__main__":
    main()