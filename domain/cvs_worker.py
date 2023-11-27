import csv
from pathlib import Path

from common.contribution_status import ContributionStatus
from common.format_contribution_file import FormatContributionFile
from domain.domain_model.contribution import Contribution


class CSVWorker:
    def get_contributions_and_students_from_file(self, path: Path) -> tuple[list, list]:
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            contributions = []
            students = []
            for row in reader:
                row: dict
                amount: str = row.get(FormatContributionFile.amount)
                amount, status = self._get_amount_and_status(amount)

                contribution = Contribution(
                        amount=amount,
                        student_id_number=row.get(FormatContributionFile.student_id),
                        status=status
                    )
                contribution.update_season()
                contribution.update_year()
                contributions.append(
                    contribution
                )

                surname, name, *_ = row.get(FormatContributionFile.fio).split()
                students.append(
                    {
                        "name": name,
                        "surname": surname,
                        "student_id_number": row.get(FormatContributionFile.student_id)
                    }
                )
            return contributions, students

    @staticmethod
    def _get_amount_and_status(amount: str) -> tuple[int, ContributionStatus]:
        if amount.isdigit():
            amount: int = int(amount)
            status = ContributionStatus.PASSED
        else:
            match amount:
                case FormatContributionFile.amount_NOT_KNOWN:
                    amount = FormatContributionFile.amount_DEFAULT
                    status = ContributionStatus.NOT_KNOWN
                case FormatContributionFile.amount_REFUSUAL:
                    amount = FormatContributionFile.amount_DEFAULT
                    status = ContributionStatus.REFUSAL
                case FormatContributionFile.amount_STUDENTSHIP:
                    amount = FormatContributionFile.amount_DEFAULT
                    status = ContributionStatus.STUDENTSHIP
                case _:
                    raise Exception("NOT KNOWN AMOUNT")
        return amount, status


if __name__ == "__main__":
    wr = CSVWorker()
    ar1, ar2 = wr.get_contributions_and_students_from_file(FormatContributionFile.path)
    print(*ar1, sep="\n")
    print()
    print(*ar2, sep="\n")
