

class Button:
    def __init__(self, text, reply_text):
        self.text = text
        self.reply_text = reply_text


class BaseKB:
    buttons: dict[Button] = None
    size: set = (3, 2)
