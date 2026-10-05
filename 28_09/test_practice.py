"""Unit-тесты для всех классов Practice.py.

Настоящие input() и print() в тестах не используются: вместо них
подставляются mock-классы, реализующие те же интерфейсы.
"""

import unittest
from typing import List, Optional

from Practice import (
    ApplicationBuilder, AutomaticStudent, ControlWorkStudent,
    ControlWorkStudentCreator, ControlWorkStudentFormatter, ExamStudent,
    ExamStudentCreator, ExamStudentFormatter, FloatRangeValidator, FloatReader,
    FullName, FullNameFormatter, FullNameReader, IFloatReader, IFullNameReader,
    IInput, IIntReader, IOutput, IRunnable, IStudentChecker, IStudentCreator,
    IStudentFilter, IStudentFormatter, IStudentKindReader, IStudentPrinter,
    IStudentProvider, IStudentReceiver, ITextReader, IntRangeValidator,
    IntReader, LastNameFirstLetterChecker, NamePartValidator, OlympiadStudent,
    RangeValidator, RetryingReader, Validator,
    OlympiadStudentCreator, OlympiadStudentFormatter, Student, StudentFilter,
    StudentFormatterByType, StudentInputScenario, StudentKindReader,
    StudentPrinter, StudentRepository, Task, TextReader,
)


# =============================================================================
# Mock-классы
# =============================================================================

class MockInput(IInput):
    """Отдаёт заранее заданные ответы и запоминает приглашения."""

    def __init__(self, answers: List[str]) -> None:
        self.answers = list(answers)
        self.prompts: List[str] = []

    def read(self, prompt: str) -> str:
        self.prompts.append(prompt)
        if not self.answers:
            raise AssertionError("программа запросила больше ввода, чем ожидалось")
        return self.answers.pop(0)


class MockOutput(IOutput):
    """Запоминает все выведенные сообщения."""

    def __init__(self) -> None:
        self.messages: List[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)

    def text(self) -> str:
        return "\n".join(self.messages)


class StubTextReader(ITextReader):
    def __init__(self, value: str) -> None:
        self.value = value

    def read_text(self) -> str:
        return self.value


class StubIntReader(IIntReader):
    def __init__(self, value: int) -> None:
        self.value = value

    def read_int(self) -> int:
        return self.value


class StubFloatReader(IFloatReader):
    def __init__(self, value: float) -> None:
        self.value = value

    def read_float(self) -> float:
        return self.value


class StubKindReader(IStudentKindReader):
    """Отдаёт типы по очереди, затем None (стоп)."""

    def __init__(self, kinds: List[str]) -> None:
        self.kinds = list(kinds)

    def read_kind(self) -> Optional[str]:
        return self.kinds.pop(0) if self.kinds else None


class StubFullNameReader(IFullNameReader):
    def __init__(self, last_names: List[str]) -> None:
        self.last_names = list(last_names)

    def read_full_name(self) -> FullName:
        return FullName(self.last_names.pop(0), "Имя", "Отчество")


class StubCreator(IStudentCreator):
    def create(self, full_name: FullName) -> Student:
        return OlympiadStudent(full_name)


class MockReceiver(IStudentReceiver):
    def __init__(self) -> None:
        self.students: List[Student] = []

    def add(self, student: Student) -> None:
        self.students.append(student)


class StubProvider(IStudentProvider):
    def __init__(self, students: List[Student]) -> None:
        self.students = students

    def get_all(self) -> List[Student]:
        return list(self.students)


class StubChecker(IStudentChecker):
    """Пропускает студентов из заданного списка фамилий."""

    def __init__(self, allowed: List[str]) -> None:
        self.allowed = allowed

    def check(self, student: Student) -> bool:
        return student.full_name.last_name in self.allowed


class StubFilter(IStudentFilter):
    def __init__(self) -> None:
        self.received: Optional[List[Student]] = None

    def filter(self, students: List[Student]) -> List[Student]:
        self.received = students
        return students[:1]


class StubFormatter(IStudentFormatter):
    def format(self, student: Student) -> str:
        return student.full_name.last_name


class MockPrinter(IStudentPrinter):
    def __init__(self) -> None:
        self.printed: Optional[List[Student]] = None

    def print_students(self, students: List[Student]) -> None:
        self.printed = students


class MockRunnable(IRunnable):
    def __init__(self) -> None:
        self.was_run = False

    def run(self) -> None:
        self.was_run = True


def make_name(last_name: str = "Иванов") -> FullName:
    return FullName(last_name, "Иван", "Иванович")


