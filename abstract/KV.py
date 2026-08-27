from __future__ import annotations
import math
import numpy as np
from numpy import ndarray
from abstract.KV_abstract import *


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

    def apply(self, vector: Vector_KV) -> Vector_KV:
        return Vector_KV(coordinates=np.transpose(np.matmul(self.matrix, np.transpose(vector.coordinates))))


class Vector_KV(Vector_KV_ABC):
    def __init__(self, coordinates: ndarray):
        """
        Конструктор класса векторов n-мерного Евклидового пространства в стандартном ОНБ
        :param coordinates: координаты вектора (в стандартном ОНБ)
        """
        self.coordinates = coordinates

        # Матрица скалярного произведения единичная ↓
        self.scalar_multiplying = Bilinear_Function_KV(np.identity(len(coordinates)))

    def __add__(self, other: Self) -> Self:
        return Vector_KV(self.coordinates + other.coordinates)

    def __neg__(self) -> Self:
        return Vector_KV(-self.coordinates)

    def __mul__(self, other: Self | float) -> float | Self:
        if isinstance(other, Vector_KV):
            return self.scalar_multiplying.apply(self, other)

        elif isinstance(other, float | int):
            return Vector_KV(self.coordinates * other)

        raise TypeError("Unsupported operand type")

    def vec_mul(self, other: Self) -> Self:
        vec_mul_self_matrix = np.array([
            [0, -self.coordinates[2], self.coordinates[1]],
            [self.coordinates[2], 0, -self.coordinates[0]],
            [-self.coordinates[1], -self.coordinates[0], 0],
        ])

        return Linear_Operator_KV(vec_mul_self_matrix).apply(other)


    def __abs__(self) -> float:
        return math.sqrt(self * self)

    def angle(self, other: Self) -> float:
        return math.acos((self * other) / (abs(self) * abs(other)))

    def scale(self, scalar: float) -> Self:
        if scalar == 0:
            raise ZeroDivisionError

        self.coordinates *= (1 / scalar)
        return self

    def normalize(self) -> Self:
        normalization = 0
        for i in self.coordinates:
            normalization += i**2
        normalization = normalization ** (1 / 2)
        return self.scale(normalization)
