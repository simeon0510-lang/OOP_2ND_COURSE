"""Семинары «SOLID». Вариант 8.

Информация о студенте определяется ФИО. Для студентов, не имеющих автомата,
указывается балл, полученный на экзамене (2-5); для студентов, имеющих автомат,
указывается основание (олимпиада или контрольные работы). Если основание -
контрольные работы, дополнительно указывается средний балл за к/р.
Выводится информация о студентах с фамилией на буквы от А до К.

Код первой работы переписан по принципам SOLID:
S - каждый класс отвечает ровно за одно;
O - новый тип студента добавляется новыми классами, без правки старых;
L - наследники используются везде, где ожидается базовый тип;
I - в конструкторы передаются максимально узкие интерфейсы;
D - классы зависят от интерфейсов (ABC), а не от конкретных реализаций.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from accessify import private, protected


# =============================================================================
# Интерфейсы (абстрактные классы только с абстрактными методами)
# =============================================================================

class IInput(ABC):
    """Источник строк, введённых пользователем."""

    @abstractmethod
    def read(self, prompt: str) -> str:
        """Показывает приглашение и возвращает введённую строку."""


class IOutput(ABC):
    """Приёмник сообщений для пользователя."""

    @abstractmethod
    def write(self, message: str) -> None:
        """Выводит одно сообщение."""


class ITextValidator(ABC):
    """Проверка строкового значения."""

    @abstractmethod
    def validate(self, value: str) -> str:
        """Возвращает нормализованную строку или бросает ValueError."""


class IIntValidator(ABC):
    """Проверка целого значения."""

    @abstractmethod
    def validate(self, value: int) -> int:
        """Возвращает значение или бросает ValueError."""


class IFloatValidator(ABC):
    """Проверка дробного значения."""

    @abstractmethod
    def validate(self, value: float) -> float:
        """Возвращает значение или бросает ValueError."""


class ITextReader(ABC):
    """Получение одного корректного текстового значения."""

    @abstractmethod
    def read_text(self) -> str:
        """Возвращает корректную строку."""


class IIntReader(ABC):
    """Получение одного корректного целого числа."""

    @abstractmethod
    def read_int(self) -> int:
        """Возвращает корректное целое число."""


class IFloatReader(ABC):
    """Получение одного корректного дробного числа."""

    @abstractmethod
    def read_float(self) -> float:
        """Возвращает корректное дробное число."""


class IFullNameReader(ABC):
    """Получение ФИО."""

    @abstractmethod
    def read_full_name(self) -> "FullName":
        """Возвращает ФИО."""


class IStudentKindReader(ABC):
    """Получение типа студента, которого нужно добавить."""

    @abstractmethod
    def read_kind(self) -> Optional[str]:
        """Возвращает ключ типа студента или None, если ввод завершён."""


class IStudentCreator(ABC):
    """Создание студента одного конкретного типа."""

    @abstractmethod
    def create(self, full_name: "FullName") -> "Student":
        """Создаёт студента с данным ФИО (дополнительные данные получает сам)."""


class IStudentReceiver(ABC):
    """Хранилище, в которое можно только добавлять."""

    @abstractmethod
    def add(self, student: "Student") -> None:
        """Добавляет студента."""


class IStudentProvider(ABC):
    """Хранилище, из которого можно только читать."""

    @abstractmethod
    def get_all(self) -> List["Student"]:
        """Возвращает копию списка всех студентов."""


class IStudentChecker(ABC):
    """Условие отбора студента."""

    @abstractmethod
    def check(self, student: "Student") -> bool:
        """Возвращает True, если студент подходит под условие."""


class IStudentFilter(ABC):
    """Отбор студентов из списка."""

    @abstractmethod
    def filter(self, students: List["Student"]) -> List["Student"]:
        """Возвращает новый список подходящих студентов."""


class IFullNameFormatter(ABC):
    """Превращение ФИО в строку."""

    @abstractmethod
    def format(self, full_name: "FullName") -> str:
        """Возвращает ФИО одной строкой."""


class IStudentFormatter(ABC):
    """Превращение студента в строку для вывода."""

    @abstractmethod
    def format(self, student: "Student") -> str:
        """Возвращает описание студента."""


class IStudentPrinter(ABC):
    """Вывод списка студентов."""

    @abstractmethod
    def print_students(self, students: List["Student"]) -> None:
        """Выводит студентов."""


class IRunnable(ABC):
    """То, что можно запустить."""

    @abstractmethod
    def run(self) -> None:
        """Выполняет действие."""


class IApplicationBuilder(ABC):
    """Сборка приложения из зависимостей."""

    @abstractmethod
    def build(self, user_input: IInput, output: IOutput) -> IRunnable:
        """Возвращает готовое к запуску приложение."""


# =============================================================================
# Сущности (только данные)
# =============================================================================

class FullName:
    """ФИО студента.

    Args:
        last_name: фамилия.
        first_name: имя.
        middle_name: отчество.
    """

    def __init__(self, last_name: str, first_name: str, middle_name: str) -> None:
        self.__last_name = last_name
        self.__first_name = first_name
        self.__middle_name = middle_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def middle_name(self) -> str:
        return self.__middle_name


class Student(ABC):
    """Студент. Определяется ФИО.

    Args:
        full_name: ФИО студента.
    """

    def __init__(self, full_name: FullName) -> None:
        self.__full_name = full_name

    @property
    def full_name(self) -> FullName:
        return self.__full_name

    @property
    @abstractmethod
    def has_automatic(self) -> bool:
        """Есть ли у студента автомат."""


class ExamStudent(Student):
    """Студент без автомата: сдавал экзамен.

    Args:
        full_name: ФИО студента.
        exam_score: балл за экзамен.
    """

    def __init__(self, full_name: FullName, exam_score: int) -> None:
        super().__init__(full_name)
        self.__exam_score = exam_score

    @property
    def has_automatic(self) -> bool:
        return False

    @property
    def exam_score(self) -> int:
        return self.__exam_score


class AutomaticStudent(Student, ABC):
    """Студент с автоматом. Основание определяют наследники."""

    @property
    def has_automatic(self) -> bool:
        return True

    @property
    @abstractmethod
    def basis(self) -> str:
        """Основание автомата."""


class OlympiadStudent(AutomaticStudent):
    """Студент с автоматом за олимпиаду."""

    @property
    def basis(self) -> str:
        return "олимпиада"


class ControlWorkStudent(AutomaticStudent):
    """Студент с автоматом за контрольные работы.

    Args:
        full_name: ФИО студента.
        average_score: средний балл за контрольные работы.
    """

    def __init__(self, full_name: FullName, average_score: float) -> None:
        super().__init__(full_name)
        self.__average_score = average_score

    @property
    def basis(self) -> str:
        return "контрольные работы"

    @property
    def average_score(self) -> float:
        return self.__average_score


# =============================================================================
# Консольный ввод и вывод
# =============================================================================

class ConsoleInput(IInput):
    """Ввод с клавиатуры через input()."""

    def read(self, prompt: str) -> str:
        return input(prompt)


class ConsoleOutput(IOutput):
    """Вывод на экран через print()."""

    def write(self, message: str) -> None:
        print(message)


# =============================================================================
# Валидаторы
#
# Validator                 - общая часть: название поля и текст ошибки
# ├── NamePartValidator     - часть ФИО
# └── RangeValidator        - общая часть проверки отрезка [minimum, maximum]
#     ├── IntRangeValidator
#     └── FloatRangeValidator
#
# Методы с @protected вызываются только из методов самих наследников.
# =============================================================================

class Validator(ABC):
    """Базовый класс всех валидаторов: хранит название поля и строит ошибку.

    Args:
        field_name: название поля для сообщений об ошибке.
    """

    def __init__(self, field_name: str) -> None:
        self.__field_name = field_name

    @property
    def field_name(self) -> str:
        return self.__field_name

    @protected
    def error(self, reason: str) -> ValueError:
        """Возвращает ошибку вида «поле «X» <reason>» (бросает её наследник)."""
        return ValueError(f"поле «{self.__field_name}» {reason}")


class NamePartValidator(Validator, ITextValidator):
    """Проверяет часть ФИО: непустая, только буквы, дефис и пробел.

    Лишние пробелы убираются, первая буква делается заглавной.

    Args:
        field_name: название поля для сообщений об ошибке.
    """

    ALLOWED_SEPARATORS = "- "

    def validate(self, value: str) -> str:
        """Убирает лишние пробелы и проверяет значение.

        Raises:
            ValueError: строка пустая, начинается не с буквы
                или содержит недопустимые символы.
        """
        value = " ".join(value.split())
        if not value:
            raise self.error("не может быть пустым")
        if not value[0].isalpha():
            raise self.error("должно начинаться с буквы")
        for char in value:
            if not (char.isalpha() or char in NamePartValidator.ALLOWED_SEPARATORS):
                raise self.error("может содержать только буквы, дефис и пробел")
        return value[0].upper() + value[1:]


class RangeValidator(Validator):
    """Общая логика для проверки, что число лежит в отрезке [minimum, maximum].

    Наследники отличаются только типом числа (int или float).

    Args:
        field_name: название поля для сообщений об ошибке.
        minimum: наименьшее допустимое значение.
        maximum: наибольшее допустимое значение.
    """

    def __init__(self, field_name: str, minimum: float, maximum: float) -> None:
        super().__init__(field_name)
        if minimum > maximum:
            raise ValueError("minimum не может быть больше maximum")
        self.__minimum = minimum
        self.__maximum = maximum

    @property
    def minimum(self) -> float:
        return self.__minimum

    @property
    def maximum(self) -> float:
        return self.__maximum

    @protected
    def is_in_range(self, value: float) -> bool:
        """True, если значение в отрезке (nan и inf в отрезок не попадают)."""
        return self.__minimum <= value <= self.__maximum

    @protected
    def range_reason(self) -> str:
        """Текст причины ошибки для сообщения."""
        return f"должно быть от {self.__minimum:g} до {self.__maximum:g}"


class IntRangeValidator(RangeValidator, IIntValidator):
    """Проверяет, что целое число лежит в отрезке."""

    def validate(self, value: int) -> int:
        """Raises: ValueError, если число вне отрезка."""
        if not self.is_in_range(value):
            raise self.error(self.range_reason())
        return value


class FloatRangeValidator(RangeValidator, IFloatValidator):
    """Проверяет, что дробное число лежит в отрезке."""

    def validate(self, value: float) -> float:
        """Raises: ValueError, если число вне отрезка (в том числе nan и inf)."""
        if not self.is_in_range(value):
            raise self.error(self.range_reason())
        return value


# =============================================================================
# Получение отдельных значений (при ошибке переспрашивается только это поле)
#
# RetryingReader     - общий цикл «спросить -> преобразовать -> при ошибке повторить»
# ├── TextReader
# ├── IntReader
# └── FloatReader
# =============================================================================

class RetryingReader(ABC):
    """Базовый класс: спрашивает значение, пока оно не станет корректным.

    Наследник определяет только convert - как превратить строку в значение.

    Args:
        user_input: откуда читать.
        output: куда писать ошибки.
        prompt: приглашение к вводу.
    """

    def __init__(self, user_input: IInput, output: IOutput, prompt: str) -> None:
        self.__input = user_input
        self.__output = output
        self.__prompt = prompt

    @abstractmethod
    def convert(self, raw: str):
        """Превращает введённую строку в значение. Raises: ValueError."""

    @protected
    def read_value(self):
        """Повторяет ввод, пока convert не вернёт значение без ошибки."""
        while True:
            try:
                return self.convert(self.__input.read(self.__prompt))
            except ValueError as error:
                self.__output.write(f"Ошибка: {error}. Попробуйте ещё раз.")


class TextReader(RetryingReader, ITextReader):
    """Спрашивает строку, пока она не пройдёт проверку.

    Args:
        user_input: откуда читать.
        output: куда писать ошибки.
        validator: проверка значения.
        prompt: приглашение к вводу.
    """

    def __init__(self, user_input: IInput, output: IOutput,
                 validator: ITextValidator, prompt: str) -> None:
        super().__init__(user_input, output, prompt)
        self.__validator = validator

    def convert(self, raw: str) -> str:
        return self.__validator.validate(raw)

    def read_text(self) -> str:
        return self.read_value()


class IntReader(RetryingReader, IIntReader):
    """Спрашивает целое число, пока оно не пройдёт проверку.

    Args:
        user_input: откуда читать.
        output: куда писать ошибки.
        validator: проверка значения.
        prompt: приглашение к вводу.
    """

    def __init__(self, user_input: IInput, output: IOutput,
                 validator: IIntValidator, prompt: str) -> None:
        super().__init__(user_input, output, prompt)
        self.__validator = validator

    @private
    def parse(self, raw: str) -> int:
        """Превращает строку в целое число. Raises: ValueError."""
        try:
            return int(raw.strip())
        except ValueError:
            raise ValueError("нужно ввести целое число")

    def convert(self, raw: str) -> int:
        return self.__validator.validate(self.parse(raw))

    def read_int(self) -> int:
        return self.read_value()


class FloatReader(RetryingReader, IFloatReader):
    """Спрашивает дробное число (допускаются точка и запятая).

    Args:
        user_input: откуда читать.
        output: куда писать ошибки.
        validator: проверка значения.
        prompt: приглашение к вводу.
    """

    def __init__(self, user_input: IInput, output: IOutput,
                 validator: IFloatValidator, prompt: str) -> None:
        super().__init__(user_input, output, prompt)
        self.__validator = validator

    @private
    def parse(self, raw: str) -> float:
        """Превращает строку в число, запятая считается точкой. Raises: ValueError."""
        try:
            return float(raw.strip().replace(",", "."))
        except ValueError:
            raise ValueError("нужно ввести число, например 4.5 или 4,5")

    def convert(self, raw: str) -> float:
        return self.__validator.validate(self.parse(raw))

    def read_float(self) -> float:
        return self.read_value()


class FullNameReader(IFullNameReader):
    """Собирает ФИО из трёх отдельных полей.

    Args:
        last_name_reader: получение фамилии.
        first_name_reader: получение имени.
        middle_name_reader: получение отчества.
    """

    def __init__(self, last_name_reader: ITextReader, first_name_reader: ITextReader,
                 middle_name_reader: ITextReader) -> None:
        self.__last_name_reader = last_name_reader
        self.__first_name_reader = first_name_reader
        self.__middle_name_reader = middle_name_reader

    def read_full_name(self) -> FullName:
        return FullName(
            self.__last_name_reader.read_text(),
            self.__first_name_reader.read_text(),
            self.__middle_name_reader.read_text(),
        )


class StudentKindReader(IStudentKindReader):
    """Показывает меню типов студентов и спрашивает выбор.

    Регистр и лишние пробелы не учитываются. При неверном вводе
    меню показывается снова.

    Args:
        user_input: откуда читать.
        output: куда писать меню и ошибки.
        kinds: ключ типа -> пояснение для меню.
        stop_word: слово для завершения ввода.
    """

    def __init__(self, user_input: IInput, output: IOutput,
                 kinds: Dict[str, str], stop_word: str) -> None:
        self.__input = user_input
        self.__output = output
        self.__kinds = dict(kinds)
        self.__stop_word = stop_word

    def read_kind(self) -> Optional[str]:
        while True:
            self.__output.write("")
            for key, description in self.__kinds.items():
                self.__output.write(f'  "{key}" - {description}')
            self.__output.write(f'  "{self.__stop_word}" - закончить ввод')
            answer = self.__input.read("Тип студента: ").strip().lower()
            if answer == self.__stop_word:
                return None
            if answer in self.__kinds:
                return answer
            self.__output.write(f'Ошибка: неизвестный тип "{answer}". Выберите из списка.')


# =============================================================================
# Создание студентов (принцип O: новый тип = новый класс-создатель)
# =============================================================================

class ExamStudentCreator(IStudentCreator):
    """Создаёт студента без автомата.

    Args:
        exam_score_reader: получение балла за экзамен.
    """

    def __init__(self, exam_score_reader: IIntReader) -> None:
        self.__exam_score_reader = exam_score_reader

    def create(self, full_name: FullName) -> Student:
        return ExamStudent(full_name, self.__exam_score_reader.read_int())


class OlympiadStudentCreator(IStudentCreator):
    """Создаёт студента с автоматом за олимпиаду."""

    def create(self, full_name: FullName) -> Student:
        return OlympiadStudent(full_name)


class ControlWorkStudentCreator(IStudentCreator):
    """Создаёт студента с автоматом за контрольные работы.

    Args:
        average_score_reader: получение среднего балла за к/р.
    """

    def __init__(self, average_score_reader: IFloatReader) -> None:
        self.__average_score_reader = average_score_reader

    def create(self, full_name: FullName) -> Student:
        return ControlWorkStudent(full_name, self.__average_score_reader.read_float())


# =============================================================================
# Хранение, отбор, вывод
# =============================================================================

class StudentRepository(IStudentReceiver, IStudentProvider):
    """Хранит студентов в памяти."""

    def __init__(self) -> None:
        self.__students: List[Student] = []

    def add(self, student: Student) -> None:
        """Raises: TypeError, если передан не студент."""
        if not isinstance(student, Student):
            raise TypeError("можно добавить только студента")
        self.__students.append(student)

    def get_all(self) -> List[Student]:
        return list(self.__students)


class LastNameFirstLetterChecker(IStudentChecker):
    """Проверяет первую букву фамилии.

    Args:
        letters: допустимые первые буквы (в верхнем регистре).
    """

    def __init__(self, letters: str) -> None:
        self.__letters = letters.upper()

    def check(self, student: Student) -> bool:
        return student.full_name.last_name[0].upper() in self.__letters


class StudentFilter(IStudentFilter):
    """Оставляет студентов, подходящих под условие.

    Args:
        checker: условие отбора.
    """

    def __init__(self, checker: IStudentChecker) -> None:
        self.__checker = checker

    def filter(self, students: List[Student]) -> List[Student]:
        return [student for student in students if self.__checker.check(student)]


class FullNameFormatter(IFullNameFormatter):
    """Записывает ФИО как «Фамилия Имя Отчество»."""

    def format(self, full_name: FullName) -> str:
        return f"{full_name.last_name} {full_name.first_name} {full_name.middle_name}"


class ExamStudentFormatter(IStudentFormatter):
    """Описание студента без автомата.

    Args:
        full_name_formatter: как записывать ФИО.
    """

    def __init__(self, full_name_formatter: IFullNameFormatter) -> None:
        self.__full_name_formatter = full_name_formatter

    def format(self, student: Student) -> str:
        name = self.__full_name_formatter.format(student.full_name)
        return f"{name}: без автомата, балл за экзамен {student.exam_score}"


class OlympiadStudentFormatter(IStudentFormatter):
    """Описание студента с автоматом за олимпиаду.

    Args:
        full_name_formatter: как записывать ФИО.
    """

    def __init__(self, full_name_formatter: IFullNameFormatter) -> None:
        self.__full_name_formatter = full_name_formatter

    def format(self, student: Student) -> str:
        name = self.__full_name_formatter.format(student.full_name)
        return f"{name}: автомат, основание - {student.basis}"


class ControlWorkStudentFormatter(IStudentFormatter):
    """Описание студента с автоматом за контрольные работы.

    Args:
        full_name_formatter: как записывать ФИО.
    """

    def __init__(self, full_name_formatter: IFullNameFormatter) -> None:
        self.__full_name_formatter = full_name_formatter

    def format(self, student: Student) -> str:
        name = self.__full_name_formatter.format(student.full_name)
        return (f"{name}: автомат, основание - {student.basis}, "
                f"средний балл за к/р {student.average_score:.2f}")


class StudentFormatterByType(IStudentFormatter):
    """Выбирает форматировщик по классу студента.

    Новый тип студента подключается добавлением пары в словарь,
    сам класс при этом не меняется.

    Args:
        formatters: класс студента -> форматировщик.
    """

    def __init__(self, formatters: Dict[type, IStudentFormatter]) -> None:
        self.__formatters = dict(formatters)

    def format(self, student: Student) -> str:
        """Raises: TypeError, если для типа студента нет форматировщика."""
        formatter = self.__formatters.get(type(student))
        if formatter is None:
            raise TypeError(f"нет форматировщика для {type(student).__name__}")
        return formatter.format(student)


class StudentPrinter(IStudentPrinter):
    """Выводит пронумерованный список студентов с заголовком.

    Args:
        formatter: как описывать студента.
        output: куда выводить.
        title: заголовок списка.
        empty_message: что вывести, если список пуст.
    """

    def __init__(self, formatter: IStudentFormatter, output: IOutput,
                 title: str, empty_message: str) -> None:
        self.__formatter = formatter
        self.__output = output
        self.__title = title
        self.__empty_message = empty_message

    def print_students(self, students: List[Student]) -> None:
        self.__output.write("")
        self.__output.write(self.__title)
        if not students:
            self.__output.write(self.__empty_message)
            return
        for number, student in enumerate(students, start=1):
            self.__output.write(f"{number}. {self.__formatter.format(student)}")


# =============================================================================
# Сценарии
# =============================================================================

class StudentInputScenario(IRunnable):
    """Управляет вводом студентов: тип -> ФИО -> данные типа -> сохранение.

    Args:
        kind_reader: получение типа студента.
        full_name_reader: получение ФИО.
        creators: ключ типа -> создатель студента этого типа.
        receiver: куда добавлять студентов.
        output: куда писать сообщения.
    """

    def __init__(self, kind_reader: IStudentKindReader, full_name_reader: IFullNameReader,
                 creators: Dict[str, IStudentCreator], receiver: IStudentReceiver,
                 output: IOutput) -> None:
        self.__kind_reader = kind_reader
        self.__full_name_reader = full_name_reader
        self.__creators = dict(creators)
        self.__receiver = receiver
        self.__output = output

    def run(self) -> None:
        added_count = 0
        while True:
            kind = self.__kind_reader.read_kind()
            if kind is None:
                break
            full_name = self.__full_name_reader.read_full_name()
            student = self.__creators[kind].create(full_name)
            self.__receiver.add(student)
            added_count += 1
            self.__output.write(f"Студент {full_name.last_name} добавлен.")
        self.__output.write(f"Ввод завершён. Добавлено студентов: {added_count}.")


class Task(IRunnable):
    """Главный сценарий: ввод, отбор, вывод.

    Args:
        input_scenario: ввод студентов.
        provider: откуда брать студентов.
        student_filter: отбор нужных студентов.
        printer: вывод результата.
    """

    def __init__(self, input_scenario: IRunnable, provider: IStudentProvider,
                 student_filter: IStudentFilter, printer: IStudentPrinter) -> None:
        self.__input_scenario = input_scenario
        self.__provider = provider
        self.__student_filter = student_filter
        self.__printer = printer

    def run(self) -> None:
        self.__input_scenario.run()
        students = self.__student_filter.filter(self.__provider.get_all())
        self.__printer.print_students(students)


# =============================================================================
# Сборка приложения (единственное место, где создаются конкретные классы)
# =============================================================================

class ApplicationBuilder(IApplicationBuilder):
    """Создаёт все объекты и связывает их через конструкторы."""

    STOP_WORD = "стоп"
    FIRST_LETTERS = "АБВГДЕЁЖЗИЙК"
    MIN_SCORE = 2
    MAX_SCORE = 5

    def build(self, user_input: IInput, output: IOutput) -> IRunnable:
        full_name_reader = FullNameReader(
            TextReader(user_input, output, NamePartValidator("Фамилия"), "Фамилия: "),
            TextReader(user_input, output, NamePartValidator("Имя"), "Имя: "),
            TextReader(user_input, output, NamePartValidator("Отчество"), "Отчество: "),
        )
        exam_score_reader = IntReader(
            user_input, output,
            IntRangeValidator("Балл за экзамен", self.MIN_SCORE, self.MAX_SCORE),
            f"Балл за экзамен ({self.MIN_SCORE}-{self.MAX_SCORE}): ",
        )
        average_score_reader = FloatReader(
            user_input, output,
            FloatRangeValidator("Средний балл за к/р", self.MIN_SCORE, self.MAX_SCORE),
            f"Средний балл за к/р ({self.MIN_SCORE}-{self.MAX_SCORE}): ",
        )

        creators: Dict[str, IStudentCreator] = {
            "экзамен": ExamStudentCreator(exam_score_reader),
            "олимпиада": OlympiadStudentCreator(),
            "контрольные": ControlWorkStudentCreator(average_score_reader),
        }
        kind_descriptions = {
            "экзамен": "без автомата, указать балл за экзамен",
            "олимпиада": "автомат за олимпиаду",
            "контрольные": "автомат за контрольные работы, указать средний балл",
        }

        full_name_formatter = FullNameFormatter()
        formatter = StudentFormatterByType({
            ExamStudent: ExamStudentFormatter(full_name_formatter),
            OlympiadStudent: OlympiadStudentFormatter(full_name_formatter),
            ControlWorkStudent: ControlWorkStudentFormatter(full_name_formatter),
        })

        repository = StudentRepository()
        input_scenario = StudentInputScenario(
            StudentKindReader(user_input, output, kind_descriptions, self.STOP_WORD),
            full_name_reader,
            creators,
            repository,
            output,
        )
        printer = StudentPrinter(
            formatter, output,
            "Студенты с фамилией на буквы от А до К:",
            "Таких студентов нет.",
        )
        return Task(
            input_scenario,
            repository,
            StudentFilter(LastNameFirstLetterChecker(self.FIRST_LETTERS)),
            printer,
        )


if __name__ == "__main__":
    ApplicationBuilder().build(ConsoleInput(), ConsoleOutput()).run()
