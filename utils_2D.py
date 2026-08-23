from __future__ import annotations

from KV import *
from numpy import ndarray
import math
from manim import *


class LineE2:
    def __init__(self, start_point: ndarray, end_point: ndarray):
        """
        Конструктор класса линий (т.е отрезков прямой) в двумерном Евклидовом пространстве
        :param start_point: начальная точка R^2, т.е (x, y)
        :param end_point: конечная точка R^2, т.е (x, y)
        """
        self.start_point = start_point
        self.end_point = end_point

        # Ненормированный вектор, соединяющий две точки (т.е направленный отрезок прямой) ↓
        self.direction_vector = Vector_KV(coordinates=self.end_point - self.start_point)

        # Нормированный вектор нормали (для составления уравнения прямой в E^2) ↓
        self.normal_vector = self.rotation_operator_by_angle(math.pi / 2).apply(self.direction_vector).normalize()

        # Свободный член уравнения прямой в E^2 (Ax + By + C = 0, C := self.free_member)
        self.free_member = - self.normal_vector.coordinates[0] * self.start_point[0] - self.normal_vector.coordinates[1] * self.start_point[1]

    @staticmethod
    def make_R3(point: ndarray) -> ndarray:
        """
        Преобразование точки R^2 в R^3 (для корректной работы manim в 2D)
        :param point: Точка в R^2
        :return: Точка в R^3
        """
        return np.array([point[0], point[1], 0.0])

    @property
    def start_manim(self) -> ndarray:
        """
        Преобразование start_point R^2 в R^3 (для корректной работы manim в 2D)
        :return: точка R^3
        """
        return self.make_R3(self.start_point)

    @property
    def end_manim(self):
        """
        Преобразование end_point R^2 в R^3 (для корректной работы manim в 2D)
        :return: точка R^3
        """
        return self.make_R3(self.end_point)

    @staticmethod
    def rotation_operator_by_angle(angle: float) -> Linear_Operator_KV:
        """
        Создание ортогонального оператора для поворота вектора E^2 на угол angle
        :param angle: угол поворота (против часовой стрелки)
        :return: Ортогональный оператор поворота
        """
        return Linear_Operator_KV(np.array([
            [round(math.cos(angle), 10), -round(math.sin(angle), 10)],
            [round(math.sin(angle), 10), round(math.cos(angle), 10)]
        ]))

    def intersection(self, other: Self) -> ndarray:
        """
        Выискивание пересечения двух линий (возможно их продолжений) методом Крамера
        :param other: линия
        :return: точка в R^2
        """
        x_matrix = np.array([
            [-self.free_member, self.normal_vector.coordinates[1]],
            [-other.free_member, other.normal_vector.coordinates[1]],
        ])

        y_matrix = np.array([
            [self.normal_vector.coordinates[0], -self.free_member],
            [other.normal_vector.coordinates[0], -other.free_member],
        ])

        system_matrix = np.array([
            [self.normal_vector.coordinates[0], self.normal_vector.coordinates[1]],
            [other.normal_vector.coordinates[0], other.normal_vector.coordinates[1]],
        ])

        if np.linalg.det(system_matrix) == 0:
            raise ZeroDivisionError("Determinant is zero (Lines are parallel)")
        return np.array([np.linalg.det(x_matrix) / np.linalg.det(system_matrix), np.linalg.det(y_matrix) / np.linalg.det(system_matrix)])

    def line_by_angle(self, angle: float, start_point: ndarray, length_scale: float) -> Self:
        """
        Выискивание линии длины length_scale, имеющей с данной линией заданный угол angle в E^2
        :param length_scale: длина линии
        :param angle: заданный угол
        :param start_point: начальная точка новой линии
        :return: линия в E^2
        """
        rotation_operator = self.rotation_operator_by_angle(angle)
        new_normal_vector = rotation_operator.apply(self.normal_vector).normalize()
        new_direction_vector = self.rotation_operator_by_angle(math.pi/2).apply(new_normal_vector).normalize()
        return LineE2(start_point, start_point + (new_direction_vector * length_scale).coordinates)

    def angle(self, other: Self) -> float:
        """
        Операция измерения угла между направляющими векторами линий self и other
        :param other:
        :return:
        """
        return self.normal_vector.angle(other.normal_vector)

    def get_Line(self, **kwargs) -> Line:
        """
        Перевод объекта класса LineE2 в объект класса manim.mobject.geometry.line.Line
        :param kwargs: кастомизация (manim)
        :return: manim.mobject.geometry.line.Line
        """
        return Line(start=self.start_manim, end=self.end_manim, **kwargs)

    def get_Arrow(self, **kwargs) -> Arrow:
        """
        Перевод объекта класса LineE2 в объект класса manim.mobject.geometry.arrow.Arrow
        :param kwargs: кастомизация (manim)
        :return: manim.mobject.geometry.arrow.Arrow
        """
        return Arrow(start=self.start_manim, end=self.end_manim, **kwargs)

    def scale(self, scalar: float) -> Self:
        """
        Операция увеличения длины направляющего вектора (длины линии вдоль направления direction_vector) в scalar раз с сохранением направления
        :param scalar: Число раз, в которое увеличивается линия
        :return: Линия
        """
        return LineE2(self.start_point, self.start_point + (self.direction_vector * scalar).coordinates)

    def __neg__(self) -> Self:
        """
        Получение линии с противоположным направляющим вектором (direction_vector)
        :return:
        """
        return LineE2(self.end_point, self.start_point)

    def __abs__(self) -> float:
        """
        Операция измерения длины линии (длины направляющего вектора direction_vector)
        :return: Число
        """
        return abs(self.direction_vector)


