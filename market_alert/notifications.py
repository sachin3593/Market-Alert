class Notifier:
    def send(self, message: str, metadata: dict | None = None) -> None:
        raise NotImplementedError


class ConsoleNotifier(Notifier):
    def send(self, message: str, metadata: dict | None = None) -> None:
        print(message)
        if metadata:
            print(f"metadata={metadata}")