# =============================================================================
# Сущности
# =============================================================================

class TestEntities(unittest.TestCase):

    def test_full_name(self):
        name = FullName("Иванов", "Иван", "Иванович")
        self.assertEqual(
            (name.last_name, name.first_name, name.middle_name),
            ("Иванов", "Иван", "Иванович"),
        )

    def test_exam_student(self):
        student = ExamStudent(make_name(), 4)
        self.assertEqual(student.full_name.last_name, "Иванов")
        self.assertEqual(student.exam_score, 4)
        self.assertFalse(student.has_automatic)

    def test_olympiad_student(self):
        student = OlympiadStudent(make_name())
        self.assertTrue(student.has_automatic)
        self.assertEqual(student.basis, "олимпиада")

    def test_control_work_student(self):
        student = ControlWorkStudent(make_name(), 4.5)
        self.assertTrue(student.has_automatic)
        self.assertEqual(student.basis, "контрольные работы")
        self.assertEqual(student.average_score, 4.5)

    def test_abstract_student_cannot_be_created(self):
        with self.assertRaises(TypeError):
            Student(make_name())

    def test_abstract_automatic_student_cannot_be_created(self):
        with self.assertRaises(TypeError):
            AutomaticStudent(make_name())

    def test_liskov_all_students_are_students(self):
        for student in (ExamStudent(make_name(), 3), OlympiadStudent(make_name()),
                        ControlWorkStudent(make_name(), 3.0)):
            self.assertIsInstance(student, Student)
            self.assertIsInstance(student.has_automatic, bool)


# =============================================================================
# Валидаторы
# =============================================================================

class TestNamePartValidator(unittest.TestCase):

    def setUp(self):
        self.validator = NamePartValidator("Фамилия")

    def test_correct(self):
        self.assertEqual(self.validator.validate("Иванов"), "Иванов")

    def test_strips_spaces(self):
        self.assertEqual(self.validator.validate("  Иванов  "), "Иванов")

    def test_capitalizes_first_letter(self):
        self.assertEqual(self.validator.validate("иванов"), "Иванов")

    def test_double_last_name(self):
        self.assertEqual(self.validator.validate("Римский-Корсаков"), "Римский-Корсаков")

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.validator.validate("")

    def test_only_spaces(self):
        with self.assertRaises(ValueError):
            self.validator.validate("   ")

    def test_digits(self):
        with self.assertRaises(ValueError):
            self.validator.validate("Иван0в")

    def test_starts_with_hyphen(self):
        with self.assertRaises(ValueError):
            self.validator.validate("-Иванов")


class TestValidatorHierarchy(unittest.TestCase):
    """Все валидаторы наследуют общую логику от Validator и RangeValidator."""

    def test_all_validators_share_base(self):
        for validator in (NamePartValidator("Имя"), IntRangeValidator("Балл", 2, 5),
                          FloatRangeValidator("Балл", 2, 5)):
            self.assertIsInstance(validator, Validator)

    def test_range_validators_share_range_logic(self):
        self.assertIsInstance(IntRangeValidator("Балл", 2, 5), RangeValidator)
        self.assertIsInstance(FloatRangeValidator("Балл", 2, 5), RangeValidator)

    def test_field_name_and_bounds(self):
        validator = IntRangeValidator("Балл", 2, 5)
        self.assertEqual(validator.field_name, "Балл")
        self.assertEqual((validator.minimum, validator.maximum), (2, 5))

    def test_wrong_bounds(self):
        with self.assertRaises(ValueError):
            IntRangeValidator("Балл", 5, 2)

    def test_same_message_format_everywhere(self):
        for validator, bad_value in ((NamePartValidator("Имя"), ""),
                                     (IntRangeValidator("Балл", 2, 5), 9),
                                     (FloatRangeValidator("Балл", 2, 5), 9.0)):
            with self.assertRaises(ValueError) as context:
                validator.validate(bad_value)
            self.assertTrue(str(context.exception).startswith("поле «"))

    def test_protected_method_is_hidden_from_outside(self):
        with self.assertRaises(Exception):
            IntRangeValidator("Балл", 2, 5).is_in_range(3)


class TestIntRangeValidator(unittest.TestCase):

    def setUp(self):
        self.validator = IntRangeValidator("Балл", 2, 5)

    def test_bounds_inside(self):
        for value in (2, 3, 5):
            self.assertEqual(self.validator.validate(value), value)

    def test_below(self):
        with self.assertRaises(ValueError):
            self.validator.validate(1)

    def test_above(self):
        with self.assertRaises(ValueError):
            self.validator.validate(6)


