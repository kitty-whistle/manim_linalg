from __future__ import annotations
from typing import Self
from abc import ABC, abstractmethod
from numpy import ndarray


class Vector_ABC(ABC):
    """
    Класс векторов n-мерного линейного пространства V
    """

    @abstractmethod
    def __add__(self, another: Self) -> Self:
        """
        Операция сложения векторов, необходимая для определения векторного пространства
        :param another: Вектор-слагаемое
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
    def __mul__(self, another: float) -> Self:
        """
        Операция умножения на число
        :param another: число
        :return: Вектор
        """
        pass

    @abstractmethod
    def change_basis(self, another_basis: Basis_ABC) -> Self:
        """
        Смена базиса, в котором задан вектор self, на another_basis
        :param another_basis: Новый базис линейного пространства V, в котором необходимо задать вектор self
        :return: self в новом базисе
        """
        pass


class Basis_ABC(ABC):
    """
    Класс базисов n-мерного линейного пространства V
    """

    @abstractmethod
    def decompose(self, vector: Vector_ABC) -> ndarray:
        """
        Разложение вектора vector по базису self
        :param vector:
        :return: вектор строка координат vector в базисе self
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
    """
    Класс линейных отображений φ: V -> W
    """

    @abstractmethod
    def change_basis(self, another_basis_V: Basis_ABC, another_basis_W: Basis_ABC) -> Self:
        """
        Смена базисов, в котором задано линейное отображение на another_basis_V, another_basis_W
        :param another_basis_V: Новый базиc линейного пространства V
        :param another_basis_W: Новый базис линейного пространства W
        :return: self в новых базисах (по сути меняется только матрица)
        """
        pass

    @abstractmethod
    def apply(self, vector: Vector_ABC) -> Vector_ABC:
        """
        Применение линейного отображения к вектору vector
        :param vector: Вектор, к которому применяют линейное отображение
        :return: Образ вектора vector в линейном пространстве W
        """
        pass


class Linear_Operator_ABC(ABC):
    """
    Класс линейных операторов φ: V -> V
    """

    @abstractmethod
    def change_basis(self, another_basis: Basis_ABC) -> Self:
        """
        Смена базиса, в котором задано линейное отображение на another_basis
        :param another_basis: Новый базис линейного пространства V
        :return: self в новом базисе (по сути меняется только матрица)
        """

    @abstractmethod
    def apply(self, vector: Vector_ABC) -> Vector_ABC:
        """
        Применение линейного оператора к вектору vector
        :param vector: Вектор, к которому применяют линейное отображение
        :return: Образ вектора vector в линейном пространстве W
        """

    @abstractmethod
    def calculate_eigenvalues_and_eigenvectors(self) -> dict[float, Vector_ABC]:
        """
        Определение собственных значений и соответствующих им собственных векторов линейного оператора φ
        :return: словарь из собственных значений и соответствующих им собственный значений
        """
        pass

    @abstractmethod
    def diagonalize(self) -> Self:
        """
        Задание оператора в "хорошем" базисе, т.е в базисе из собственных векторов + стандартное дополнение до E^n
        Замечание 1: Если оператор диагонализуем, то возвращение оператора в базисе из собственных векторов
        Замечание 2: Если ранее оператор был задан в каком-то базисе, то от него ничего не останется
        """
        pass


class Bilinear_Function_ABC(ABC):
    """
    Класс билинейных функций β: V × V -> R
    """

    @abstractmethod
    def change_basis(self, another_basis: Basis_ABC) -> Self:
        """
        Смена базиса, в котором задана билинейная функция на another_basis
        :param another_basis: Новый базис линейного пространства V
        :return: self в новом базисе (по сути меняется только матрица)
        """

    @abstractmethod
    def apply(self, vector_1: Vector_ABC, vector_2: Vector_ABC) -> float:
        """
        Применение билинейной функции к 2 векторам
        :param vector_1: первый вектор
        :param vector_2: второй вектор
        :return: Число (значение билинейной функции на паре векторов)
        """
        pass


class VectorE_ABC(Vector_ABC, ABC):
    """
    Класс векторов n-мерного линейного евклидового пространства E
    """

    @abstractmethod
    def __mul__(self, another: float | Self) -> Self | float:
        """
        Операция умножения (на число, скалярно с другим вектором), необходимая для определения Евклидового векторного пространства
        :param another: Вектор или число
        :return: Число (скалярное произведение) или вектор соответственно ↑
        """
        pass

    @abstractmethod
    def __abs__(self) -> Self:
        """
        Операция измерения длины вектора
        :return: Число (корень из скалярного квадрата)
        """
        pass

    @abstractmethod
    def angle(self, another: Self) -> float:
        """
        Операция измерения угла между двумя векторами
        :param another: Вектор
        :return: Угол между векторами в радианах
        """
        pass

    @abstractmethod
    def normalize(self) -> Self:
        """
        Операция нормировки вектора
        :return: Нормированный на единицу вектор
        """
        pass

    @abstractmethod
    def get_orthogonal_projection(self, subspace_basis: BasisE_ABC) -> ndarray:
        """
        Вычисление ортогональной проекции вектора self на подпространство, порожденное линейной оболочкой subspace_basis
        :param subspace_basis: Базис подпространства к пространству, порожденному базисом self.basis
        :return: Координаты вектора-проекции вектора self на подпространство, порожденное базисом subspace_basis
        """
        pass

    @abstractmethod
    def get_orthogonal_component(self, subspace_basis: BasisE_ABC) -> ndarray:
        """
        Вычисление ортогональной составляющей вектора к подпространству, порожденному линейной оболочкой subspace_basis
        :param subspace_basis: Базис подпространства к пространству, порожденному self.basis
        :return: Координаты вектора, являющегося ортогональной составляющей вектора self к подпространству, порожденному базисом subspace_basis
        """
        pass


class BasisE_ABC(Basis_ABC, ABC):

    @abstractmethod
    def normalize(self) -> Self:
        """
        Построение ОНБ из self методом Грамма-Шмидта
        """
        pass

    # @abstractmethod
    # def get_orthogonal_complement_basis(self, subspace_basis: BasisE_ABC) -> Self:
    #     """
    #     Построение базиса ортогонального дополнение к линейному пространству, порожденному базисом subspace_basis
    #     :param subspace_basis: Базис подпространства линейного пространства, порожденного линейной оболочкой базиса self
    #     :return: Базис ортогонального дополнения к линейному пространству, порожденному базисом subspace_basis
    #     """
    #     pass

