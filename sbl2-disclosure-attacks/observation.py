class Observation:
    def __init__(self, senders: list[int], receivers: list[int]):
        self.senders = senders
        self.receivers = receivers

    def __str__(self):
        return f"{self.senders} -> {self.receivers}"