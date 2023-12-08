import uuid
from datetime import datetime

from common.contribution_status import ContributionStatus
from common.season import Season


class Contribution:
    def __init__(
            self,
            amount: int,
            student_id_number: str = None,
            season: Season = None,
            year: int = None,
            status: ContributionStatus = None,
            student_id: uuid = None
    ):
        self.amount = amount
        self.student_id_number = student_id_number
        self.season = season
        self.year = year
        self.status = status
        self.student_id = student_id

    def update_season(self, season: Season = None):
        if season:
            self.season = season
        else:
            if int(datetime.now().month) >= 6:
                self.season = Season.AUTUMN
            else:
                self.season = Season.SPRING

    def update_year(self, year: int = None):
        if year:
            self.year = year
        else:
            self.year = int(datetime.now().year)

    def get(self, attr_name: str):
        att = getattr(self, attr_name)
        return getattr(att, "value", att)

    def __repr__(self):
        return (f"Contribution mount={self.amount} student_id_number={self.student_id_number} \
season={self.season} year={self.year} status={self.status} student_id = {self.student_id}")

    def __str__(self):
        return f"Профзносы в размере <b>{self.amount}</b> студента <b>{self.student_id_number}</b>"