class TestFloatRangeValidator(unittest.TestCase):

    def setUp(self):
        self.validator = FloatRangeValidator("Балл", 2, 5)

    def test_bounds_inside(self):
        for value in (2.0, 4.5, 5.0):
            self.assertEqual(self.validator.validate(value), value)

    def test_just_below(self):
        with self.assertRaises(ValueError):
            self.validator.validate(1.99)

    def test_just_above(self):
        with self.assertRaises(ValueError):
            self.validator.validate(5.01)

    def test_nan(self):
        with self.assertRaises(ValueError):
            self.validator.validate(float("nan"))


# =============================================================================
# Получение значений
# =============================================================================

class TestReaderHierarchy(unittest.TestCase):
    """Все читатели получают цикл повторного ввода от RetryingReader."""

    def test_all_readers_share_base(self):
        user_input, output = MockInput([]), MockOutput()
        for reader in (TextReader(user_input, output, NamePartValidator("Имя"), ""),
                       IntReader(user_input, output, IntRangeValidator("Балл", 2, 5), ""),
                       FloatReader(user_input, output, FloatRangeValidator("Балл", 2, 5), "")):
            self.assertIsInstance(reader, RetryingReader)

    def test_retrying_reader_is_abstract(self):
        with self.assertRaises(TypeError):
            RetryingReader(MockInput([]), MockOutput(), "")

    def test_read_value_is_hidden_from_outside(self):
        reader = TextReader(MockInput(["Иванов"]), MockOutput(), NamePartValidator("Имя"), "")
        with self.assertRaises(Exception):
            reader.read_value()


class TestTextReader(unittest.TestCase):

    def test_correct_first_time(self):
        user_input, output = MockInput(["Иванов"]), MockOutput()
        reader = TextReader(user_input, output, NamePartValidator("Фамилия"), "Фамилия: ")
        self.assertEqual(reader.read_text(), "Иванов")
        self.assertEqual(output.messages, [])
        self.assertEqual(user_input.prompts, ["Фамилия: "])

    def test_asks_again_after_error(self):
        user_input, output = MockInput(["", "123", "Иванов"]), MockOutput()
        reader = TextReader(user_input, output, NamePartValidator("Фамилия"), "Фамилия: ")
        self.assertEqual(reader.read_text(), "Иванов")
        self.assertEqual(len(output.messages), 2)
        self.assertEqual(len(user_input.prompts), 3)


class TestIntReader(unittest.TestCase):

    def make_reader(self, answers: List[str]):
        user_input, output = MockInput(answers), MockOutput()
        return IntReader(user_input, output, IntRangeValidator("Балл", 2, 5), "Балл: "), output

    def test_correct(self):
        reader, _ = self.make_reader([" 4 "])
        self.assertEqual(reader.read_int(), 4)

    def test_not_a_number_then_correct(self):
        reader, output = self.make_reader(["пять", "5"])
        self.assertEqual(reader.read_int(), 5)
        self.assertIn("целое число", output.text())

    def test_fraction_is_rejected(self):
        reader, output = self.make_reader(["4.5", "4"])
        self.assertEqual(reader.read_int(), 4)
        self.assertEqual(len(output.messages), 1)

    def test_out_of_range_then_correct(self):
        reader, output = self.make_reader(["7", "1", "2"])
        self.assertEqual(reader.read_int(), 2)
        self.assertEqual(len(output.messages), 2)


class TestFloatReader(unittest.TestCase):

    def make_reader(self, answers: List[str]):
        user_input, output = MockInput(answers), MockOutput()
        return FloatReader(user_input, output, FloatRangeValidator("Балл", 2, 5), "Балл: "), output

    def test_dot(self):
        reader, _ = self.make_reader(["4.5"])
        self.assertEqual(reader.read_float(), 4.5)

    def test_comma(self):
        reader, _ = self.make_reader(["4,5"])
        self.assertEqual(reader.read_float(), 4.5)

    def test_integer_is_accepted(self):
        reader, _ = self.make_reader(["3"])
        self.assertEqual(reader.read_float(), 3.0)

    def test_errors_then_correct(self):
        reader, output = self.make_reader(["абв", "5,5", "", "2"])
        self.assertEqual(reader.read_float(), 2.0)
        self.assertEqual(len(output.messages), 3)


class TestFullNameReader(unittest.TestCase):

    def test_collects_three_parts(self):
        reader = FullNameReader(StubTextReader("Иванов"), StubTextReader("Иван"),
                                StubTextReader("Иванович"))
        name = reader.read_full_name()
        self.assertEqual(
            (name.last_name, name.first_name, name.middle_name),
            ("Иванов", "Иван", "Иванович"),
        )


