from __future__ import annotations

import math
from typing import Dict

import numpy as np

from abstract.KV import Vector_KV
from abstract.utils_abstract import *
from manim import *
from sympy import Matrix
from abstract.KV import Linear_Operator_KV
from manimlib.imports import *

class LineE3(Line_KV):

    def projection(self, point: ndarray) -> ndarray:

        # Плоскость на точке и прямой (на 2 неколлинеарных векторах)
        vec_1 = self.direction_vector
        vec_2 = Vector_KV(coordinates=point - self.start_point)

        if np.linalg.matrix_rank(np.array(vec_1.coordinates, vec_2.coordinates)) != 2:
            raise TypeError("Unsupported operand type (point is on the line)")

        plane = PlaneE3(normal_vector=vec_1.vec_mul(vec_2), plane_point=point)
        perpendicular_direction = self.line_by_angle(self.start_point, {plane: PI/2}, 1).direction_vector
        perpendicular_line = LineE3(start_point=point, end_point=point + perpendicular_direction.coordinates)
        return perpendicular_line.intersection(self)

    def __init__(self, start_point: ndarray, end_point: ndarray):
        self.start_point = start_point
        self.end_point = end_point

        self.direction_vector = Vector_KV(coordinates=end_point - start_point)

    @staticmethod
    def rotation_operator_by_angle(axe: Vector_KV, angle: float) -> Linear_Operator_KV:
        axe = axe.normalize()
        vector_mult_axe = np.array([
            [0, -axe.coordinates[2], axe.coordinates[1]],
            [axe.coordinates[2], 0, -axe.coordinates[0]],
            [-axe.coordinates[1], axe.coordinates[0], 0]])

        return Linear_Operator_KV(np.identity(3) + math.sin(angle) * vector_mult_axe + (1 - math.cos(angle) * (vector_mult_axe * vector_mult_axe)))
        # Формула Родрига

    def intersection(self, other: Self | Plane_KV) -> ndarray:
        if isinstance(other, LineE3):
            extended_system_matrix = np.array([
                [1, 0, 0, -self.direction_vector.coordinates[0], self.start_point[0]],
                [0, 1, 0, -self.direction_vector.coordinates[1], self.start_point[1]],
                [0, 0, 1, -self.direction_vector.coordinates[2], self.start_point[2]],
                [1, 0, 0, -other.direction_vector.coordinates[0], self.end_point[0]],
                [0, 1, 0, -other.direction_vector.coordinates[1], self.end_point[1]],
                [0, 0, 1, -other.direction_vector.coordinates[2], self.end_point[2]],
            ])

            if np.linalg.matrix_rank(extended_system_matrix) > 4:
                raise ZeroDivisionError("Lines are interbreeding")

            elif np.linalg.matrix_rank(extended_system_matrix) < 4:
                raise ZeroDivisionError("Lines are parallel")

            ex_sys_matrix_rref = np.array(Matrix(extended_system_matrix).rref().tolist, dtype=float)[0:4]

            x_matrix = np.array([
                [ex_sys_matrix_rref[0][-1], ex_sys_matrix_rref[0][1:4]],
                [ex_sys_matrix_rref[1][-1], ex_sys_matrix_rref[1][1:4]],
                [ex_sys_matrix_rref[2][-1], ex_sys_matrix_rref[2][1:4]],
                [ex_sys_matrix_rref[3][-1], ex_sys_matrix_rref[3][1:4]],
            ])

            y_matrix = np.array([
                [ex_sys_matrix_rref[0][0], ex_sys_matrix_rref[0][-1], ex_sys_matrix_rref[0][2:4]],
                [ex_sys_matrix_rref[1][0], ex_sys_matrix_rref[1][-1], ex_sys_matrix_rref[1][2:4]],
                [ex_sys_matrix_rref[2][0], ex_sys_matrix_rref[2][-1], ex_sys_matrix_rref[2][2:4]],
                [ex_sys_matrix_rref[3][0], ex_sys_matrix_rref[3][-1], ex_sys_matrix_rref[3][2:4]],
            ])

            z_matrix = np.array([
                [ex_sys_matrix_rref[0][0:2], ex_sys_matrix_rref[0][-1], ex_sys_matrix_rref[0][3]],
                [ex_sys_matrix_rref[1][0:2], ex_sys_matrix_rref[1][-1], ex_sys_matrix_rref[1][3]],
                [ex_sys_matrix_rref[2][0:2], ex_sys_matrix_rref[2][-1], ex_sys_matrix_rref[2][3]],
                [ex_sys_matrix_rref[3][0:2], ex_sys_matrix_rref[3][-1], ex_sys_matrix_rref[3][3]],
            ])

            system_matrix = np.array([ex_sys_matrix_rref[0][0:4],
                                      ex_sys_matrix_rref[1][0:4],
                                      ex_sys_matrix_rref[2][0:4],
                                      ex_sys_matrix_rref[3][0:4]])

            return np.array([np.linalg.det(x_matrix) / np.linalg.det(system_matrix),
                             np.linalg.det(y_matrix) / np.linalg.det(system_matrix),
                             np.linalg.det(z_matrix) / np.linalg.det(system_matrix)])

        elif isinstance(other, PlaneE3):
            x_matrix = np.array([
                [other.free_member, other.normal_vector.coordinates[1], other.normal_vector.coordinates[2], 0],
                [self.start_point[0], 0, 0, -self.direction_vector.coordinates[0]],
                [self.start_point[1], 1, 0, -self.direction_vector.coordinates[1]],
                [self.start_point[2], 0, 1, -self.direction_vector.coordinates[2]],
            ])

            y_matrix = np.array([
                [other.normal_vector.coordinates[0], other.free_member, other.normal_vector.coordinates[2], 0],
                [1, self.start_point[0], 0, -self.direction_vector.coordinates[0]],
                [0, self.start_point[1], 0, -self.direction_vector.coordinates[1]],
                [0, self.start_point[2], 1, -self.direction_vector.coordinates[2]],
            ])

            z_matrix = np.array([
                [other.normal_vector.coordinates[0], other.normal_vector.coordinates[1], other.free_member, 0],
                [1, 0, self.start_point[0], -self.direction_vector.coordinates[0]],
                [0, 1, self.start_point[1], -self.direction_vector.coordinates[1]],
                [0, 0, self.start_point[2], -self.direction_vector.coordinates[2]],
            ])

            system_matrix = np.array([
                [other.normal_vector.coordinates[0], other.normal_vector.coordinates[1], other.normal_vector.coordinates[2], 0],
                [1, 0, 0, -self.direction_vector.coordinates[0]],
                [0, 1, 0, -self.direction_vector.coordinates[1]],
                [0, 0, 1, -self.direction_vector.coordinates[2]],
            ])

            if np.linalg.det(system_matrix) == 0:
                raise ZeroDivisionError("Determinant is zero (the line is parallel to the plane)")

            return np.array([np.linalg.det(x_matrix) / np.linalg.det(system_matrix),
                             np.linalg.det(y_matrix) / np.linalg.det(system_matrix),
                             np.linalg.det(z_matrix) / np.linalg.det(system_matrix)])

        else:
            raise TypeError

    def line_by_angle(self, start_point: ndarray, rotations: Dict[PlaneE3, float], length: float) -> Self:
        new_direction_vector = self.direction_vector
        for plane, angle in rotations.items():
            new_direction_vector = self.rotation_operator_by_angle(plane.normal_vector, angle).apply(new_direction_vector)
        new_direction_vector = new_direction_vector.normalize()

        return Line(start_point, start_point + (new_direction_vector * length).coordinates)

    def angle(self, other: Self | Plane_KV) -> float:
        if isinstance(other, LineE3):
            return self.direction_vector.angle(other.direction_vector)
        elif isinstance(other, PlaneE3):
            intersection = self.intersection(other)
            perpendicular = LineE3(start_point=self.start_point, end_point=self.start_point + other.normal_vector.coordinates)  # Ортогональная составляющая
            projection = perpendicular.intersection(other)
            return perpendicular.angle(LineE3(start_point=projection, end_point=intersection)) # Ортогональная проекция
        else:
            raise TypeError

    def get_Line(self, **kwargs) -> Line | Line3D:
        return Line3D(start=self.start_point, end=self.end_point, **kwargs)

    def scale(self, scalar: float) -> Self:
        return LineE3(self.start_point - (self.direction_vector * scalar).coordinates, self.end_point + (self.direction_vector * scalar).coordinates)

    def __neg__(self) -> Self:
        return LineE3(self.end_point, self.start_point)

    def __abs__(self) -> Self:
        return abs(self.direction_vector)


