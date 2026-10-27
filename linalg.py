from __future__ import annotations

import math
from io import UnsupportedOperation

from linalg_abstract import *
import numpy as np


class UnsupportedType(UnsupportedOperation):
    """Несоответсвие типов"""


class BasisMismatchError(ValueError):
    """Объекты заданы в разных базисах"""
    pass


class DimensionMismatchError(ValueError):
    """Объекты разных размерностей"""
    pass


class NonCanonicalBasisError(ValueError):
    """Базис вектора не является стандартным"""
    pass


class LinearDependencyError(ValueError):
    """Вектора линейно зависимы"""
    pass


class Vector(Vector_ABC):
    def __init__(self, coordinates: ndarray, basis: Basis):
        """
        Конструктор класса векторов n-мерного линейного пространства
        :param coordinates: координаты вектора
        :param basis: базис линейного пространства, в котором заданы координаты.

        Если вектор записан в стандартном базисе, то basis = Basis.get_standard_basis(dimension)
        Но нужно иметь в виду, что у объекта Basis.get_standard_basis(dimension) поле self.vectors = None
        """
        if len(coordinates) != basis.dimension:
            raise DimensionMismatchError
        self.coordinates = coordinates
        self.dimension = len(self.coordinates)  # кол-во координат
        self.basis = basis

    def __eq__(self, another: Vector):
        return list(self.coordinates) == list(another.coordinates) and self.basis == another.basis

    def __add__(self, another: Self) -> Self:
        if self.basis != another.basis:
            raise BasisMismatchError
        return Vector(coordinates=self.coordinates + another.coordinates, basis=self.basis)

    def __sub__(self, other: Self) -> Self:
        if self.basis != other.basis:
            raise BasisMismatchError
        return Vector(coordinates=self.coordinates - other.coordinates, basis=self.basis)

    def __neg__(self) -> Self:
        return Vector(coordinates=-self.coordinates, basis=self.basis)

    def __mul__(self, another: float) -> float | Self:
        return Vector(coordinates=self.coordinates * another, basis=self.basis)

    def __rmul__(self, another: float) -> float | Self:
        return self.__mul__(another)

    def change_basis(self, basis: Basis) -> Vector:
        if self.basis.dimension != self.dimension:
            raise DimensionMismatchError
        coordinates = (basis.transition_from_standard_reversed @ self.coordinates.transpose()).transpose()
        return Vector(coordinates=coordinates, basis=basis)

    def __str__(self) -> str:
        return f"Vector(coordinates={self.coordinates}, basis={self.basis})"


class Basis(Basis_ABC):

    @classmethod
    def get_standard_basis(cls, dimension: int) -> Basis:
        standard_basis = cls.__new__(cls)

        standard_basis.vectors = None
        standard_basis.dimension = dimension
        standard_basis.transition_from_standard = np.identity(dimension)
        standard_basis.transition_from_standard_reversed = np.identity(dimension)
        standard_basis.is_standard_basis = True

        return standard_basis

    @staticmethod
    def get_system_rank(vectors: list[Vector]) -> int:
        dimension = vectors[0].dimension
        for vector in vectors:
            if vector.dimension != dimension:
                raise DimensionMismatchError

        return np.linalg.matrix_rank(np.array([vector.coordinates for vector in vectors]))

    def __init__(self, vectors: list[Vector]):
        for vector in vectors:
            if vector.basis != self.get_standard_basis(dimension=vector.dimension):
                raise NonCanonicalBasisError
        # Начать думать отсюда
        if len(vectors) != len(vectors[0].coordinates):
            raise DimensionMismatchError

        if np.linalg.det(np.array([vector.coordinates for vector in vectors])) == 0:
            raise LinearDependencyError

        self.vectors = vectors
        self.dimension = len(vectors)
        self.transition_from_standard = np.array([vector.coordinates for vector in vectors]).transpose()
        self.transition_from_standard_reversed = np.linalg.inv(self.transition_from_standard)
        self.is_standard_basis = False

    def __eq__(self, another: Basis) -> bool:
        if self.is_standard_basis == another.is_standard_basis:
            return self.dimension == another.dimension

        return self.vectors == another.vectors

    def decompose(self, vector: Vector) -> ndarray:
        if vector.dimension != self.dimension:
            raise DimensionMismatchError

        transition_matrix = self.get_transition_matrix(another_basis=vector.basis)
        return (transition_matrix @ vector.coordinates).transpose()

    def get_transition_matrix(self, another_basis: Basis) -> ndarray:
        if another_basis.dimension != self.dimension:
            raise DimensionMismatchError

        return another_basis.transition_from_standard_reversed @ self.transition_from_standard

    def __str__(self) -> str:
        return f"Basis(vectors={self.vectors}, is_standard_basis={self.is_standard_basis})"