class TestStudentKindReader(unittest.TestCase):

    KINDS = {"экзамен": "без автомата", "олимпиада": "автомат"}

    def make_reader(self, answers: List[str]):
        user_input, output = MockInput(answers), MockOutput()
        return StudentKindReader(user_input, output, self.KINDS, "стоп"), output

    def test_correct_kind(self):
        reader, output = self.make_reader(["экзамен"])
        self.assertEqual(reader.read_kind(), "экзамен")
        self.assertIn("олимпиада", output.text())

    def test_case_and_spaces_ignored(self):
        reader, _ = self.make_reader(["  ОЛИМПИАДА "])
        self.assertEqual(reader.read_kind(), "олимпиада")

    def test_stop(self):
        reader, _ = self.make_reader(["Стоп"])
        self.assertIsNone(reader.read_kind())

    def test_wrong_kind_then_correct(self):
        reader, output = self.make_reader(["автомат", "экзамен"])
        self.assertEqual(reader.read_kind(), "экзамен")
        self.assertIn("неизвестный тип", output.text())


# =============================================================================
# Создание студентов
# =============================================================================

class TestCreators(unittest.TestCase):

    def test_exam_creator(self):
        student = ExamStudentCreator(StubIntReader(5)).create(make_name())
        self.assertIsInstance(student, ExamStudent)
        self.assertEqual(student.exam_score, 5)

    def test_olympiad_creator(self):
        student = OlympiadStudentCreator().create(make_name())
        self.assertIsInstance(student, OlympiadStudent)

    def test_control_work_creator(self):
        student = ControlWorkStudentCreator(StubFloatReader(3.5)).create(make_name())
        self.assertIsInstance(student, ControlWorkStudent)
        self.assertEqual(student.average_score, 3.5)


# =============================================================================
# Хранение и отбор
# =============================================================================

class TestStudentRepository(unittest.TestCase):

    def test_add_and_get(self):
        repository = StudentRepository()
        student = OlympiadStudent(make_name())
        repository.add(student)
        self.assertEqual(repository.get_all(), [student])

    def test_empty(self):
        self.assertEqual(StudentRepository().get_all(), [])

    def test_get_all_returns_copy(self):
        repository = StudentRepository()
        repository.add(OlympiadStudent(make_name()))
        repository.get_all().clear()
        self.assertEqual(len(repository.get_all()), 1)

    def test_add_wrong_object(self):
        with self.assertRaises(TypeError):
            StudentRepository().add("Иванов")


class TestLastNameFirstLetterChecker(unittest.TestCase):

    def setUp(self):
        self.checker = LastNameFirstLetterChecker("АБВГДЕЁЖЗИЙК")

    def check(self, last_name: str) -> bool:
        return self.checker.check(OlympiadStudent(make_name(last_name)))

    def test_bounds_inside(self):
        self.assertTrue(self.check("Андреев"))
        self.assertTrue(self.check("Ким"))
        self.assertTrue(self.check("Ёлкин"))

    def test_just_outside(self):
        self.assertFalse(self.check("Лебедев"))
        self.assertFalse(self.check("Яковлев"))

    def test_lowercase(self):
        self.assertTrue(self.check("иванов"))

    def test_latin_letter(self):
        self.assertFalse(self.check("Adams"))


class TestStudentFilter(unittest.TestCase):

    def test_keeps_only_matching(self):
        students = [OlympiadStudent(make_name(n)) for n in ("Иванов", "Петров", "Ким")]
        result = StudentFilter(StubChecker(["Иванов", "Ким"])).filter(students)
        self.assertEqual([s.full_name.last_name for s in result], ["Иванов", "Ким"])

    def test_empty_list(self):
        self.assertEqual(StudentFilter(StubChecker([])).filter([]), [])

    def test_nothing_matches(self):
        students = [OlympiadStudent(make_name("Петров"))]
        self.assertEqual(StudentFilter(StubChecker([])).filter(students), [])


# =============================================================================
# Вывод
# =============================================================================

