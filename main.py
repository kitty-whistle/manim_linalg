from manim import *
from utils_2D import *
from random import randint


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(3)
        for i in range(5):
            A, B, C = np.array([randint(-5, 5), randint(-5, 5), 0]), np.array([randint(-5, 5), randint(-5, 5), 0]), np.array([randint(-5, 5), randint(-5, 5), 0])
            A_dot, B_dot, C_dot = Dot().move_to(A), Dot().move_to(B), Dot().move_to(C)
            A_tex, B_tex, C_tex = Tex("A").next_to(A, DOWN), Tex("B").next_to(B, DOWN), Tex("C").next_to(C, DOWN)

            triangle = TriangleE2(A, B, C)
            AB, BC, AC = triangle.AB, triangle.BC, triangle.AC
            mAB, mBC, mAC = (-triangle.AB).scale(3), (-triangle.BC).scale(3), (-triangle.AC).scale(3)

            self.play(DrawBorderThenFill(A_dot), DrawBorderThenFill(B_dot), DrawBorderThenFill(C_dot), Write(A_tex), Write(B_tex), Write(C_tex), Create(AB.scale(3).get_Line()), Create(BC.scale(3).get_Line()), Create(AC.scale(3).get_Line()), Create(mAB.get_Line()), Create(mBC.get_Line()), Create(mAC.get_Line()))
            self.play(DrawBorderThenFill(Dot().move_to(triangle.unsigned_circle_center(A))), Create(Circle(radius=triangle.unsigned_circle_radius(A)).move_to(triangle.unsigned_circle_center(A))))
            self.play(DrawBorderThenFill(Dot().move_to(triangle.unsigned_circle_center(B))), Create(Circle(radius=triangle.unsigned_circle_radius(B)).move_to(triangle.unsigned_circle_center(B))))
            self.play(DrawBorderThenFill(Dot().move_to(triangle.unsigned_circle_center(C))), Create(Circle(radius=triangle.unsigned_circle_radius(C)).move_to(triangle.unsigned_circle_center(C))))
            self.wait(3)
            self.play(FadeOut(*self.mobjects))
