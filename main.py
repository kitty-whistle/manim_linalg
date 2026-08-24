from utils_2D import *

dot_kwargs = {"radius": 0.05, "fill_color": BLUE, "stroke_color": BLACK, "stroke_width": 2, "z_index": 1}
moving_dot_kwargs = {"radius": 0.05, "fill_color": YELLOW, "stroke_color": BLACK, "stroke_width": 2, "z_index": 1}
line_kwargs = {"stroke_color": GREY, "stroke_opacity": 1, "stroke_width": 4, "z_index": 0}
dash_kwargs = {"stroke_color": BLUE, "stroke_opacity": 1, "stroke_width": 2.5, "z_index": 1}
right_angle_kwargs = {"length": 0.2, "stroke_color": BLUE, "stroke_opacity": 0.8, "stroke_width": 2.5, "z_index": -1}
angle_kwargs = {"stroke_color": BLUE, "stroke_opacity": 0.8, "stroke_width": 2.5, "z_index": -1}
tex_kwargs = {"font_size": 25, "z_index": 1}
circle_kwargs = {"stroke_color": BLUE, "stroke_opacity": 1, "stroke_width": 2.5, "z_index": 0}


class BasicTriangle(MovingCameraScene):
    def construct(self):
        A, B, C = np.array([-4, -2, 0]), np.array([4, -3, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)
        triangleE2 = TriangleE2(A=A[0:2], B=B[0:2], C=C[0:2])

        self.play(DrawBorderThenFill(A_dot), DrawBorderThenFill(B_dot), DrawBorderThenFill(C_dot))
        self.play(Write(A_tex), Write(B_tex), Write(C_tex))
        self.play(Create(triangleE2.AB.get_Line(**line_kwargs)), Create(triangleE2.BC.get_Line(**line_kwargs)), Create(triangleE2.AC.get_Line(**line_kwargs)))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))


class Median(MovingCameraScene):
    def construct(self):
        A, B, C = np.array([-4, -2, 0]), np.array([4, -3, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)
        triangleE2 = TriangleE2(A=A[0:2], B=B[0:2], C=C[0:2])

        median_A = triangleE2.median(A[0:2])

        M_dot = Dot(**moving_dot_kwargs).move_to(B)
        M_tex = always_redraw(lambda: Tex("M", **tex_kwargs).next_to(M_dot, RIGHT))
        AM = always_redraw(lambda: LineE2(A[0:2], M_dot.get_center()[0:2]).get_Line(**line_kwargs))

        BM = LineE2(B[0:2], median_A.end_point)
        MC = LineE2(median_A.end_point, C[0:2])
        dash_1 = BM.line_by_angle(angle=math.pi / 2, start_point=BM.center, length_scale=0.2).get_Line(**dash_kwargs).move_to(BM.make_R3(BM.center))
        dash_2 = MC.line_by_angle(angle=math.pi / 2, start_point=MC.center, length_scale=0.2).get_Line(**dash_kwargs).move_to(MC.make_R3(MC.center))

        self.add(A_dot, B_dot, C_dot, A_tex, B_tex, C_tex, triangleE2.AB.get_Line(**line_kwargs), triangleE2.BC.get_Line(**line_kwargs), triangleE2.AC.get_Line(**line_kwargs), M_dot, AM)
        self.play(Write(M_tex))
        self.play(M_dot.animate.move_to(median_A.end_manim))
        self.play(Create(dash_1), Create(dash_2))
        self.wait(2)
        self.play(FadeOut(dash_1), FadeOut(dash_2))

        median_B = triangleE2.median(B[0:2])
        median_C = triangleE2.median(C[0:2])
        centroid = Dot(**dot_kwargs).move_to(LineE2.make_R3(triangleE2.centroid))

        self.play(FadeIn(median_B.get_Line(**line_kwargs)), FadeIn(centroid), FadeIn(median_C.get_Line(**line_kwargs)), FadeIn(Dot(**moving_dot_kwargs).move_to(median_B.end_manim)), FadeIn(Dot(**moving_dot_kwargs).move_to(median_C.end_manim)))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))


