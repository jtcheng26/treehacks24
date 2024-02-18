from manim import *
import numpy as np

class MatrixIntroduction(Scene):
    def construct(self):
        matrix = Matrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]], v_buff=0.5, h_buff=0.5).set_stroke(width=0.5)
        matrix_label = MathTex('A = ', font_size=24).next_to(matrix, LEFT)

        self.play(Write(matrix_label), Write(matrix))
        self.wait(1)