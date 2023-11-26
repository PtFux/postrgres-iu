

class MessageDomain:
    def __init__(self,
                 chat_id: str,
                 text: str,
                 reply_text: str = None,
                 username: str = None):
        self.chat_id = chat_id
        self.text = text
        self.reply_text = reply_text
        self.username = username

