from __future__ import annotations
import math
import numpy as np
from numpy import ndarray
from KV_abstract import *


class Bilinear_Function_KV(Bilinear_Function_KV_ABC):
    def __init__(self, function_matrix: ndarray):
        """
        Конструктор класса билинейных функций
        :param function_matrix: матрица, в ячейках которой стоят значения билинейной функции на соответствующих парах базисных векторов
        """
        self.matrix = function_matrix

    def apply(self, vector_1: Vector_KV, vector_2: Vector_KV) -> float:
        c1 = vector_1.coordinates  # строка
        c2_trans = np.transpose(vector_2.coordinates)  # столбец
        return round(float(c1 @ self.matrix @ c2_trans), 10)


class Linear_Operator_KV(Linear_Operator_KV_ABC):
    def __init__(self, operator_matrix: ndarray):
        """
        Конструктор класса линейных операторов
        :param operator_matrix: матрица, в i-ом столбце которой стоят координаты i-го базисного вектора
        """
        self.matrix = operator_matrix

    def apply(self, vector: Vector_KV):
        return Vector_KV(coordinates=np.transpose(np.matmul(self.matrix, np.transpose(vector.coordinates))))


class Vector_KV(Vector_KV_ABC):
    # scalar_multiplying = Bilinear_Function_KV(np.identity(3))

    def __init__(self, coordinates: ndarray):
        """
        Конструктор класса векторов E
        :param coordinates: координаты вектора !в стандартном ОНБ!
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

    def __neg__(self):
        return Vector_KV(-self.coordinates)

    def __mul__(self, other: float | Vector_KV) -> float | Vector_KV:
        if isinstance(other, Vector_KV):
            return self.scalar_multiplying.apply(self, other)

        elif isinstance(other, float | int):
            return Vector_KV(self.coordinates * other)

    def __abs__(self) -> float:
        return math.sqrt(self * self)

    def angle(self, other: Vector_KV) -> float:
        return math.acos((self * other) / (abs(self) * abs(other)))

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
