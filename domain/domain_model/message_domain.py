from pathlib import Path

from bot.content_type import ContentType


class MessageDomain:
    def __init__(self,
                 chat_id: str,
                 text: str,
                 reply_text: str = None,
                 username: str = None,
                 content_type: ContentType = None,
                 file_path: str | Path = None):
        self.chat_id = chat_id
        self.text = text
        self.reply_text = reply_text
        self.username = username
        self.content_type = content_type
        self.file_path = file_path

    def __repr__(self):
        return f"<MessageDomain object chat_id={self.chat_id} text={self.text} by user={self.username}"
