

class RatingDomain:

    def __init__(self, amount: int = 0, last_amount: int = -1, rating_id: int = None, student_id: str = None):
        self.rating_id = rating_id
        self.student_id = student_id

        self.amount = amount
        self.last_amount = last_amount

        self.add_amount: int = 0
