from manim import *
from utils_2D import *


class Test_Scene(Scene):
    def construct(self):
        A = Dot(np.array([0, 2, 0]), radius=0.05)
        B = Dot(np.array([2, 0, 0]), radius=0.05)
        C = Dot(np.array([-1, -1, 0]), radius=0.05)
        A_tex = Text("A", font_size=14).next_to(A, UP)
        B_tex = Text("B", font_size=14).next_to(B, UP)
        C_tex = Text("C", font_size=14).next_to(C, UP)

        self.add(A_tex, B_tex, C_tex, A, B, C)
        self.add(Line(A, B), Line(A, C), Line(B, C))
        triangle = TriangleE2(A.get_center(), B.get_center(), C.get_center())
        self.play(FadeIn(Dot(triangle.incenter, radius=0.05)))
        self.play(FadeIn(Circle(radius=triangle.inscribed_radius).move_to(triangle.incenter)))

