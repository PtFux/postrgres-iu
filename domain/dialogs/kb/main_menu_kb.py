from domain.dialogs.kb.base_kb import Button, BaseKB


class MainMenuKB(BaseKB):
    size: set = (1, 2)

    def __init__(self, rights: dict):
        self.buttons = {}
        for r_filter, values in rights.items():
            self.buttons.update({
                r_filter:
                Button(
                    values.get("name"),
                    reply_text=values.get("reply_text")
                )
            })

