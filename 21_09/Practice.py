from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from accessify import private


class Student(ABC):
    """Студент. Определяется ФИО."""

    def __init__(self, last_name: str, first_name: str, middle_name: str) -> None:
        if len(last_name.strip()) < 1:
            raise ValueError("фамилия не может быть пустой")
        if len(first_name.strip()) < 1:
            raise ValueError("имя не может быть пустым")
        if len(middle_name.strip()) < 1:
            raise ValueError("отчество не может быть пустым")
        self.__last_name = last_name.strip()
        self.__first_name = first_name.strip()
        self.__middle_name = middle_name.strip()

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def middle_name(self) -> str:
        return self.__middle_name

    @property
    def full_name(self) -> str:
        return f"{self.__last_name} {self.__first_name} {self.__middle_name}"

    @abstractmethod
    def __str__(self) -> str:
        return self.full_name


class ExamStudent(Student):
    """Студент, не имеющий автомата: указывается балл, полученный на экзамене (2-5)."""

    MIN_SCORE = 2
    MAX_SCORE = 5

    def __init__(self, last_name: str, first_name: str, middle_name: str,
                 exam_score: int) -> None:
        super().__init__(last_name, first_name, middle_name)
        if not ExamStudent.MIN_SCORE <= exam_score <= ExamStudent.MAX_SCORE:
            raise ValueError(
                f"балл за экзамен должен быть от {ExamStudent.MIN_SCORE} "
                f"до {ExamStudent.MAX_SCORE}"
            )
        self.__exam_score = exam_score

    @property
    def exam_score(self) -> int:
        return self.__exam_score

    def __str__(self) -> str:
        s = super().__str__()
        return f"{s}, экзамен, балл: {self.__exam_score}"


class AutomaticStudent(Student, ABC):
    """Студент, имеющий автомат: указывается основание."""

    @property
    @abstractmethod
    def basis(self) -> str:
        ...

    def __str__(self) -> str:
        s = super().__str__()
        return f"{s}, автомат, основание: {self.basis}"


class OlympiadStudent(AutomaticStudent):
    """Автомат получен за олимпиаду."""

    @property
    def basis(self) -> str:
        return "олимпиада"


class ControlWorkStudent(AutomaticStudent):
    """Автомат получен за контрольные работы: указывается средний балл за к/р."""

    MIN_SCORE = 2.0
    MAX_SCORE = 5.0

    def __init__(self, last_name: str, first_name: str, middle_name: str,
                 average_score: float) -> None:
        super().__init__(last_name, first_name, middle_name)
        if not ControlWorkStudent.MIN_SCORE <= average_score <= ControlWorkStudent.MAX_SCORE:
            raise ValueError(
                f"средний балл за к/р должен быть от {ControlWorkStudent.MIN_SCORE} "
                f"до {ControlWorkStudent.MAX_SCORE}"
            )
        self.__average_score = average_score

    @property
    def basis(self) -> str:
        return "контрольные работы"

    @property
    def average_score(self) -> float:
        return self.__average_score

    def __str__(self) -> str:
        s = super().__str__()
        return f"{s}, средний балл за к/р: {self.__average_score:.2f}"


class StudentGroup:
    """Хранилище студентов."""

    FIRST_LETTERS = "АБВГДЕЁЖЗИЙК"

    def __init__(self) -> None:
        self.__students: List[Student] = []

    def add_student(self, student: Student) -> None:
        if not isinstance(student, Student):
            raise TypeError("можно добавить только студента")
        self.__students.append(student)

    @private
    def is_last_name_in_range(self, last_name: str) -> bool:
        return last_name[0].upper() in StudentGroup.FIRST_LETTERS

    def print_students_from_a_to_k(self) -> None:
        # перебор и вывод студентов с фамилией на буквы от А до К
        is_found = False
        for student in self.__students:
            if self.is_last_name_in_range(student.last_name):
                print(student)
                is_found = True
        if not is_found:
            print("Студентов с фамилией на буквы от А до К нет")


class InputStudents:
    """Ввод студентов с клавиатуры."""

    STOP_WORD = "стоп"

    def __init__(self, group: StudentGroup) -> None:
        self.__group = group

    @private
    def input_full_name(self) -> Tuple[str, str, str]:
        last_name = input("Фамилия: ")
        first_name = input("Имя: ")
        middle_name = input("Отчество: ")
        return last_name, first_name, middle_name

    @private
    def input_exam_student(self) -> Student:
        last_name, first_name, middle_name = self.input_full_name()
        raw_score = input("Балл за экзамен (2-5): ")
        try:
            exam_score = int(raw_score)
        except ValueError:
            raise ValueError("балл за экзамен должен быть целым числом")
        return ExamStudent(last_name, first_name, middle_name, exam_score)

    @private
    def input_automatic_student(self) -> Student:
        last_name, first_name, middle_name = self.input_full_name()
        basis = input("Основание (олимпиада/контрольные): ").strip().lower()
        if basis == "олимпиада":
            return OlympiadStudent(last_name, first_name, middle_name)
        if basis == "контрольные":
            raw_score = input("Средний балл за к/р (2-5): ")
            try:
                average_score = float(raw_score.replace(",", "."))
            except ValueError:
                raise ValueError("средний балл за к/р должен быть числом")
            return ControlWorkStudent(last_name, first_name, middle_name, average_score)
        raise ValueError("неверное основание автомата")

    def input(self) -> None:
        while True:
            # ввод студентов
            kind = input(
                f'Тип студента (экзамен/автомат, "{InputStudents.STOP_WORD}" - закончить): '
            ).strip().lower()
            if kind == InputStudents.STOP_WORD:
                break
            student: Optional[Student] = None
            try:
                if kind == "экзамен":
                    student = self.input_exam_student()
                elif kind == "автомат":
                    student = self.input_automatic_student()
                else:
                    print("Неверный тип студента")
                    continue
            except ValueError as error:
                print(f"Ошибка ввода: {error}")
                continue
            self.__group.add_student(student)


class Task:
    def run(self) -> None:
        # тут все вместе делается
        group = StudentGroup()
        input_students = InputStudents(group)
        input_students.input()
        print("\nСтуденты с фамилией на буквы от А до К:")
        group.print_students_from_a_to_k()


if __name__ == "__main__":
    Task().run()
