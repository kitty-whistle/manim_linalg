from __future__ import annotations

from collections import defaultdict

import numpy as np

from linalg_abstract import *


class Vector(Vector_ABC):
    """
    Класс векторов n-мерного линейного пространства V
    """

    basis: Basis

    def __init__(self, coordinates: ndarray, basis: Basis):
        """
        Конструктор класса векторов n-мерного линейного пространства V
        :param coordinates: координаты вектора в базисе basis
        :param basis: базис векторного пространства, в котором заданы координаты вектора
        """

        if len(coordinates) != basis.dimension:
            raise ValueError("Координаты вектора должны совпадать с размерностью базиса")

        self.coordinates = coordinates
        self.basis = basis

    def __eq__(self, other: Self) -> bool:
        # Равенство векторов <-> равенству координат в одном и том же базисе
        return np.array_equal(self.coordinates, other.coordinates) and self.basis == other.basis

    def __neg__(self) -> Self:
        return type(self)(-self.coordinates, self.basis)

    def __add__(self, other: Self) -> Self:
        if self.basis != other.basis:
            raise ValueError("Вектора можно складывать только тогда, когда их базисы одинаковы")

        return type(self)(self.coordinates + other.coordinates, self.basis)

    def __sub__(self, other: Vector) -> Self:
        return self + (-other)

    def __mul__(self, other: float) -> Self:
        return type(self)(self.coordinates * other, self.basis)

    def change_basis(self, other_basis: Basis) -> Self:
        transition_matrix = self.basis.get_transition_matrix(other_basis)  # transition_matrix: self.basis -> other_basis
        new_coordinates = (transition_matrix @ self.coordinates.transpose()).transpose()
        return type(self)(new_coordinates, other_basis)

    def __str__(self) -> str:
        return f"Vector(coordinates={self.coordinates}, basis={self.basis})"


class Basis(Basis_ABC):
    """
    Класс базисов n-мерных линейных пространств V
    """

    is_standard_basis: bool
    vectors: list[Vector] | None

    @classmethod
    def standard_basis(cls, dimension: int) -> Self:
        basis = cls.__new__(cls)
        basis.vectors = None  # У стандартного базиса нет векторов!
        basis.is_standard_basis = True
        basis.transition_from_standard = np.identity(dimension)
        basis.reversed_transition_from_standard = np.identity(dimension)
        basis.dimension = dimension

        return basis

    def __init__(self, vectors: list[Vector]):
        """
        Конструктор класса базисов n-мерного линейного пространства
        :param vectors: набор ЛНЗ векторов, на линейной оболочке которых строится линейное пространство.

        Допущение 1: размерность пространства, в котором заданы вектора, должна совпадать с количеством векторов.
        (т.е количество координат у каждого из векторов vectors должна быть равна количеству самих этих векторов)
        Это сделано для того, чтобы в рамках Vector и Basis работать только с квадратными матрицами.
        Для перехода от базисов подпространств к базисам пространств будут служить линейные отображения.
        """

        self.is_standard_basis = False
        self.vectors = vectors

        # Проверка на стандартный базис ↓
        for vector in vectors:
            if not vector.basis.is_standard_basis:
                raise ValueError("Вектора заданы не в стандартном базисе")

        # Матрица перехода из закрепленного стандартного базиса в базис self (квадратная) ↓
        self.transition_from_standard = np.array([vector.coordinates for vector in vectors]).transpose()

        # Проверка на Допущение 1
        if self.transition_from_standard.shape[0] != self.transition_from_standard.shape[1]:
            raise ValueError("Нарушено Допущение 1 (см. __init__)")

        # Проверка на линейную независимость векторов | Существование обратной матрицы перехода ↓
        if np.linalg.det(self.transition_from_standard) == 0:
            raise ValueError("Вектора линейно зависимы")
        self.reversed_transition_from_standard = np.linalg.inv(self.transition_from_standard)

        self.dimension = len(vectors)  # Размерность линейного пространства, построенного на линейной оболочке векторов

    def __eq__(self, other: Self) -> bool:
        # Для стандартных базисов равенство эквивалентно равенству размерностей линейных пространств, порожденных стандартным базисом
        if self.is_standard_basis and other.is_standard_basis:
            return self.dimension == other.dimension

        # Для нестандартных базисов равенство эквивалентно равенству соответствующих векторов (вектора там заданы в стандартном базисе)
        return self.vectors == other.vectors

    def get_transition_matrix(self, another_basis: Self) -> ndarray:
        # Конкатенация по столбцам: (n, k) и (n, m) → (n, k + m)
        # global_matrix = np.hstack([self.transition_from_standard, another_basis.transition_from_standard])

        #if np.linalg.matrix_rank(global_matrix) != another_basis.dimension != self.dimension:
        #    raise ValueError("Линейные оболочки векторов базиса self и another_basis отличаются")

        # Это эквивалентно равенству линейных оболочек при условии Допущение 1
        if self.dimension != another_basis.dimension:
            raise ValueError("Линейные оболочки векторов базиса self и another_basis отличаются")

        return self.reversed_transition_from_standard @ another_basis.transition_from_standard

    def __str__(self) -> str:
        if self.is_standard_basis:
            return f"Basis(dimension={self.dimension}, is_standard_basis={self.is_standard_basis})"

        return f"Basis(dimension={self.dimension}, vectors={[str(vector) for vector in self.vectors]}, is_standard_basis={self.is_standard_basis})"


