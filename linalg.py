from __future__ import annotations
from linalg_abstract import *
import numpy as np


class Vector(Vector_ABC):
    """
    Класс векторов линейного пространства V размерности n над полем R
    """
    def __init__(self, coordinates: ndarray, basis: Basis | None = None):
        """
        Конструктор класса векторов n-мерного линейного пространства
        :param coordinates: координаты вектора
        :param basis: базис линейного пространства, в котором заданы координаты. По умолчанию - стандартный базис: (eᵢ)ⱼ = δᵢⱼ, i,j=1,...,n

        Если вектор записан в стандартном базисе, то basis = None
        """
        self.coordinates = coordinates
        self.basis = basis  # Если None - то вектора записаны в стандартном базисе

    def __add__(self, other: Self) -> Self:
        return Vector(self.coordinates + other.coordinates)

    def __sub__(self, other: Self) -> Self:
        return Vector(self.coordinates - other.coordinates)

    def __neg__(self) -> Self:
        return Vector(-self.coordinates)

    def __mul__(self, other: Self | float) -> float | Self:
        return Vector(self.coordinates * other)

    def change_basis(self, basis: Basis) -> Vector:
        coordinates = (basis.transition_from_standard_reversed @ self.coordinates.transpose()).transpose()
        return Vector(coordinates, basis)


class Basis(Basis_ABC):
    """
    Класс базисов линейного пространства V размерности n
    """
    def __init__(self, vectors: list[Vector]):
        """
        Конструктор класса базисов линейного пространства
        :param vectors: набор ЛНЗ векторов, заданных в стандартном базисе
        """

        for vector in vectors:
            if vector.basis is not None or len(vector.coordinates) != len(vectors):
                # У векторов одна размерность, стандартный базис и размерность вектора совпадает с их количеством, вектора не ЛНЗ
                raise NotImplementedError

        if len(vectors) != len(vectors[0].coordinates):
            raise NotImplementedError
        if np.linalg.det(np.array([vector.coordinates for vector in vectors])) == 0:
            raise NotImplementedError

        self.vectors = vectors
        self.transition_from_standard = np.array([vector.coordinates for vector in vectors]).transpose()
        self.transition_from_standard_reversed = np.linalg.inv(self.transition_from_standard)

    def decompose(self, vector: Vector) -> ndarray:
        """
        Разложение вектора vector по базису self
        :param vector:
        :return:
        """
        if vector.basis is None:
            return (self.transition_from_standard_reversed @ vector.coordinates).transpose()

        transition_matrix = self.get_transition_matrix(another_basis=vector.basis)
        return (transition_matrix @ vector.coordinates).transpose()

    def get_transition_matrix(self, another_basis: Basis) -> ndarray:
        """
        C: (a1...an) -> (b1...bn)
        C = Ca^-1 * Cb, где Ca, Cb - матрицы перехода из стандартного базиса в a и b
        :param another_basis:
        :return:
        """
        return another_basis.transition_from_standard_reversed @ self.transition_from_standard


class Linear_Mapping(Linear_Mapping_ABC):
    """
    Класс линейных отображений φ: V -> W размерностей n и m соответственно
    """
    def __init__(self, matrix: ndarray, basis_V: Basis | None = None, basis_W: Basis | None = None):
        self.matrix = matrix
        self.basis_V = basis_V
        self.basis_W = basis_W

    def change_basis(self, another_basis_V: Basis, another_basis_W: Basis) -> Linear_Mapping:
        new_matrix = another_basis_W.transition_from_standard_reversed @ self.matrix @ another_basis_V.transition_from_standard
        return Linear_Mapping(new_matrix, another_basis_V, another_basis_W)

    def apply(self, vector: Vector) -> Vector:
        if vector.basis == self.basis_V:
            coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
            return Vector(coordinates=coordinates, basis=self.basis_W)
        raise NotImplementedError


class Linear_Operator(Linear_Operator_ABC):
    """
    Класс линейных операторов φ: V -> V размерности n
    """
    def __init__(self, matrix: ndarray, basis: Basis | None = None):
        self.matrix = matrix
        self.basis = basis

    def change_basis(self, another_basis: Basis) -> Linear_Operator:
        new_matrix = another_basis.transition_from_standard_reversed @ self.matrix @ another_basis.transition_from_standard
        return Linear_Operator(new_matrix, another_basis)

    def apply(self, vector: Vector):
        if vector.basis == self.basis:
            coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
            return Vector(coordinates=coordinates, basis=self.basis)
        raise NotImplementedError


class Bilinear_Function(Bilinear_Function_ABC):
    """
    Класс билинейных функций β: V × V -> R
    """
    def __init__(self, matrix: ndarray, basis: Basis | None = None):
        self.matrix = matrix
        self.basis = basis

    def change_basis(self, another_basis: Basis) -> Bilinear_Function:
        new_matrix = another_basis.transition_from_standard.transpose() @ self.matrix @ another_basis.transition_from_standard
        return Bilinear_Function(new_matrix, another_basis)

    def apply(self, vector_1: Vector, vector_2: Vector) -> float:
        if vector_1.basis == self.basis and vector_2.basis == self.basis:
            return float(vector_1.coordinates.transpose() @ self.matrix @ vector_2.coordinates)
        raise NotImplementedError