class Linear_Mapping(Linear_Mapping_ABC):
    def __init__(self, matrix: ndarray, basis_V: Basis, basis_W: Basis):
        if matrix.shape[0] != basis_W.dimension or matrix.shape[1] != basis_V.dimension:
            raise DimensionMismatchError

        self.matrix = matrix
        self.basis_V = basis_V
        self.basis_W = basis_W

    def change_basis(self, another_basis_V: Basis, another_basis_W: Basis) -> Linear_Mapping:
        if self.basis_V.dimension != another_basis_V.dimension or self.basis_W.dimension != another_basis_W.dimension:
            raise DimensionMismatchError

        new_matrix = another_basis_W.transition_from_standard_reversed @ self.matrix @ another_basis_V.transition_from_standard
        return Linear_Mapping(new_matrix, another_basis_V, another_basis_W)

    def apply(self, vector: Vector) -> Vector:
        if vector.basis != self.basis_V:
            raise BasisMismatchError

        coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
        return Vector(coordinates=coordinates, basis=self.basis_W)

    def __str__(self) -> str:
        return f"Linear_Mapping(matrix={self.matrix}, basis_V={self.basis_V}, basis_W={self.basis_W})"


class Linear_Operator(Linear_Operator_ABC):

    def __init__(self, matrix: ndarray, basis: Basis):
        if basis.dimension != matrix.shape[0] or matrix.shape[0] != matrix.shape[1]:
            raise DimensionMismatchError

        self.matrix = matrix
        self.basis = basis

    def change_basis(self, another_basis: Basis) -> Linear_Operator:
        if another_basis.dimension != self.basis.dimension:
            raise DimensionMismatchError
        new_matrix = another_basis.transition_from_standard_reversed @ self.matrix @ another_basis.transition_from_standard
        return Linear_Operator(new_matrix, another_basis)

    def apply(self, vector: Vector):
        if vector.basis != self.basis:
            raise BasisMismatchError

        coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
        return Vector(coordinates=coordinates, basis=self.basis)

    def calculate_eigenvalues_and_eigenvectors(self) -> dict[VectorE, float]:
        eigenvalues, eigenvectors = np.linalg.eig(self.matrix)
        return {VectorE(coordinates=eigenvectors[i], basis=BasisE.get_standard_basis(len(eigenvectors[i]))): eigenvalues[i] for i in range(len(eigenvalues))}

    def diagonalize(self) -> Self:
        invariant_subspace = self.calculate_eigenvalues_and_eigenvectors()
        eigenvectors = list(invariant_subspace.keys())

        if self.basis.dimension == BasisE.get_system_rank(eigenvectors):
            # Это и есть базис из собственных векторов
            return self.change_basis(BasisE(vectors=eigenvectors))

        # Надо дополнять до базиса self.basis
        return None

    def __str__(self) -> str:
        return f"Linear_Operator(matrix={self.matrix}, basis={self.basis})"


class Bilinear_Function(Bilinear_Function_ABC):
    def __init__(self, matrix: ndarray, basis: Basis):
        if basis.dimension != matrix.shape[0] or matrix.shape[0] != matrix.shape[1]:
            raise DimensionMismatchError

        self.matrix = matrix
        self.basis = basis

    def change_basis(self, another_basis: Basis) -> Bilinear_Function:
        if self.basis.dimension != another_basis.dimension:
            raise DimensionMismatchError
        new_matrix = another_basis.transition_from_standard.transpose() @ self.matrix @ another_basis.transition_from_standard
        return Bilinear_Function(new_matrix, another_basis)

    def apply(self, vector_1: Vector, vector_2: Vector) -> float:
        if vector_1.basis != self.basis or vector_2.basis != self.basis:
            raise BasisMismatchError

        return float(vector_1.coordinates.transpose() @ self.matrix @ vector_2.coordinates)

    def __str__(self) -> str:
        return f"Bilinear_Function(matrix={self.matrix}, basis={self.basis})"


