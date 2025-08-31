from core.orchestrator import BrowserOrchestrator
import time


def main():
    orchestrator = BrowserOrchestrator.instance()
    orchestrator.start()
    print("Browser launched and kept alive. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down...")
        orchestrator.stop()


if __name__ == "__main__":
    main()