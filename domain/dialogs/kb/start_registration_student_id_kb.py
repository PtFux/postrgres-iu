from enum import Enum

from domain.dialogs.kb.base_kb import Button, BaseKB


class StatusStudent(Enum):
    STUDENT = "wait_student_id"
    NO_STUDENT = "no_student"


class StartRegistrationStudentIdKB(BaseKB):
    buttons = {
        StatusStudent.STUDENT:
        Button("Я студент МГТУ",
               StatusStudent.STUDENT),
        StatusStudent.NO_STUDENT:
        Button("Я не студент МГТУ",
               StatusStudent.NO_STUDENT)
    }
