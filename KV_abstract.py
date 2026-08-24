from typing import Self
from abc import ABC, abstractmethod


class Vector_KV_ABC(ABC):

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
    def __mul__(self, other: Self | float) -> float | Self:
        """
        Операция умножения (на число, скалярно с другим вектором), необходимая для определения Евклидового векторного пространства
        :param other: Вектор или число
        :return: Число (скалярное произведение) или вектор соответственно ↑
        """
        pass

    @abstractmethod
    def __abs__(self) -> float:
        """
        Операция измерения длины вектора
        :return: Число (корень из скалярного квадрата)
        """
        pass

    @abstractmethod
    def angle(self, other: Self) -> float:
        """
        Операция измерения угла между двумя векторами
        :param other: Вектор
        :return: Угол между векторами в радианах
        """
        pass

    @abstractmethod
    def scale(self, scalar: float) -> Self:
        """
        Операция увеличения длины вектора в scalar раз с сохранением направления
        :param scalar: Число раз, в которое увеличивается длина вектора
        :return: Вектор
        """
        pass

    @abstractmethod
    def normalize(self) -> Self:
        """
        Операция нормировки вектора
        :return: Нормированный на единицу вектор
        """
        pass


class Bilinear_Function_KV_ABC(ABC):

    @abstractmethod
    def apply(self, vector_1: Vector_KV_ABC, vector_2: Vector_KV_ABC) -> float:
        """
        Применение билинейной функции к 2 векторам
        :param vector_1: первый вектор
        :param vector_2: второй вектор
        :return: Число (значение билинейной функции на паре векторов)
        """
        pass


class Linear_Operator_KV_ABC(ABC):

    @abstractmethod
    def apply(self, vector: Vector_KV_ABC):
        """
        Применение линейного оператора к вектору
        :param vector: Вектор
        :return: Вектор
        """
        pass
