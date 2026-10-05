from solution import triangle_angle_type
import unittest


class TestTriangleAngleType(unittest.TestCase):

    # --- прямоугольный ---
    def test_right_classic(self):
        self.assertEqual(triangle_angle_type(3, 4, 5), "right")

    def test_right_largest_side_first(self):
        self.assertEqual(triangle_angle_type(5, 3, 4), "right")

    def test_right_largest_side_middle(self):
        self.assertEqual(triangle_angle_type(4, 5, 3), "right")

    def test_right_bigger_numbers(self):
        self.assertEqual(triangle_angle_type(5, 12, 13), "right")

    # --- остроугольный ---
    def test_acute_equilateral(self):
        self.assertEqual(triangle_angle_type(1, 1, 1), "acute")

    def test_acute_isosceles(self):
        self.assertEqual(triangle_angle_type(5, 5, 6), "acute")

    def test_acute_just_before_right(self):
        # 4^2 = 16 < 3^2 + 4^2 = 25 -> граница со стороны острого угла
        self.assertEqual(triangle_angle_type(3, 4, 4), "acute")

    # --- тупоугольный ---
    def test_obtuse(self):
        self.assertEqual(triangle_angle_type(2, 3, 4), "obtuse")

    def test_obtuse_just_after_right(self):
        # 6^2 = 36 > 3^2 + 4^2 = 25 -> граница со стороны тупого угла
        self.assertEqual(triangle_angle_type(3, 4, 6), "obtuse")

    def test_obtuse_largest_side_first(self):
        self.assertEqual(triangle_angle_type(4, 2, 3), "obtuse")

    # --- вырожденный и несуществующий ---
    def test_degenerate(self):
        self.assertEqual(triangle_angle_type(1, 2, 3), "invalid")

    def test_degenerate_other_order(self):
        self.assertEqual(triangle_angle_type(3, 1, 2), "invalid")

    def test_impossible(self):
        self.assertEqual(triangle_angle_type(1, 1, 5), "invalid")

    def test_impossible_largest_side_middle(self):
        self.assertEqual(triangle_angle_type(1, 10, 2), "invalid")

    def test_zero_side(self):
        self.assertEqual(triangle_angle_type(0, 4, 5), "invalid")

    def test_all_zero(self):
        self.assertEqual(triangle_angle_type(0, 0, 0), "invalid")

    def test_negative_side(self):
        self.assertEqual(triangle_angle_type(-3, 4, 5), "invalid")


if __name__ == "__main__":
    unittest.main()
