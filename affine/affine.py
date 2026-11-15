from __future__ import annotations
from affine_abstract import *

# Имеет ли смысл изначально отождествить начальную точку с радиусом-вектором
# Как задать стандартный репер?


class Point(Point_ABC):
    affine_frame: AffineFrame

    def __init__(self, coordinates: ndarray, affine_frame: AffineFrame):
        if len(coordinates) != affine_frame.basis.dimension:
            raise ValueError("Координаты вектора должны совпадать с размерностью репера")

        self.coordinates = coordinates
        self.affine_frame = affine_frame

    def __eq__(self, other: Self) -> bool:
        return np.array_equal(self.coordinates, other.coordinates) and self.affine_frame == other.affine_frame

    def __add__(self, other: Vector) -> Self:
        if self.affine_frame.basis != other.basis:
            raise ValueError("Базис векторного пространства, ассоциированного с аффинным пространством должен совпадать базисом, в котором задан вектор")

        return type(self)(coordinates=self.coordinates + other.coordinates, affine_frame=self.affine_frame)

    def __sub__(self, other: Vector) -> Self:
        return self + (-other)

    def vec_to(self, other: Self) -> Vector:
        if self.affine_frame != other.affine_frame:
            raise ValueError("Точки должны быть заданы в одном репере")

        return Vector(self.coordinates - other.coordinates, self.affine_frame.basis)


class PointE(Point, PointE_ABC):
    affine_frame: AffineFrameE

    def __init__(self, coordinates: ndarray, affine_frame: AffineFrameE):
        super().__init__(coordinates, affine_frame)

    def vec_to(self, other: Self) -> VectorE:
        if self.affine_frame != other.affine_frame:
            raise ValueError("Точки должны быть заданы в одном репере")

        return VectorE(self.coordinates - other.coordinates, self.affine_frame.basis)

    def dist(self, other: Self) -> float:
        return abs(self.vec_to(other))


class AffineFrame(AffineFrame_ABC):
    basis: Basis

    @classmethod
    def standard_affine_frame(cls, dimension: int) -> Self:
        standard_affine_frame = cls.__new__(cls)
        # как задать точку то без репера?

    def __init__(self, O_point: Point, basis: Basis):
        self.O_point = O_point
        self.basis = basis

    def __eq__(self, other: AffineFrame) -> bool:
        return self.O_point == other.O_point and self.basis == other.basis


class AffineFrameE(AffineFrame, AffineFrameE_ABC):
    basis: BasisE

    def __init__(self, O_point: Point, basis: BasisE):
        super().__init__(O_point, basis)
