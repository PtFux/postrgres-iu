from enum import Enum


class Button:
    def __init__(self, text, reply_text):
        self.text = text
        self.reply_text = reply_text


class StatusStudent(Enum):
    STUDENT = "give_student_id"
    NO_STUDENT = "no_student"


class StartRegistrationStudentIdKB:
    buttons = {
        StatusStudent.STUDENT:
        Button("Введу студенческий",
               "wait_student_id"),
        StatusStudent.NO_STUDENT:
        Button("Я не студент МГТУ",
               "no_student")
    }
