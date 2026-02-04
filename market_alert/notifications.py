class Notifier:
    def send(self, message: str) -> None:
        raise NotImplementedError


class ConsoleNotifier(Notifier):
    def send(self, message: str) -> None:
        print(message)