class Height(MovingCameraScene):
    def construct(self):
        A, B, C = np.array([-4, -2, 0]), np.array([4, -3, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)
        triangleE2 = TriangleE2(A=A[0:2], B=B[0:2], C=C[0:2])

        height_A = triangleE2.height(A[0:2])

        M_dot = Dot(**moving_dot_kwargs).move_to(B)
        M_tex = always_redraw(lambda: Tex("M", **tex_kwargs).next_to(M_dot, RIGHT))
        AM = always_redraw(lambda: LineE2(A[0:2], M_dot.get_center()[0:2]).get_Line(**line_kwargs))

        BM = LineE2(B[0:2], height_A.end_point)

        self.add(A_dot, B_dot, C_dot, A_tex, B_tex, C_tex, triangleE2.AB.get_Line(**line_kwargs), triangleE2.BC.get_Line(**line_kwargs), triangleE2.AC.get_Line(**line_kwargs), M_dot, AM)
        self.play(Write(M_tex))
        self.play(M_dot.animate.move_to(height_A.end_manim))

        right_angle = RightAngle(BM.get_Line(), AM, **right_angle_kwargs, quadrant=(-1, -1))
        self.play(Create(right_angle))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # height_B =
        # height_C =


class Bisector(MovingCameraScene):
    def construct(self):
        A, B, C = np.array([-4, -2, 0]), np.array([4, -3, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)
        triangleE2 = TriangleE2(A=A[0:2], B=B[0:2], C=C[0:2])

        bisector_A = triangleE2.bisector(A[0:2])

        M_dot = Dot(**moving_dot_kwargs).move_to(B)
        M_tex = always_redraw(lambda: Tex("M", **tex_kwargs).next_to(M_dot, RIGHT))
        AM = always_redraw(lambda: LineE2(A[0:2], M_dot.get_center()[0:2]).get_Line(**line_kwargs))

        BM = LineE2(B[0:2], bisector_A.end_point)
        MC = LineE2(bisector_A.end_point, C[0:2])

        self.add(A_dot, B_dot, C_dot, A_tex, B_tex, C_tex, triangleE2.AB.get_Line(**line_kwargs), triangleE2.BC.get_Line(**line_kwargs), triangleE2.AC.get_Line(**line_kwargs), M_dot, AM)
        self.play(Write(M_tex))

        self.play(M_dot.animate.move_to(bisector_A.end_manim))
        angle_1 = Angle((triangleE2.adjacent_sides[tuple(A[0:2])][0]).get_Line(), AM, radius=1.25, **angle_kwargs)
        angle_2 = Angle(AM, (triangleE2.adjacent_sides[tuple(A[0:2])][1]).get_Line(), radius=1.25, **angle_kwargs)
        self.play(Create(angle_1), Create(angle_2))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))


class MovingCircles(MovingCameraScene):
    def construct(self):
        A, B, C = np.array([-4, -2, 0]), np.array([4, -3, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)

        # triangleE2_redraw = TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2])

        incenter_redraw = always_redraw(lambda: Dot(**moving_dot_kwargs).move_to(LineE2.make_R3(TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).incenter)))
        # circumscribed_center_redraw = always_redraw(lambda: Dot(**moving_dot_kwargs).move_to(LineE2.make_R3(TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).circumscribed_center)))
        inscribed_circle_redraw = always_redraw(lambda: Circle(radius=TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).inscribed_radius, **circle_kwargs).move_to(incenter_redraw))
        #circumscribed_circle_redraw = always_redraw(lambda: Circle(radius=TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).circumscribed_radius, **circle_kwargs).move_to(circumscribed_center_redraw))

        unsigned_center_A_redraw = always_redraw(lambda: Dot(**moving_dot_kwargs).move_to(LineE2.make_R3(TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_center(A_dot.get_center()[0:2]))))
        unsigned_circle_A_redraw = always_redraw(lambda: Circle(radius=TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_radius(A_dot.get_center()[0:2]), **circle_kwargs).move_to(unsigned_center_A_redraw))

        unsigned_center_B_redraw = always_redraw(lambda: Dot(**moving_dot_kwargs).move_to(LineE2.make_R3(TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_center(B_dot.get_center()[0:2]))))
        unsigned_circle_B_redraw = always_redraw(lambda: Circle(radius=TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_radius(B_dot.get_center()[0:2]), **circle_kwargs).move_to(unsigned_center_B_redraw))

        unsigned_center_C_redraw = always_redraw(lambda: Dot(**moving_dot_kwargs).move_to(LineE2.make_R3(TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_center(C_dot.get_center()[0:2]))))
        unsigned_circle_C_redraw = always_redraw(lambda: Circle(radius=TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).unsigned_circle_radius(C_dot.get_center()[0:2]), **circle_kwargs).move_to(unsigned_center_C_redraw))
        AB_redraw = always_redraw(lambda: TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).AB.scale(2).get_Line(**line_kwargs))
        BC_redraw = always_redraw(lambda: TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).BC.scale(2).get_Line(**line_kwargs))
        AC_redraw = always_redraw(lambda: TriangleE2(A=A_dot.get_center()[0:2], B=B_dot.get_center()[0:2], C=C_dot.get_center()[0:2]).AC.scale(2).get_Line(**line_kwargs))

        self.play(DrawBorderThenFill(A_dot), DrawBorderThenFill(B_dot), DrawBorderThenFill(C_dot))
        self.play(Create(AB_redraw), Create(BC_redraw), Create(AC_redraw), run_time=2)
        self.wait(2)
        self.play(DrawBorderThenFill(incenter_redraw), DrawBorderThenFill(unsigned_center_A_redraw), DrawBorderThenFill(unsigned_center_B_redraw), DrawBorderThenFill(unsigned_center_C_redraw))
        self.play(self.camera.frame.animate.scale(4))
        self.play(Create(inscribed_circle_redraw), Create(unsigned_circle_A_redraw), Create(unsigned_circle_C_redraw), Create(unsigned_circle_B_redraw))
        self.wait(2)
        self.play(A_dot.animate.shift(5*LEFT), B_dot.animate.shift(5*RIGHT), C_dot.animate.shift(5*UP), run_time=2)
        self.play(A_dot.animate.shift(5*RIGHT), B_dot.animate.shift(5*LEFT), C_dot.animate.shift(5*DOWN), run_time=2)
        self.play(A_dot.animate.shift(5*RIGHT), B_dot.animate.shift(5*RIGHT), run_time=2)
        self.play(A_dot.animate.shift(5*LEFT), B_dot.animate.shift(5*LEFT), run_time=2)
        self.play(FadeOut(*self.mobjects))