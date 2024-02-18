from manim import *
import numpy as np

sdfsdfksf


class MatrixVectorMultiplication(Scene):
    def construct(self):
        # Matrix and vector setup
        matrix = Matrix([[-3, 2], [5, 1]], h_buff=2.5)
        vector = Matrix([[1], [2]], h_buff=1.5)
        vector.next_to(matrix, LEFT, buff=1)
        result_vector = Matrix([[1], [6]], h_buff=1.5)
        result_vector.next_to(matrix, RIGHT, buff=1)

        # Highlight the first column of the matrix
        matrix_col_highlight = SurroundingRectangle(
            matrix.get_columns()[0], color=YELLOW
        )

        # Equations for transformation
        # Corrected equation for transformation
        equation = Tex(
            "$-3 \\times 1 + 2 \\times 2$",
            ",\\ ",
            "$5 \\times 1 + 1 \\times 2$",
            font_size=24,
        )
        equation.next_to(matrix, DOWN, buff=0.5)

        # Animation
        self.play(Create(matrix), Create(vector))
        self.play(Create(matrix_col_highlight))
        self.wait(1)
        self.play(TransformFromCopy(vector, result_vector))
        self.wait(1)
        self.play(FadeIn(equation))
        self.wait(1)