class PlaneE3(Plane_KV):
    def __init__(self, normal_vector: Vector_KV, plane_point: ndarray):
        self.normal_vector = normal_vector.normalize()
        self.plane_point = plane_point

        self.free_member = - self.normal_vector.coordinates[0] * self.plane_point[0] - self.normal_vector.coordinates[
            1] * self.plane_point[1] - self.normal_vector.coordinates[2] * self.plane_point[2]

    def intersection(self, other: Self | Line_KV) -> LineE3 | ndarray:
        if isinstance(other, LineE3):
            return other.intersection(self)

        elif isinstance(other, PlaneE3):
            # 1-мерное пространство решений
            x_matrix_1 = np.array([
                [-self.free_member - self.normal_vector.coordinates[2], self.normal_vector.coordinates[1]],
                [-other.free_member - other.normal_vector.coordinates[2], other.normal_vector.coordinates[1]]
            ])

            y_matrix_1 = np.array([
                [self.normal_vector.coordinates[0], -self.free_member - self.normal_vector.coordinates[2]],
                [other.normal_vector.coordinates[0], -other.free_member - other.normal_vector.coordinates[2]],
            ])

            system_matrix = np.array([
                [self.normal_vector.coordinates[0], self.normal_vector.coordinates[1]],
                [other.normal_vector.coordinates[0], self.normal_vector.coordinates[1]],
            ])

            if np.linalg.det(system_matrix) == 0:
                raise ZeroDivisionError("Determinant is zero (Planes are parallel)")

            x_matrix_2 = np.array([
                [-self.free_member - self.normal_vector.coordinates[2], self.normal_vector.coordinates[1]],
                [-other.free_member - other.normal_vector.coordinates[2], other.normal_vector.coordinates[1]]
            ])

            y_matrix_2 = np.array([
                [self.normal_vector.coordinates[0], -self.free_member - 2 * self.normal_vector.coordinates[2]],
                [other.normal_vector.coordinates[0], -other.free_member - 2 * other.normal_vector.coordinates[2]],
            ])

            start_point = np.array([np.linalg.det(x_matrix_1) / np.linalg.det(system_matrix), np.linalg.det(y_matrix_1) / np.linalg.det(system_matrix), 1])
            end_point = np.array([np.linalg.det(x_matrix_2) / np.linalg.det(system_matrix), np.linalg.det(y_matrix_2) / np.linalg.det(system_matrix), 2])

            return LineE3(start_point=start_point, end_point=end_point)

        raise TypeError

    def plane_by_angle(self, angle: float) -> Self:
        pass

    def angle(self, other: Self | Line_KV) -> float:
        if isinstance(other, LineE3):
            return other.angle(self)
        elif isinstance(other, PlaneE3):
            return self.normal_vector.angle(other.normal_vector)

        raise TypeError

    def projection(self, other: LineE3 | ndarray) -> LineE3 | ndarray:
        if isinstance(other, LineE3):
            end_point = other.intersection(self)
            perpendicular_line = LineE3(start_point=other.start_point, end_point=self.normal_vector.coordinates + other.start_point)
            return LineE3(start_point=perpendicular_line.intersection(self), end_point=end_point)

        elif isinstance(other, ndarray):
            perpendicular_line = LineE3(start_point=other, end_point=self.normal_vector.coordinates + other)
            return perpendicular_line.intersection(self)

        raise TypeError

    def get_Plane(self, **kwargs) -> ParametricSurface:
        func = lambda x, y: np.array([x, y, (-self.normal_vector.coordinates[0] * x - self.normal_vector.coordinates[1] * y - self.free_member) / self.normal_vector[2]])
        return ParametricSurface(func, **kwargs)


if __name__ == "__main__":
    matrix = np.array([
        [1, 2, 5, 6, 8, 1],
        [2, 4, 2, 6, 7, 1],
        [2, 4, 10, 12, 16, 2],
        [-3, 4, 6, 8, 1, 12]
    ])
    s_matrix = Matrix(matrix)
    print(s_matrix.rref().array)