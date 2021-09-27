class Flagged:
    def __init__(self, message_id, is_toxic):
        self.message_id = message_id
        self.content = None
        self.sender = None
        self.is_toxic = None
