from __future__ import annotations

from KV import *
from numpy import ndarray
import math
from manim import *


class LineE2:
    def __init__(self, start_point: ndarray, end_point: ndarray):
        """
        Конструктор класса линий в двумерном Евклидовом пространстве
        :param start_point: начальная точка (формата manim, т.е R^3 с z = 0)
        :param end_point: конечная точка (формата manim, т.е R^3 с z = 0)
        """
        self._start_point = start_point[0:2]
        self._end_point = end_point[0:2]
        # print(self.start_point, self.end_point)
        self.direction_vector = Vector_KV(coordinates=self._end_point - self._start_point)
        self.normal_vector = self.rotation_operator_by_angle(math.pi / 2).apply(self.direction_vector).normalize()
        self.free_member = - self.normal_vector.coordinates[0] * self._start_point[0] - self.normal_vector.coordinates[1] * self._start_point[1]

    @property
    def start_manim(self): return np.array([self._start_point[0], self._start_point[1], 0.0])

    @property
    def end_manim(self): return np.array([self._end_point[0], self._end_point[1], 0.0])

    @staticmethod
    def rotation_operator_by_angle(angle: float) -> Linear_Operator_KV:
        return Linear_Operator_KV(np.array([
            [round(math.cos(angle), 10), -round(math.sin(angle), 10)],
            [round(math.sin(angle), 10), round(math.cos(angle), 10)]
        ]))

    def interception(self, other: LineE2) -> ndarray:
        """
        Выискивание пересечения 2 прямых на плоскости методом Крамера
        :param other: другая линия на плоскости
        :return: точка на плоскости
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
            raise ZeroDivisionError
        return np.array([np.linalg.det(x_matrix) / np.linalg.det(system_matrix), np.linalg.det(y_matrix) / np.linalg.det(system_matrix), 0])

    def line_by_angle(self, angle: float, start_point: ndarray, length_scale: float) -> LineE2:
        """
        Выискивание прямой, имеющей с данной прямой заданный угол, с помощью применения ортогонального оператора в E2
        :param length_scale: длина итоговой линии
        :param angle: заданный угол
        :param start_point: начальная точка новой прямой
        :return: прямая на плоскости
        """
        rotation_operator = self.rotation_operator_by_angle(angle)
        new_normal_vector = rotation_operator.apply(self.normal_vector).normalize()
        new_direction_vector = self.rotation_operator_by_angle(math.pi/2).apply(new_normal_vector).normalize()
        return LineE2(start_point, start_point + (new_direction_vector * length_scale).coordinates)

    def angle(self, other: LineE2) -> float:
        return self.normal_vector.angle(other.normal_vector)

    def get_Line(self, **kwargs) -> Line:
        """
        Перевод объекта класса LineE2 в объект класса manim.mobject.geometry.line.Line
        :param kwargs: кастомизация
        :return: manim.mobject.geometry.line.Line
        """
        start_point = np.array([self._start_point[0], self._start_point[1], 0])
        end_point = np.array([self._end_point[0], self._end_point[1], 0])
        return Line(start=start_point, end=end_point, **kwargs)

    def __neg__(self) -> LineE2:
        return LineE2(self._end_point, self._start_point)

    def __abs__(self) -> float:
        return abs(self.direction_vector)


class TriangleE2:
    def __init__(self, A_point: ndarray, B_point: ndarray, C_point: ndarray):
        """
        Конструктор класса треугольников в двумерном Евклидовом пространстве
        :param A_point: Первая вершина
        :param B_point: Вторая вершина
        :param C_point: Третья вершина
        """
        self.A = A_point[0:2]
        self.B = B_point[0:2]
        self.C = C_point[0:2]
        self.AB = LineE2(self.A, self.B)
        self.BC = LineE2(self.B, self.C)
        self.AC = LineE2(self.A, self.C)

    @property
    def perimeter(self) -> float:
        return abs(self.AB) + abs(self.BC) + abs(self.AC)

    @property
    def area(self) -> float:
        return 0.5 * abs(self.height(self.B)) * abs(self.AC)

    @property
    def incenter(self) -> ndarray:
        return self.bisector(self.A).interception(self.bisector(self.B))

    @property
    def inscribed_radius(self) -> float:
        return 2 * self.area / self.perimeter

    @property
    def centroid(self) -> ndarray:
        return self.median(self.A).interception(self.median(self.B))

    @property
    def orthocenter(self) -> ndarray:
        return self.height(self.A).interception(self.height(self.B))

    @property
    def circumscribed_center(self) -> ndarray:
        AB_center = self.AB.get_Line().get_center()[0:2]
        BC_center = self.BC.get_Line().get_center()[0:2]

        median_perpendicular_normalized_AB = self.AB.line_by_angle(math.pi/2, AB_center, 1)
        median_perpendicular_normalized_BC = self.BC.line_by_angle(math.pi/2, BC_center, 1)
        return median_perpendicular_normalized_AB.interception(median_perpendicular_normalized_BC)

    @property
    def circumscribed_radius(self) -> float:
        return abs(LineE2(self.A, self.circumscribed_center))

    def height(self, vertex: ndarray) -> LineE2:
        vertex = vertex[0:2]
        if np.all(vertex == self.A):
            correct_line = self.BC
        elif np.all(vertex == self.B):
            correct_line = self.AC
        elif np.all(vertex == self.C):
            correct_line = self.AB
        else:
            raise TypeError

        normal_line_unnormalized = correct_line.line_by_angle(math.pi / 2, vertex, 1)
        end_point = normal_line_unnormalized.interception(correct_line)
        return LineE2(vertex, end_point)

    def bisector(self, vertex: ndarray) -> LineE2:
        vertex = vertex[0:2]
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
        if angle_value > math.pi / 2:
            angle_value = math.pi - angle_value
        bisector_line_unnormalized = line_main.line_by_angle(angle_value, vertex, 1)
        end_point = bisector_line_unnormalized.interception(correct_line)
        return LineE2(vertex, end_point)

    def median(self, vertex: ndarray) -> LineE2:
        vertex = vertex[0:2]
        if np.all(vertex == self.A):
            correct_line = self.BC
        elif np.all(vertex == self.B):
            correct_line = self.AC
        elif np.all(vertex == self.C):
            correct_line = self.AB
        else:
            raise TypeError
        return LineE2(vertex, correct_line.get_Line().get_center())


if __name__ == "__main__":
    pass



