from manim import *

class MatrixMultiplicationScene(Scene):
    def construct(self):
        matrix = Matrix([
            [1, 2],
            [3, 4]
        ]).set_edge_and_bar_color(edge_color=BLACK, bar_color=WHITE)

        matrix_labels = VGroup(*[
            Tex(f"a_{i},{j}".format(i=i, j=j))
            for i in range(2)
            for j in range(2)
        ])

        for i in range(2):
            for j in range(2):
                matrix_labels[i*2+j].move_to(matrix.get_corner(UL) + (i*UNIT_ vectors.RIGHT + j*UNIT_vectors.UP))

        self.play(
            Create(matrix),
            Write(matrix_labels)
        )
        self.wait(1)
        self.play(
            *[FadeOut(matrix_labels[i]) for i in range(4)]
        )
        self.wait(1)