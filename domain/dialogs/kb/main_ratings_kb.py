from domain.dialogs.kb.base_kb import Button, BaseKB


class MainRatingsKB(BaseKB):

    def __init__(self, rights: dict):
        self.buttons = {}
        for right, values in rights.items():
            self.buttons.update({
                right:
                Button(
                    values.get("name"),
                    right
                )
            })
