from manim import *
import numpy as np

class VectorIntroduction(Scene):
    def construct(self):
        number_line = NumberLine(x_range=[-10, 10, 0.2], length=10, include_numbers=True)
        vector = Arrow(start=ORIGIN, end=[2, 0, 0], buff=0).set_color(RED)
        vector_label = MathTex('v', font_size=24).next_to(vector, UP, buff=0.1)

        self.play(Create(number_line))
        self.play(GrowArrow(vector), Write(vector_label))
        self.wait(1)
        self.play(vector.animate.scale(0.4, about_point=ORIGIN))
        self.wait(1)