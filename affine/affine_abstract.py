from __future__ import annotations
from linalg.linalg import *


class Point_ABC(ABC):
    """
    Класс точек n-мерного аффинного пространства
    """

    @abstractmethod
    def __eq__(self, other: Point_ABC) -> bool:
        """
        Операция проверки на равенство двух точек аффинного пространства
        """
        pass

    @abstractmethod
    def __add__(self, other: Vector_ABC) -> Point_ABC:
        """
        Операция сложения точки self c вектором other
        """
        pass

    @abstractmethod
    def __sub__(self, other: Vector_ABC) -> Point_ABC:
        """
        Операция сложения точки self с вектором, противоположным вектору other
        """
        pass

    @abstractmethod
    def vec_to(self, other: Point_ABC) -> Vector_ABC:
        """
        Операция восстановления вектора, соединяющего точки self и other
        """
        pass


class Affine_Frame_ABC(ABC):
    """
    Класс реперов n-мерного аффинного пространства
    """

    @abstractmethod
    def __eq__(self, other: Affine_Frame_ABC) -> bool:
        pass


class Affine_Mapping_ABC(ABC):
    """
    Класс аффинных отображений f: S -> S'
    """

    @abstractmethod
    def change_frame(self, new_frame: Affine_Frame_ABC) -> Affine_Mapping_ABC:
        """
        Смена репера аффинных пространств, в которых заданы аффинные пространства
        """
        pass

    @abstractmethod
    def apply(self, point: Point_ABC) -> Point_ABC:
        """
        Применение аффинного отображения к точке
        """
        pass


# class Coordination_Map(ABC):
#     """
#     Класс, отвечающий за переход от n-мерных координат подпространства U (dim U = k < n) n-мерного линейного пространства V в изоморфное линейное пространство R^k
#     """
#
#     @abstractmethod
#     def to_V(self, vector: Vector) -> Vector:
#         """
#         Метод, переводящий вектор размерности n, лежащий в k-мерном подпространстве в вектор размерности k
#         """
#         pass
#
#     @abstractmethod
#     def to_U(self, vector: Vector) -> Vector:
#         """
#         Метод, переводящий вектор размерности k в вектор размерности n, лежащий в подпространстве
#         """
#         pass