class TestFormatters(unittest.TestCase):

    def setUp(self):
        self.name_formatter = FullNameFormatter()

    def test_full_name_formatter(self):
        self.assertEqual(self.name_formatter.format(make_name()), "Иванов Иван Иванович")

    def test_exam_formatter(self):
        text = ExamStudentFormatter(self.name_formatter).format(ExamStudent(make_name(), 4))
        self.assertEqual(text, "Иванов Иван Иванович: без автомата, балл за экзамен 4")

    def test_olympiad_formatter(self):
        text = OlympiadStudentFormatter(self.name_formatter).format(OlympiadStudent(make_name()))
        self.assertEqual(text, "Иванов Иван Иванович: автомат, основание - олимпиада")

    def test_control_work_formatter(self):
        text = ControlWorkStudentFormatter(self.name_formatter).format(
            ControlWorkStudent(make_name(), 4.5))
        self.assertEqual(
            text,
            "Иванов Иван Иванович: автомат, основание - контрольные работы, "
            "средний балл за к/р 4.50",
        )

    def test_formatter_by_type_chooses_right_one(self):
        formatter = StudentFormatterByType({
            ExamStudent: ExamStudentFormatter(self.name_formatter),
            OlympiadStudent: StubFormatter(),
        })
        self.assertIn("экзамен", formatter.format(ExamStudent(make_name(), 3)))
        self.assertEqual(formatter.format(OlympiadStudent(make_name("Ким"))), "Ким")

    def test_formatter_by_type_unknown_type(self):
        formatter = StudentFormatterByType({})
        with self.assertRaises(TypeError):
            formatter.format(OlympiadStudent(make_name()))


class TestStudentPrinter(unittest.TestCase):

    def test_prints_numbered_list(self):
        output = MockOutput()
        printer = StudentPrinter(StubFormatter(), output, "Заголовок", "Пусто")
        printer.print_students([OlympiadStudent(make_name("Иванов")),
                                OlympiadStudent(make_name("Ким"))])
        self.assertEqual(output.messages, ["", "Заголовок", "1. Иванов", "2. Ким"])

    def test_prints_empty_message(self):
        output = MockOutput()
        StudentPrinter(StubFormatter(), output, "Заголовок", "Пусто").print_students([])
        self.assertEqual(output.messages, ["", "Заголовок", "Пусто"])


# =============================================================================
# Сценарии
# =============================================================================

class TestStudentInputScenario(unittest.TestCase):

    def test_adds_students_until_stop(self):
        receiver, output = MockReceiver(), MockOutput()
        scenario = StudentInputScenario(
            StubKindReader(["олимпиада", "олимпиада"]),
            StubFullNameReader(["Иванов", "Ким"]),
            {"олимпиада": StubCreator()},
            receiver,
            output,
        )
        scenario.run()
        self.assertEqual([s.full_name.last_name for s in receiver.students], ["Иванов", "Ким"])
        self.assertIn("Добавлено студентов: 2", output.text())

    def test_stop_immediately(self):
        receiver, output = MockReceiver(), MockOutput()
        StudentInputScenario(StubKindReader([]), StubFullNameReader([]),
                             {}, receiver, output).run()
        self.assertEqual(receiver.students, [])
        self.assertIn("Добавлено студентов: 0", output.text())


class TestTask(unittest.TestCase):

    def test_runs_input_filters_and_prints(self):
        scenario, printer, student_filter = MockRunnable(), MockPrinter(), StubFilter()
        students = [OlympiadStudent(make_name("Иванов")), OlympiadStudent(make_name("Петров"))]
        Task(scenario, StubProvider(students), student_filter, printer).run()
        self.assertTrue(scenario.was_run)
        self.assertEqual(student_filter.received, students)
        self.assertEqual(printer.printed, students[:1])


class TestApplication(unittest.TestCase):
    """Проверка всего приложения целиком на mock-вводе."""

    def test_full_scenario(self):
        user_input = MockInput([
            "экзамен", "Иванов", "Иван", "Иванович", "пять", "4",
            "олимпиада", "Яковлев", "Ян", "Янович",
            "что-то", "контрольные", "андреева", "Анна", "Сергеевна", "4,5",
            "стоп",
        ])
        output = MockOutput()
        ApplicationBuilder().build(user_input, output).run()
        text = output.text()
        self.assertIn("1. Иванов Иван Иванович: без автомата, балл за экзамен 4", text)
        self.assertIn("2. Андреева Анна Сергеевна: автомат, основание - контрольные работы", text)
        self.assertNotIn("Яковлев Ян", text)
        self.assertIn("Добавлено студентов: 3", text)

    def test_nobody_matches(self):
        user_input = MockInput(["олимпиада", "Яковлев", "Ян", "Янович", "стоп"])
        output = MockOutput()
        ApplicationBuilder().build(user_input, output).run()
        self.assertIn("Таких студентов нет.", output.text())


if __name__ == "__main__":
    unittest.main()
