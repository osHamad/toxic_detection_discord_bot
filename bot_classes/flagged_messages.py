class Flagged:
    def __init__(self, message, number, is_toxic=None):
        self.number = number
        self.message = message
        self.message_id = message.id
        self.content = message.content
        self.sender = message.author
        self.sender_id = message.author.id
        self.is_toxic = is_toxic
