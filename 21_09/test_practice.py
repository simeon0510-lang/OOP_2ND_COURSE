import unittest

from Practice import (AutomaticStudent, ControlWorkStudent, ExamStudent,
                      OlympiadStudent, Student, StudentGroup)


class TestStudents(unittest.TestCase):

    def test_exam_student(self):
        student = ExamStudent("Иванов", "Иван", "Иванович", 4)
        self.assertEqual(student.last_name, "Иванов")
        self.assertEqual(student.exam_score, 4)
        self.assertEqual(str(student), "Иванов Иван Иванович, экзамен, балл: 4")

    def test_exam_score_bounds(self):
        self.assertEqual(ExamStudent("А", "Б", "В", 2).exam_score, 2)
        self.assertEqual(ExamStudent("А", "Б", "В", 5).exam_score, 5)

    def test_exam_score_too_low(self):
        with self.assertRaises(ValueError):
            ExamStudent("Иванов", "Иван", "Иванович", 1)

    def test_exam_score_too_high(self):
        with self.assertRaises(ValueError):
            ExamStudent("Иванов", "Иван", "Иванович", 6)

    def test_olympiad_student(self):
        student = OlympiadStudent("Ким", "Ли", "Сергеевич")
        self.assertEqual(student.basis, "олимпиада")
        self.assertIn("автомат", str(student))

    def test_control_work_student(self):
        student = ControlWorkStudent("Андреева", "Анна", "Сергеевна", 4.5)
        self.assertEqual(student.basis, "контрольные работы")
        self.assertEqual(student.average_score, 4.5)

    def test_control_work_score_out_of_range(self):
        with self.assertRaises(ValueError):
            ControlWorkStudent("Андреева", "Анна", "Сергеевна", 5.1)

    def test_empty_last_name(self):
        with self.assertRaises(ValueError):
            ExamStudent("", "Иван", "Иванович", 4)

    def test_spaces_only_name(self):
        with self.assertRaises(ValueError):
            OlympiadStudent("Ким", "   ", "Сергеевич")

    def test_abstract_classes(self):
        with self.assertRaises(TypeError):
            Student("Иванов", "Иван", "Иванович")
        with self.assertRaises(TypeError):
            AutomaticStudent("Иванов", "Иван", "Иванович")


class TestStudentGroup(unittest.TestCase):

    def test_add_wrong_object(self):
        with self.assertRaises(TypeError):
            StudentGroup().add_student("Иванов")


if __name__ == "__main__":
    unittest.main()