class Linear_Mapping(Linear_Mapping_ABC):
    def __init__(self, matrix: ndarray, basis_V: Basis, basis_W: Basis):
        """
        Конструктор класса линейных отображений φ: V -> W
        :param matrix: Матрица, в i-ом столбце которой, записаны координаты образа i-го базисного вектора basis_V в базисе basis_W.
        :param basis_V: базис пространства, из которого отображаются вектора.
        :param basis_W: базис пространства, в которое отображаются вектора
        """
        if matrix.shape[0] != basis_W.dimension or matrix.shape[1] != basis_V.dimension:
            raise ValueError("Размерность матрицы не совпадает с размерностью пространства, построенного на базисах")

        self.matrix = matrix
        self.basis_V = basis_V
        self.basis_W = basis_W

    def change_basis(self, another_basis_V: Basis, another_basis_W: Basis) -> Self:
        transition_matrix_V = self.basis_V.get_transition_matrix(another_basis_V)
        transition_matrix_W = self.basis_W.get_transition_matrix(another_basis_W)

        new_matrix = transition_matrix_W @ self.matrix @ transition_matrix_V
        return Linear_Mapping(new_matrix, another_basis_V, another_basis_W)

    def apply(self, vector: Vector) -> Vector:
        if vector.basis != self.basis_V:
            raise ValueError("Вектор задан не в том же базисе, в котором задано линейное отображение")

        coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
        return type(vector)(coordinates=coordinates, basis=self.basis_W)

    def __str__(self) -> str:
        return f"Linear_Mapping(matrix={self.matrix}, basis_V={self.basis_V}, basis_W={self.basis_W})"


class Bilinear_Function(Bilinear_Function_ABC):

    def __init__(self, matrix: ndarray, basis: Basis):
        if basis.dimension != matrix.shape[0] or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Размерность матрицы билинейной функции не совпадает с размерностью пространства, порожденного базисными векторами")

        self.matrix = matrix
        self.basis = basis

    def change_basis(self, other_basis: Basis) -> Self:
        if self.basis.dimension != other_basis.dimension:
            raise ValueError("Базисы образуют линейные оболочки разной размерности")
        new_matrix = other_basis.transition_from_standard.transpose() @ self.matrix @ other_basis.transition_from_standard
        return type(self)(new_matrix, other_basis)

    def apply(self, vector_1: Vector, vector_2: Vector) -> float:
        if vector_1.basis != self.basis or vector_2.basis != self.basis:
            raise ValueError("Вектора и билинейная функция должны быть заданы в одном и том же базисе")

        return float(vector_1.coordinates.transpose() @ self.matrix @ vector_2.coordinates)

    def __str__(self) -> str:
        return f"Bilinear_Function(matrix={self.matrix}, basis={str(self.basis)})"


