from dataclasses import dataclass
from pathlib import Path


@dataclass
class FormatContributionFile:
    exp = "csv"
    fio = "fio"
    student_id = "student_id"
    amount = "amount"
    path = Path("../files/contribution.cvs")

    amount_NOT_KNOWN = "нет"
    amount_STUDENTSHIP = "стипа"
    amount_REFUSUAL = "отказ"
    amount_DEFAULT = 195

    def get_headliner(self):
        return [
            self.fio,
            self.student_id,
            self.amount
        ]