class VectorE(Vector, VectorE_ABC):
    def __init__(self, coordinates: ndarray, basis: BasisE):
        super().__init__(coordinates, basis)
        self.basis = basis

    def __add__(self, another: Self) -> Self:
        vector = super().__add__(another)
        return VectorE(coordinates=vector.coordinates, basis=self.basis)

    def __sub__(self, another: Self) -> Self:
        vector = super().__sub__(another)
        return VectorE(coordinates=vector.coordinates, basis=self.basis)

    def __neg__(self) -> Self:
        vector = super().__neg__()
        return VectorE(coordinates=vector.coordinates, basis=self.basis)

    def __mul__(self, another: float | Self) -> Self | float:
        if isinstance(another, float):
            vector = super().__mul__(another)
            return VectorE(vector.coordinates, self.basis)

        elif isinstance(another, VectorE):
            if self.basis != another.basis:
                raise BasisMismatchError

            return float(self.coordinates @ self.basis.gram_matrix @ another.coordinates.transpose())
        else:
            raise UnsupportedOperation

    def __abs__(self) -> float:
        return math.sqrt(self * self)

    def angle(self, other: Self) -> float:
        return math.acos((self * other) / (abs(self) * abs(other)))

    def normalize(self) -> Self:
        normalization = 0
        for i in self.coordinates:
            normalization += i**2
        normalization = normalization ** (1 / 2)

        coordinates = np.array([round(cord / normalization, 3) for cord in self.coordinates])
        return VectorE(coordinates=coordinates, basis=self.basis)

    def get_orthogonal_projection(self, subspace_basis: BasisE) -> Self:
        """
        Поиск ортогональной проекции вектора self на подпространство, порожденное базисом subspace_basis
        :param subspace_basis: Базис линейного подпространства пространства, порожденного self.basis
        Важным является то, что subspace_basis должен лежать в self.basis
        """

        # Будем искать ортогональную составляющую к подпространству, порожденному addition_basis
        addition_basis = BasisE(vectors=[vector for vector in self.basis.vectors if vector not in subspace_basis])
        return self.get_orthogonal_component(subspace_basis=addition_basis)

    def get_orthogonal_component(self, subspace_basis: BasisE) -> Self:
        """
        Поиск ортогональной составляющей вектора self к подпространству, порожденному базисом subspace_basis
        :param subspace_basis: Базис линейного подпространства пространства, порожденного self.basis
        Важным является то, что subspace_basis должен лежать в self.basis
        """
        if subspace_basis not in self.basis:
            raise BasisMismatchError

        # self.basis - базис линейного пространства (e1....en)
        # subspace_basis - базис линейного подпространства (e1...ek) k < n (БОО)
        # addition_basis - базис дополнения subspace_basis до self.basis (ek+1...en) (БОО)
        addition_basis = BasisE(vectors=[vector for vector in self.basis.vectors if vector not in subspace_basis])

        heterogeneity = np.array([self * vector for vector in addition_basis.vectors]).transpose()
        component_coordinates = (addition_basis.gram_matrix @ heterogeneity).transpose()  # координаты ортогональной проекции в базисе addition_basis

        # Важно, что этот вектор уже задан в базисе дополнения U до E^n
        return VectorE(coordinates=component_coordinates, basis=addition_basis)

    def __str__(self) -> str:
        return f"VectorE(coordinates={self.coordinates}, basis={self.basis})"


class BasisE(BasisE_ABC, Basis):
    def __init__(self, vectors: list[VectorE]):
        super().__init__(vectors)
        self.vectors = vectors

        # В стандартном базисе матрица скалярного произведения единичная -> в self ↓
        self.gram_matrix = self.transition_from_standard.transpose() @ self.transition_from_standard

    def normalize(self) -> Self:
        if self.is_standard_basis:
            raise BasisMismatchError

        other_basis = self.vectors

        for vector_i_index in range(len(self.vectors)):
            vector_i = self.vectors[vector_i_index]
            new_vector_i = vector_i
            for vector_j_index in range(len(self.vectors) - vector_i_index):
                vector_j = self.vectors[vector_j_index]

                # Нормировочный коэффициент ортогональности i-го вектора для j-ого участника линейной оболочки
                normalization_ij = - (vector_i * vector_j) / (vector_j * vector_j)

                new_vector_i = new_vector_i - vector_j * normalization_ij

            other_basis[vector_i_index] = new_vector_i

        # Теперь other_basis ортогонален и имеет ту же линейную оболочку, его надо нормировать
        other_basis = [other_vector.normalize() for other_vector in other_basis]

        return BasisE(vectors=other_basis)

    def __str__(self) -> str:
        return f"BasisE(vectors={self.vectors})"


if __name__ == "__main__":
    vector_a = Vector(coordinates=np.array([1, 2]), basis=Basis.get_standard_basis(dimension=3))
    vector_b = Vector(coordinates=np.array([2, 4]), basis=Basis.get_standard_basis(dimension=3))
    basis_ab = Basis(vectors=[vector_a, vector_b])
    print(basis_ab)