class TriangleE2:
    def __init__(self, A: ndarray, B: ndarray, C: ndarray):
        """
        Конструктор класса треугольников в двумерном Евклидовом пространстве
        :param A: Первая вершина
        :param B: Вторая вершина
        :param C: Третья вершина
        """
        self.A = A[0:2]
        self.B = B[0:2]
        self.C = C[0:2]
        self.AB = LineE2(self.A, self.B)
        self.BC = LineE2(self.B, self.C)
        self.AC = LineE2(self.A, self.C)

    @property
    def perimeter(self) -> float:
        """
        Вычисление периметра треугольника
        :return: Периметр
        """
        return abs(self.AB) + abs(self.BC) + abs(self.AC)

    @property
    def area(self) -> float:
        """
        Вычисление площади треугольника
        :return: Площадь
        """
        return 0.5 * abs(self.height(self.B)) * abs(self.AC)

    @property
    def incenter(self) -> ndarray:
        """
        Вычисление координаты центра вписанной окружности треугольника
        :return: Точка R^2
        """
        return self.bisector(self.A).intersection(self.bisector(self.B))

    @property
    def inscribed_radius(self) -> float:
        """
        Вычисление радиуса вписанной окружности треугольника
        :return: Длина радиуса
        """
        return 2 * self.area / self.perimeter

    @property
    def centroid(self) -> ndarray:
        """
        Вычисление координаты центра масс треугольника
        :return: Точка R^2
        """
        return self.median(self.A).intersection(self.median(self.B))

    @property
    def orthocenter(self) -> ndarray:
        """
        Вычисление координаты ортоцентра треугольника
        :return: Точка R^2
        """
        return self.height(self.A).intersection(self.height(self.B))

    @property
    def circumscribed_center(self) -> ndarray:
        """
        Вычисление центра описанной вокруг треугольника окружности
        :return: Точка R^2
        """
        AB_center = self.AB.get_Line().get_center()[0:2]
        BC_center = self.BC.get_Line().get_center()[0:2]

        median_perpendicular_normalized_AB = self.AB.line_by_angle(math.pi/2, AB_center, 1)
        median_perpendicular_normalized_BC = self.BC.line_by_angle(math.pi/2, BC_center, 1)
        return median_perpendicular_normalized_AB.intersection(median_perpendicular_normalized_BC)

    @property
    def circumscribed_radius(self) -> float:
        """
        Вычисление радиуса описанной вокруг треугольника окружности
        :return: Длина радиуса описанной окружности
        """
        return abs(LineE2(self.A, self.circumscribed_center))

    def height(self, vertex: ndarray) -> LineE2:
        """
        Построение высоты треугольника из указанной вершины
        :param vertex: Вершина треугольника, из которой проводится высота (точка R^2)
        :return: Высота (линия LineE2)
        """
        if np.all(vertex == self.A):
            correct_line = self.BC
        elif np.all(vertex == self.B):
            correct_line = self.AC
        elif np.all(vertex == self.C):
            correct_line = self.AB
        else:
            raise TypeError

        normal_line_unnormalized = correct_line.line_by_angle(math.pi / 2, vertex, 1)
        end_point = normal_line_unnormalized.intersection(correct_line)
        return LineE2(vertex, end_point)

    def bisector(self, vertex: ndarray) -> LineE2:
        """
        Построение биссектрисы треугольника из указанной вершины
        :param vertex: Вершина треугольника, из которой проводится биссектриса (точка R^2)
        :return: Биссектриса (линия LineE2)
        """
        if np.all(vertex == self.A):
            line_main = self.AC
            line_angle = self.AB
            correct_line = self.BC
        elif np.all(vertex == self.B):
            line_main = -self.AB
            line_angle = self.BC
            correct_line = self.AC
        elif np.all(vertex == self.C):
            line_main = -self.BC
            line_angle = -self.AC
            correct_line = self.AB
        else:
            raise TypeError

        angle_value = line_main.angle(line_angle) / 2

        bisector_line_unnormalized_1 = line_main.line_by_angle(angle_value, vertex, 1)
        end_point_1 = bisector_line_unnormalized_1.intersection(correct_line)

        bisector_line_unnormalized_2 = line_angle.line_by_angle(angle_value, vertex, 1)
        end_point_2 = bisector_line_unnormalized_2.intersection(correct_line)

        bis_1 = LineE2(vertex, end_point_1)
        bis_2 = LineE2(vertex, end_point_2)

        if round(bis_1.angle(line_angle), 3) == round(bis_2.angle(line_angle), 3):
            return bis_1
        return bis_2

    def median(self, vertex: ndarray) -> LineE2:
        """
        Построение медианы треугольника из указанной вершины
        :param vertex: Вершина треугольника, из которой проводится медиана (точка R^2)
        :return: Медиана (линия LineE2)
        """
        if np.all(vertex == self.A):
            correct_line = self.BC
        elif np.all(vertex == self.B):
            correct_line = self.AC
        elif np.all(vertex == self.C):
            correct_line = self.AB
        else:
            raise TypeError
        return LineE2(vertex, correct_line.get_Line().get_center())

    def unsigned_circle_center(self, vertex: ndarray) -> ndarray:
        """
        Вычисление координаты центра вневписанной окружности треугольника, построенной на угле с вершиной vertex
        :param vertex: Вершина треугольника, на угле которой построена окружность (точка R^2)
        :return: Точка R^2
        """
        if np.all(vertex == self.A):
            first_direction = self.AB
            common_direction = self.BC
            intercept_direction = self.AC
        elif np.all(vertex == self.B):
            first_direction = -self.AB
            common_direction = self.AC
            intercept_direction = self.BC
        elif np.all(vertex == self.C):
            first_direction = -self.AC
            common_direction = self.AB
            intercept_direction = -self.BC

        else:
            raise TypeError

        angle_value = first_direction.angle(common_direction) / 2

        bis_line_unnormalized_1 = first_direction.line_by_angle(angle_value, first_direction.end_point, 1)
        end_point_1 = bis_line_unnormalized_1.intersection(intercept_direction)

        bis_line_unnormalized_2 = common_direction.line_by_angle(angle_value, first_direction.end_point, 1)
        end_point_2 = bis_line_unnormalized_2.intersection(intercept_direction)

        bis_1 = LineE2(first_direction.end_point, end_point_1)
        bis_2 = LineE2(first_direction.end_point, end_point_2)

        if round(bis_1.angle(common_direction), 3) == round(bis_1.angle(first_direction), 3):
            return bis_1.intersection(self.bisector(vertex))
        return bis_2.intersection(self.bisector(vertex))

    def unsigned_circle_radius(self, vertex: ndarray) -> float:
        """
        Вычисление радиуса вневписанной окружности треугольника, построенной на угле с вершиной vertex
        :param vertex: Вершина треугольника, на угле которой построена окружность (точка R^2)
        :return: Длина радиуса
        """
        if np.all(vertex == self.A):
            common_direction = self.BC
        elif np.all(vertex == self.B):
            common_direction = self.AC
        elif np.all(vertex == self.C):
            common_direction = self.AB
        else:
            raise TypeError

        return self.area / (0.5 * self.perimeter - abs(common_direction.direction_vector))


if __name__ == "__main__":
    pass
