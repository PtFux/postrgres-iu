

class StudentDomain:
    def __init__(self, name: str, surname: str, student_id_number: str, student_id: int = None, amount: int = 0):
        self.name = name
        self.surname = surname
        self.student_id_number = student_id_number

        self.student_id = student_id

    def get(self, name: str):
        return getattr(self, name)

    def __str__(self):
        return f"Студент <b>{self.surname} {self.surname}</b>\t\tстуденческий <b>{self.student_id_number}</b>"