class Linear_Operator(Linear_Operator_ABC):

    def __init__(self, matrix: ndarray, basis: Basis):
        if basis.dimension != matrix.shape[0] or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Размерность матрицы линейного оператора не совпадает с размерностью пространства, порожденного базисными векторами")

        self.matrix = matrix
        self.basis = basis

    def change_basis(self, other_basis: Basis) -> Self:
        if other_basis.dimension != self.basis.dimension:
            raise ValueError("Базисы образуют линейные оболочки различных размерностей")
        new_matrix = other_basis.reversed_transition_from_standard @ self.matrix @ other_basis.transition_from_standard
        return type(self)(new_matrix, other_basis)

    def apply(self, vector: Vector) -> Vector:
        if vector.basis != self.basis:
            raise ValueError("Вектор и линейные оператор заданы в разных базисах")

        coordinates = (self.matrix @ vector.coordinates.transpose()).transpose()
        return type(vector)(coordinates=coordinates, basis=self.basis)

    @property
    def eigenvectors(self) -> dict[float, Vector]:
        is_euclid = isinstance(self.basis, BasisE)

        eigenvalues, eigenvectors = np.linalg.eig(self.matrix)

        groups = defaultdict(list)
        for i, lam in enumerate(eigenvalues):
            groups[lam].append(eigenvectors[:, i])
        return dict(groups)


    def diagonalize(self) -> Self:
        pass


class VectorE(Vector, VectorE_ABC):
    basis: BasisE

    def __init__(self, coordinates: ndarray, basis: BasisE):
        super().__init__(coordinates, basis)

    def __matmul__(self, other: Self) -> float:
        if self.basis != other.basis:
            raise ValueError("Вектора можно умножать скалярно только тогда, когда их базисы одинаковы")

        return float(self.coordinates @ self.basis.gram_matrix @ other.coordinates.transpose())

    def __abs__(self) -> float:
        return np.sqrt(self @ self)

    def angle(self, other: Self) -> float:
        if np.isclose(abs(other), 0) or np.isclose(abs(self), 0):
            return np.pi / 2

        cos_theta = (self @ other) / (abs(self) * abs(other))
        return float(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    def normalize(self) -> Self:
        norm = abs(self)
        if np.isclose(norm, 0):
            raise ValueError("Нельзя нормировать нулевой вектор")

        return type(self)(self.coordinates / norm, self.basis)

    def get_orthogonal_component(self, subspace_indexes: list[int]) -> Self:
        return self - self.get_orthogonal_projection(subspace_indexes)

    def get_orthogonal_projection(self, subspace_indexes: list[int]) -> Self:
        P_matrix = self.basis.transition_from_standard[:, subspace_indexes]  # Часть матрицы self.basis.transition_from_standard, включающая только вектора-столбцы дополнения U
        projection_coordinates = P_matrix @ np.linalg.inv(P_matrix.transpose() @ P_matrix) @ P_matrix.transpose() @ self.coordinates.transpose()

        return type(self)(coordinates=projection_coordinates, basis=self.basis)


class BasisE(Basis, BasisE_ABC):

    vectors: list[VectorE] | None

    @classmethod
    def standard_basis(cls, dimension: int) -> Self:
        basis = super().standard_basis(dimension)  # BasisE, поскольку -> Self
        basis.gram_matrix = np.identity(dimension)
        return basis

    def __init__(self, vectors: list[VectorE]):
        super().__init__(vectors)

        # В стандартном базисе матрица скалярного произведения единичная -> в self ↓
        self.gram_matrix = self.transition_from_standard.transpose() @ self.transition_from_standard
        self.reversed_gram_matrix = np.linalg.inv(self.gram_matrix)

    def normalize(self) -> Self:
        if self.is_standard_basis:
            return self

        other_vectors = self.vectors.copy()

        for vector_i_index in range(len(self.vectors)):
            vector_i = self.vectors[vector_i_index]
            new_vector_i = vector_i
            for vector_j_index in range(vector_i_index):
                vector_j = other_vectors[vector_j_index]

                # Нормировочный коэффициент ортогональности i-го вектора для j-ого участника линейной оболочки
                normalization_ij = - (new_vector_i @ vector_j) / (vector_j @ vector_j)

                new_vector_i = new_vector_i + vector_j * normalization_ij

            other_vectors[vector_i_index] = new_vector_i

        # Теперь other_basis ортогонален и имеет ту же линейную оболочку, его надо нормировать
        other_vectors = [other_vector.normalize() for other_vector in other_vectors]

        return type(self)(other_vectors)


if __name__ == "__main__":
    basis = BasisE.standard_basis(3)

    matrix = np.array([
        [2, 0, 0], [0, 2, 0], [0, 0, 5]
    ])

    operator = Linear_Operator(matrix, basis=basis)
    print(operator.eigenvectors)

