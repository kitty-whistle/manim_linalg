from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod

from manim import Line, Line3D
from numpy import ndarray
from manim import Surface
# from utils_2D import LineE2


class Linear_Surface(ABC):
    pass


class Line_KV(ABC):
    @abstractmethod
    def intersection(self, other: Self | Plane_KV) -> ndarray:
        """
        Выискивание точки пересечения двух объектов (прямая - плоскость, прямая - прямая)
        :param other: Плоскость или прямая
        :return: Точка пересечения
        """
        pass

    @abstractmethod
    def line_by_angle(self, **kwargs) -> Self:
        """
        Выискивание линии, имеющей с данной заданный угол относительно оси
        :param kwargs: необходимые объекты
        :return: линия
        """
        pass

    @abstractmethod
    def angle(self, other: Self | Plane_KV) -> float:
        """
        Операция измерения угла между объектами (прямая - плоскость, прямая - прямая)
        :param other: Плоскость или прямая
        :return: угол в радианах
        """
        pass

    @abstractmethod
    def projection(self, point: ndarray) -> ndarray:
        """
        Вычисление координат проекции точки на прямую
        :param point: Проекционная точка
        :return: Проекция (0-мерная ортогональная составляющая)
        """
        pass

    @abstractmethod
    def get_Line(self, **kwargs) -> Line | Line3D:
        """
        Перевод объекта Self в объект manim
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def scale(self, scalar: float) -> Self:
        """
        Операция увеличения длины линии в scalar раз по обеим направлениям
        :param scalar: Число раз, в которое увеличивается линия
        :return: Линия
        """
        pass

    @abstractmethod
    def __neg__(self) -> Self:
        """
        Получение линии с противоположным направляющим вектором
        :return:
        """
        pass

    @abstractmethod
    def __abs__(self) -> Self:
        """
        Операция измерения длины линии (длины направляющего вектора direction_vector)
        :return:
        """
        pass


class Plane_KV(ABC):

    @abstractmethod
    def intersection(self, other: Self | Line_KV) -> ndarray:
        """
        Выискивание точки пересечения двух объектов (плоскость - плоскость, плоскость - прямая)
        :param other: Плоскость или прямая
        :return: Точка пересечения
        """
        pass

    @abstractmethod
    def plane_by_angle(self, **kwargs) -> Self:
        """
        Выискивание плоскости, имеющей с данной заданный угол
        :param kwargs: необходимые объекты
        :return: плоскость
        """

    @abstractmethod
    def angle(self, other: Self | Line_KV) -> float:
        """
        Операция измерения угла между объектами (плоскость - прямая, плоскость - прямая)
        :param other: Плоскость или прямая
        :return: угол в радианах
        """
        pass

    @abstractmethod
    def projection(self, other: Line_KV | ndarray) -> Line_KV | ndarray:
        """
        Вычисление координат проекции точки или прямой на плоскость
        :param other: Проекционная точка, Проекционная прямая
        :return: Проекция (0,1-мерная ортогональная составляющая)
        """
        pass

    @abstractmethod
    def get_Plane(self, **kwargs) -> Surface:
        """
        Перевод объекта Self в объект manim
        :param kwargs: Кастомизация
        :return:
        """
        pass








