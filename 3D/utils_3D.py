from __future__ import annotations

import math
from typing import Dict

from abstract.KV import Vector_KV
from abstract.utils_abstract import *
from manim import *
from sympy import Matrix
from abstract.KV import Linear_Operator_KV


class LineE3(Line_KV):
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
            extended_system_matrix = np.array([])

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

    def line_by_angle(self, start_point: ndarray, rotations: Dict[Vector_KV: float], length: float) -> Self:
        new_direction_vector = self.direction_vector
        for axe, angle in rotations.items():
            new_direction_vector = self.rotation_operator_by_angle(axe, angle).apply(new_direction_vector)
        new_direction_vector = new_direction_vector.normalize()

        return Line(start_point, start_point + (new_direction_vector * length).coordinates)

    def angle(self, other: Self | Plane_KV) -> float:
        if isinstance(other, LineE3):
            pass
        elif isinstance(other, PlaneE3):
            pass
        else:
            raise TypeError

    def projection(self, point: ndarray) -> ndarray:
        pass

    def get_Line(self, **kwargs) -> Line | Line3D:
        pass

    def scale(self, scalar: float) -> Self:
        pass

    def __neg__(self) -> Self:
        pass

    def __abs__(self) -> Self:
        pass


class PlaneE3(Plane_KV):
    def __init__(self, normal_vector: Vector_KV, plane_point: ndarray):
        self.normal_vector = normal_vector.normalize()
        self.plane_point = plane_point

        self.free_member = - self.normal_vector.coordinates[0] * self.plane_point[0] - self.normal_vector.coordinates[
            1] * self.plane_point[1] - self.normal_vector.coordinates[2] * self.plane_point[2]

    def intersection(self, other: Self | Line_KV) -> ndarray:
        pass

    def plane_by_angle(self, **kwargs) -> Self:
        pass

    def angle(self, other: Self | Line_KV) -> float:
        pass

    def projection(self, other: Line_KV | ndarray) -> Line_KV | ndarray:
        pass

    def get_Plane(self, **kwargs) -> Surface:
        pass


if __name__ == "__main__":
    matrix = np.array([
        [1, 2, 5, 6, 8, 1],
        [2, 4, 2, 6, 7, 1],
        [2, 4, 10, 12, 16, 2],
        [-3, 4, 6, 8, 1, 12]
    ])
    s_matrix = Matrix(matrix)
    print(s_matrix.rref().array)