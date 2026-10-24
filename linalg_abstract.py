from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod
from numpy import ndarray


class Vector_ABC(ABC):
    @abstractmethod
    def __add__(self, other: Self) -> Self:
        """
        Операция сложения векторов, необходимая для определения векторного пространства
        :param other: Вектор-слагаемое
        :return: Некоторый вектор
        """
        pass

    @abstractmethod
    def __neg__(self) -> Self:
        """
        Операция поиска противоположного вектора
        :return: Противоположный вектор
        """

    @abstractmethod
    def __mul__(self, other: float) -> Self:
        """
        Операция умножения на число.
        :param other: число
        :return: Вектор
        """
        pass


class Basis_ABC(ABC):
    @abstractmethod
    def decompose(self, vector: Vector_ABC) -> ndarray:
        """
        Разложение вектора по базису self
        :param vector:
        :return: вектор столбец координат vector в базисе self
        """

    @abstractmethod
    def get_transition_matrix(self, another_basis: Basis_ABC) -> ndarray:
        """
        Построение матрицы перехода от базиса self к базису another_basis (C: V->V)
        :param another_basis: новый базис
        :return: матрица перехода
        """
        pass


class Linear_Mapping_ABC(ABC):
    @abstractmethod
    def apply(self, vector: Vector_ABC) -> Vector_ABC:
        pass


class Linear_Operator_ABC(ABC):
    @abstractmethod
    def apply(self, vector: Vector_ABC):
        """
        Применение линейного оператора к вектору
        :param vector: Вектор
        :return: Вектор
        """
        pass


class Bilinear_Function_ABC(ABC):

    @abstractmethod
    def apply(self, vector_1: Vector_ABC, vector_2: Vector_ABC) -> float:
        """
        Применение билинейной функции к 2 векторам
        :param vector_1: первый вектор
        :param vector_2: второй вектор
        :return: Число (значение билинейной функции на паре векторов)
        """
        pass







