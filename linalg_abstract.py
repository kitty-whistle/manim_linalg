from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self

from numpy import ndarray


class Vector_ABC(ABC):
    """
    Класс векторов n-мерного линейного пространства V
    """

    @abstractmethod
    def __eq__(self, other: Self) -> bool:
        pass

    @abstractmethod
    def __neg__(self) -> Self:
        """
        Операция поиска противоположного вектора
        :return: Противоположный вектор
        """

    @abstractmethod
    def __add__(self, other: Self) -> Self:
        """
        Операция сложения векторов, необходимая для определения векторного пространства
        :param other: Вектор-слагаемое
        :return: Некоторый вектор
        """
        pass

    @abstractmethod
    def __sub__(self, other: Self) -> Self:
        pass

    @abstractmethod
    def __mul__(self, other: float) -> Self:
        """
        Операция умножения на число
        :param other: число
        :return: Вектор
        """
        pass

    @abstractmethod
    def change_basis(self, other_basis: Self) -> Self:
        """
        Смена базиса, в котором задан вектор self, на another_basis
        :param other_basis: Новый базис линейного пространства V, в котором необходимо задать вектор self
        :return: self в новом базисе
        """
        pass


class Basis_ABC(ABC):
    """
    Класс базисов n-мерного линейного пространства V
    """

    @classmethod
    @abstractmethod
    def standard_basis(cls, dimension: int) -> Self:
        """
        Создание стандартного базиса, который закрепляется по умолчанию
        :param dimension: размерность стандартного базиса
        :return: Базис (!без поля self.vectors!)
        """
        pass

    @abstractmethod
    def get_transition_matrix(self, another_basis: Self) -> ndarray:
        """
        Построение матрицы перехода от базиса self к базису another_basis (C: V->V)
        :param another_basis: новый базис
        :return: матрица перехода
        """
        pass

    @abstractmethod
    def __eq__(self, other: Self) -> bool:
        pass


class Linear_Mapping_ABC(ABC):
    """
    Класс линейных отображений φ: V -> W
    """

    @abstractmethod
    def change_basis(self, other_basis_V: Basis_ABC, another_basis_W: Basis_ABC) -> Self:
        """
        Смена базисов, в котором задано линейное отображение на another_basis_V, another_basis_W
        :param other_basis_V: Новый базиc линейного пространства V
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
    def change_basis(self, other_basis: Basis_ABC) -> Self:
        """
        Смена базиса, в котором задано линейное отображение на another_basis
        :param other_basis: Новый базис линейного пространства V
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
    def change_basis(self, other_basis: Basis_ABC) -> Self:
        """
        Смена базиса, в котором задана билинейная функция на another_basis
        :param other_basis: Новый базис линейного пространства V
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


class VectorE_ABC(Vector_ABC):
    """
    Класс векторов n-мерного линейного евклидового пространства E
    """

    @abstractmethod
    def __matmul__(self, other: Self) -> float:
        """
        Операция умножения (скалярно с другим вектором), необходимая для определения Евклидового векторного пространства
        :param other: Вектор
        :return: Число (скалярное произведение)
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
    def normalize(self) -> Self:
        """
        Операция нормировки вектора
        :return: Нормированный на единицу вектор
        """
        pass

    @abstractmethod
    def get_orthogonal_projection(self, subspace_indexes: list[int]) -> Self:
        """
        Поиск ортогональной проекции вектора self на подпространство, порожденное базисом subspace_basis
        :param subspace_indexes: Индексы векторов (в списке self.basis.vectors) (векторов-столбцов) базиса self.basis, порождающих подпространство subspace
        """
        pass

    @abstractmethod
    def get_orthogonal_component(self, subspace_indexes: list[int]) -> Self:
        """
        Поиск ортогональной составляющей вектора self к подпространству, порожденному базисом subspace_basis
        :param subspace_indexes: Номера векторов (в списке self.basis.vectors) (векторов-столбцов) базиса self.basis, порождающих подпространство subspace
        """
        pass


class BasisE_ABC(Basis_ABC):

    @abstractmethod
    def normalize(self) -> Self:
        """
        Построение ОНБ из self методом Грамма-Шмидта
        """
        pass

