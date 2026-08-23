# manim_linalg


<video autoplay loop muted playsinline width="100%">
  <source src="https://kitty-whistle.github.io/manim_linalg/gifs/TriangleScene_1.mp4" type="video/mp4">
</video>

```python
from utils_2D import *


class TriangleScene_1(MovingCameraScene):
    def construct(self):
        dot_kwargs = {"radius": 0.05, "fill_color": BLUE, "stroke_color": BLACK, "stroke_width": 2, "z_index": 1}
        line_kwargs = {"stroke_color": GREY, "stroke_opacity": 0.8, "stroke_width": 5, "z_index": 0}
        tex_kwargs = {"font_size": 25, "z_index": 1}

        A, B, C = np.array([-3, -2, 0]), np.array([3, -1, 0]), np.array([4, 3, 0])
        A_dot, B_dot, C_dot = Dot(**dot_kwargs).move_to(A), Dot(**dot_kwargs).move_to(B), Dot(**dot_kwargs).move_to(C)
        A_tex, B_tex, C_tex = Tex("A", **tex_kwargs).next_to(A, DOWN), Tex("B", **tex_kwargs).next_to(B, DOWN), Tex("C", **tex_kwargs).next_to(C, RIGHT)
        triangleE2 = TriangleE2(A=A[0:2], B=B[0:2], C=C[0:2])

        self.play(DrawBorderThenFill(A_dot), DrawBorderThenFill(B_dot), DrawBorderThenFill(C_dot))
        self.play(Write(A_tex), Write(B_tex), Write(C_tex))
        self.play(Create(triangleE2.AB.get_Line(**line_kwargs)), Create(triangleE2.BC.get_Line(**line_kwargs)), Create(triangleE2.AC.get_Line(**line_kwargs)))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

```
