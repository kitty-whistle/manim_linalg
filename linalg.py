from __future__ import annotations

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
    def __init__(self, coordinates: ndarray, basis: Basis | None = None):
        """
        Конструктор класса векторов n-мерного линейного пространства
        :param coordinates: координаты вектора
        :param basis: базис линейного пространства, в котором заданы координаты. По умолчанию - стандартный базис: (eᵢ)ⱼ = δᵢⱼ, i,j=1,...,n

        Если вектор записан в стандартном базисе, то basis = None
        """
        self.coordinates = coordinates
        self.dimension = len(self.coordinates)  # немного топорно, но у стандартного базиса не задать размерность, потому что нет соответствующего объекта
        self.basis = basis  # Если None, то вектора записаны в стандартном базисе

    def __add__(self, another: Self) -> Self:
        if self.basis != another.basis:
            raise BasisMismatchError
        return Vector(self.coordinates + another.coordinates)

    def __sub__(self, other: Self) -> Self:
        if self.basis != other.basis:
            raise BasisMismatchError
        return Vector(self.coordinates - other.coordinates)

    def __neg__(self) -> Self:
        return Vector(-self.coordinates)

    def __mul__(self, another: Self | float) -> float | Self:
        if self.basis != another.basis:
            raise BasisMismatchError
        return Vector(self.coordinates * another)

    def change_basis(self, basis: Basis) -> Vector:
        if self.basis.dimension != self.dimension:
            raise DimensionMismatchError
        coordinates = (basis.transition_from_standard_reversed @ self.coordinates.transpose()).transpose()
        return Vector(coordinates, basis)

    def __str__(self) -> str:
        pass


class Basis(Basis_ABC):
    def __init__(self, vectors: list[Vector]):
        for vector in vectors:
            if vector.basis is not None:
                raise NonCanonicalBasisError

            elif len(vector.coordinates) != len(vectors):
                raise DimensionMismatchError

        if len(vectors) != len(vectors[0].coordinates):
            raise DimensionMismatchError

        if np.linalg.det(np.array([vector.coordinates for vector in vectors])) == 0:
            raise LinearDependencyError

        self.vectors = vectors
        self.dimension = len(vectors)
        self.transition_from_standard = np.array([vector.coordinates for vector in vectors]).transpose()
        self.transition_from_standard_reversed = np.linalg.inv(self.transition_from_standard)

    def decompose(self, vector: Vector) -> ndarray:
        if vector.dimension != self.dimension:
            raise DimensionMismatchError

        if vector.basis is None:
            return (self.transition_from_standard_reversed @ vector.coordinates).transpose()

        transition_matrix = self.get_transition_matrix(another_basis=vector.basis)
        return (transition_matrix @ vector.coordinates).transpose()

    def get_transition_matrix(self, another_basis: Basis) -> ndarray:
        if another_basis.dimension != self.dimension:
            raise DimensionMismatchError

        return another_basis.transition_from_standard_reversed @ self.transition_from_standard

    def __str__(self) -> str:
        pass


class Linear_Mapping(Linear_Mapping_ABC):
    def __init__(self, matrix: ndarray, basis_V: Basis | None = None, basis_W: Basis | None = None):
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
        pass


class Linear_Operator(Linear_Operator_ABC):
    def __init__(self, matrix: ndarray, basis: Basis | None = None):
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

    def __str__(self) -> str:
        pass


class Bilinear_Function(Bilinear_Function_ABC):
    def __init__(self, matrix: ndarray, basis: Basis | None = None):
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
        pass


class VectorE(VectorE_ABC, Vector):

    def __init__(self, coordinates: ndarray, basis: BasisE | None = None):
        super().__init__(coordinates, basis)
        self.basis = basis

    def __mul__(self, another: float | Self) -> Self | float:
        if isinstance(another, float):
            return super().__mul__(another)

        elif isinstance(another, VectorE):
            if self.basis != another.basis:
                raise BasisMismatchError

            if self.basis is None:
                # просто покомпонентное умножение, матрица грамма единичная
                return self.coordinates @ another.coordinates.transpose()
            else:
                return self.coordinates @ self.basis.gram_matrix @ another.coordinates.transpose()
        else:
            raise UnsupportedOperation

    def __abs__(self) -> Self:
        pass

    def angle(self, another: Self) -> float:
        pass

    def normalize(self) -> Self:
        pass

    def __str__(self) -> str:
        pass


class BasisE(BasisE_ABC, Basis):
    def __init__(self, vectors: list[VectorE]):
        super().__init__(vectors)

        # В стандартном базисе матрица скалярного произведения единичная -> в self ↓
        self.gram_matrix = self.transition_from_standard.transpose() @ self.transition_from_standard

    def normalize(self) -> Self:
        pass

    def get_orthogonal_complement_basis(self) -> Self:
        pass

