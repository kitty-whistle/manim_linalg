from abc import ABC, abstractmethod


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
        Операция умножения (на число, скалярно с другим вектором), необходимая для определения Евклидового векторного пространства
        :param other: Объект поля, над которым построено векторное пространство
        :return: Некоторый объект
        """
        pass

    @abstractmethod
    def __abs__(self):
        """
        Операция измерения длины вектора (корня из скалярного квадрата)
        :return: Некоторый объект
        """
        pass

    @abstractmethod
    def angle(self, other):
        """
        Операция измерения угла между двумя векторами
        :param other:
        :return:
        """
        pass


class Bilinear_Function_KV_ABC(ABC):

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
    def apply(self, vector: Vector_KV_ABC):
        """
        Применение линейного оператора к вектору
        :param vector: вектор
        :return: Некоторый объект
        """
        pass
