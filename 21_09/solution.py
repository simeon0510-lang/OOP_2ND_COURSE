def triangle_angle_type(a: int, b: int, c: int) -> str:
    """Определяет вид треугольника по углам через квадраты сторон.

    Возвращает:
        "invalid" - треугольник не существует (в том числе вырожденный);
        "right"   - прямоугольный;
        "acute"   - остроугольный;
        "obtuse"  - тупоугольный.
    """
    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"

    # упорядочиваем стороны так, чтобы c была наибольшей
    if a > c:
        a, c = c, a
    if b > c:
        b, c = c, b

    # строгое неравенство треугольника (вырожденный считается несуществующим)
    if a + b <= c:
        return "invalid"

    squares_sum = a * a + b * b
    largest_square = c * c

    if largest_square == squares_sum:
        return "right"
    elif largest_square < squares_sum:
        return "acute"
    else:
        return "obtuse"


if __name__ == "__main__":
    sides = [int(x) for x in input("Введите три стороны через пробел: ").split()]
    print(triangle_angle_type(*sides))
