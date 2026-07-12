from __future__ import annotations

from abc import ABC, abstractmethod
from numpy import ndarray
import math
from manim import *


class Vector_KV_ABC(ABC):

    @abstractmethod
    def __add__(self, other):
        """
        Операция сложения векторов, необходимая для определения векторного пространства
        :param other: Объект-слагаемое
        :return: Некоторый объект
        """
        pass

    @abstractmethod
    def __mul__(self, other):
        """
        Операция умножения (на число), необходимая для определения векторного пространства
        :param other: Объект поля, над которым построено векторное пространство
        :return: Некоторый объект
        """
        pass


class Bilinear_Function_KV_ABC(ABC):
    @abstractmethod
    def __init__(self, function_matrix: ndarray):
        """
        Конструктор класса билинейных функций
        :param function_matrix:
        Матрица, элементы которой есть значения функции на соответствующих парах базисных векторов
        """
        pass

    @abstractmethod
    def apply(self, vector_1: Vector_KV_ABC, vector_2: Vector_KV_ABC):
        """
        Применение билинейной функции к 2 векторам alpha(vector_1, vector_2)
        :param vector_1: первый вектор
        :param vector_2: второй вектор
        :return: Некоторый объект
        """
        pass


class Linear_Operator_KV_ABC(ABC):
    @abstractmethod
    def __init__(self, operator_matrix: ndarray):
        """
        Конструктор класса линейных операторов
        :param operator_matrix:
        Матрица, i-ый столбец которой - координаты образа i-го базисного вектора
        """
        pass

    @abstractmethod
    def apply(self, vector: Vector_KV_ABC):
        """
        Применение линейного оператора к вектору
        :param vector: вектор
        :return: Некоторый объект
        """
        pass


class Bilinear_Function_KV(Bilinear_Function_KV_ABC):
    def __init__(self, function_matrix: ndarray):
        self.matrix = function_matrix

    def apply(self, vector_1: Vector_KV, vector_2: Vector_KV) -> float:
        c1 = vector_1.coordinates  # строка
        c2_trans = np.transpose(vector_2.coordinates)  # столбец
        return float(c1 @ self.matrix @ c1)


class Linear_Operator_KV(Linear_Operator_KV_ABC):

    def __init__(self, operator_matrix: ndarray):
        self.matrix = operator_matrix

    def apply(self, vector: Vector_KV):
        return Vector_KV(coordinates=np.transpose(np.matmul(self.matrix, np.transpose(vector.coordinates))))


class Vector_KV(Vector_KV_ABC):
    # scalar_multiplying = Bilinear_Function_KV(np.identity(3))

    def __init__(self, coordinates: ndarray):
        """
        Конструктор класса векторов E3
        :param coordinates: координаты вектора в стандартном ОНБ
        """
        self.coordinates = coordinates
        self.scalar_multiplying = Bilinear_Function_KV(np.identity(len(coordinates)))
        # self.vector_multiplying_operator = Linear_Operator_KV(np.array([
        #     [0, -coordinates[2], coordinates[1]],
        #     [coordinates[2], 0, -coordinates[0]],
        #     [-coordinates[1], coordinates[0], 0]
        # ]))

    def __add__(self, other: Vector_KV) -> Vector_KV:
        return Vector_KV(self.coordinates + other.coordinates)

    def __mul__(self, other: float | Vector_KV) -> float | Vector_KV:
        if isinstance(other, Vector_KV):
            return self.scalar_multiplying.apply(self, other)

        elif isinstance(other, float | int):
            return Vector_KV(self.coordinates * other)

    def __abs__(self) -> float:
        return math.sqrt(self.scalar_multiplying.apply(self, self))

    # def vector_mul(self, other: VectorE3_KV) -> VectorE3_KV:
    #     return self.vector_multiplying_operator.apply(other)

    def scale(self, scalar: float) -> Vector_KV:
        self.coordinates *= (1 / scalar)
        return self

    def normalize(self) -> Vector_KV:
        normalization = 0
        for i in self.coordinates:
            normalization += i**2
        normalization = normalization ** (1 / 2)
        return self.scale(normalization)


class LineE2:
    def __init__(self, start_point: ndarray, end_point: ndarray):
        self.start_point = start_point
        self.end_point = end_point
        self.direction_vector = Vector_KV(coordinates=end_point - start_point).normalize()
        self.normal_vector = self.rotation_operator_by_angle(math.pi / 2).apply(self.direction_vector).normalize()
        self.free_member = - self.normal_vector.coordinates[0] * self.start_point[0] - self.normal_vector.coordinates[1] * self.start_point[1]

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

    def get_Line(self, **kwargs) -> Line:
        start_point = np.array([self.start_point[0], self.start_point[1], 0])
        end_point = np.array([self.end_point[0], self.end_point[1], 0])
        return Line(start=start_point, end=end_point, **kwargs)


if __name__ == "__main__":
    A = Dot(ORIGIN, radius=0.05)
    B = Dot(ORIGIN + 2 * RIGHT, radius=0.05)
    C = Dot(ORIGIN + 2 * LEFT + 2 * UP, radius=0.05)
    D = Dot(ORIGIN + 3 * UP + 1 * LEFT, radius=0.05)
    ab = LineE2(A.get_center()[0:2], B.get_center()[0:2])
    cd = LineE2(C.get_center()[0:2], D.get_center()[0:2])
    print(ab.interception(cd))




