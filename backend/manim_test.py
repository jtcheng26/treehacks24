from manim import *
import numpy as np
import random


class RightTriangleWithSquares(Scene):
    def construct(self):
        # Define the triangle
        a = Line(LEFT, RIGHT)
        b = Line(DOWN, UP)
        c = Line(LEFT, RIGHT).rotate(np.pi / 6)
        triangle = VGroup(a, b, c)

        # Define the squares
        a_square = Square().scale(a.get_length()).next_to(a, DOWN)
        b_square = Square().scale(b.get_length()).next_to(b, RIGHT)
        c_square = Square().scale(c.get_length()).next_to(c, UP)
        squares = VGroup(a_square, b_square, c_square)

        # Define the labels
        a_label = MathTex("a").next_to(a, DOWN)
        b_label = MathTex("b").next_to(b, RIGHT)
        c_label = MathTex("c").next_to(c, UP)
        a_square_label = MathTex("a^2").next_to(a_square, DOWN)
        b_square_label = MathTex("b^2").next_to(b_square, RIGHT)
        c_square_label = MathTex("c^2").next_to(c_square, UP)
        labels = VGroup(
            a_label, b_label, c_label, a_square_label, b_square_label, c_square_label
        )

        # Add everything to the scene
        self.add(triangle, squares, labels)


class MatrixSceneB(Scene):
    def construct(self):
        m = 3
        n = 2
        A = Matrix([[1, 2], [3, 4], [5, 6]])
        v = Matrix([[1], [2]])
        A_label = Tex(f"A: {m} x {n}").move_to(A.get_corner(UL) + [-1, 1, 0])
        v_label = Tex(f"v: {n} x 1").move_to(v.get_corner(UR) + [1, 1, 0])
        group = VGroup(A, v, A_label, v_label).arrange(buff=1)
        self.play(Write(group))
        self.wait()


class MatrixScene(Scene):
    def construct(self):
        # Define matrices A and v with placeholder elements
        A = Matrix(
            [
                ["a_{11}", "a_{12}", "...", "a_{1n}"],
                ["a_{21}", "a_{22}", "...", "a_{2n}"],
                ["...", "...", "...", "..."],
                ["a_{m1}", "a_{m2}", "...", "a_{mn}"],
            ],
            element_alignment_corner=UP,
        )

        v = Matrix(
            [["v_{1}"], ["v_{2}"], ["..."], ["v_{n}"]], element_alignment_corner=UP
        )

        # Labels for matrices A and v
        A_label = Text("m x n", font_size=24).next_to(A, UP)
        v_label = Text("n x 1", font_size=24).next_to(v, UP)

        # Position matrices A and v side by side
        A.next_to(v, LEFT, buff=1)

        # Group matrices and labels for alignment
        matrices_group = VGroup(A, v, A_label, v_label).move_to(ORIGIN)

        # Display matrices and labels
        self.play(Write(matrices_group))

        # Placeholder for text overlay with concise text
        text_overlay = Text(
            "Your concise text here", font_size=24, line_spacing=1.5
        ).to_edge(RIGHT, buff=0.5)

        # Ensure text overlay does not overlap with matrices
        if (
            text_overlay.get_top()[1] == A.get_top()[1]
            or text_overlay.get_top()[1] == v.get_top()[1]
        ):
            text_overlay.next_to(matrices_group, RIGHT, buff=0.5)

        # Display text overlay
        self.play(Write(text_overlay))


class MatrixVectorMultiplication(Scene):
    def construct(self):
        m = 3
        n = 2

        A = Matrix([[random.randint(-10, 10) for j in range(n)] for i in range(m)])
        A.set_column_widths(0.5)
        A.set_row_heights(0.5)
        A.add_background_rectangle()
        A_label = Tex("A", font_size=20).next_to(A, UP + LEFT)
        A_dims = Tex(f"{m} x {n}", font_size=15).next_to(A_label, DOWN + LEFT)

        v = Matrix([[random.randint(-10, 10)] for i in range(n)])
        v.set_column_widths(0.5)
        v.set_row_heights(0.5)
        v.add_background_rectangle()
        v_label = Tex("v", font_size=20).next_to(v, UP + RIGHT)
        v_dims = Tex(f"{n} x 1", font_size=15).next_to(v_label, DOWN + RIGHT)

        text = Tex("Matrix-vector multiplication", font_size=20).to_edge(RIGHT)

        self.play(
            Write(A),
            Write(A_label),
            Write(A_dims),
            Write(v),
            Write(v_label),
            Write(v_dims),
            Write(text),
        )

        self.wait(1)

        self.play(FadeOut(A_dims), FadeOut(v_dims), FadeOut(A_label), FadeOut(v_label))

        self.wait(1)

        self.play(FadeOut(A), FadeOut(v), FadeOut(text))


class PythagoreanTheoremScene(Scene):
    def construct(self):
        # Create the right triangle
        triangle = Polygon([0, 0, 0], [3, 0, 0], [3, 4, 0], color=WHITE)
        a_label = MathTex("a", font_size=24).next_to(
            triangle.get_edge_center(DOWN), DOWN, buff=0.1
        )
        b_label = MathTex("b", font_size=24).next_to(
            triangle.get_edge_center(RIGHT), RIGHT, buff=0.1
        )
        c_label = (
            MathTex("c", font_size=24)
            .move_to(triangle.get_center_of_mass())
            .shift(UP * 0.3 + LEFT * 0.3)
        )

        # Create the squares for each side
        a_square = Square(side_length=3).next_to(triangle, DOWN, buff=0.1)
        a_square_label = MathTex("a^2", font_size=24).move_to(a_square.get_center())

        b_square = Square(side_length=4).next_to(triangle, RIGHT, buff=0.1)
        b_square_label = MathTex("b^2", font_size=24).move_to(b_square.get_center())

        c_square_side_length = np.sqrt(3**2 + 4**2)  # Calculating the hypotenuse length
        c_square = Square(side_length=c_square_side_length).move_to(
            a_square.get_center()
            + np.array(
                [c_square_side_length / 2 + 0.1, c_square_side_length / 2 + 0.1, 0]
            )
        )
        c_square_label = MathTex("c^2", font_size=24).move_to(c_square.get_center())

        # Ensure everything fits on the screen and is not overlapping
        # Adjust position to ensure no overlapping and everything is visible
        all_objects = VGroup(
            triangle,
            a_label,
            b_label,
            c_label,
            a_square,
            a_square_label,
            b_square,
            b_square_label,
            c_square,
            c_square_label,
        ).scale(0.75)

        # Draw the objects on the screen
        self.play(Create(triangle), Write(a_label), Write(b_label), Write(c_label))
        self.wait(1)
        self.play(Create(a_square), Write(a_square_label))
        self.wait(1)
        self.play(Create(b_square), Write(b_square_label))
        self.wait(1)
        self.play(Create(c_square), Write(c_square_label))
        self.wait(2)


class RightTriangle(Scene):
    def construct(self):
        # Define variables
        a = 3
        b = 4
        c = 5

        # Create right triangle
        triangle = Polygon(ORIGIN, DR * a, DR * a + DOWN * b, color=YELLOW)

        # Create labels for sides
        side_a_label = Tex(f"a={a}").next_to(triangle.points[0], DOWN)
        side_b_label = Tex(f"b={b}").next_to(triangle.points[1], LEFT)
        hypotenuse_label = Tex(f"c={c}").next_to(triangle.points[2], RIGHT + UP)

        # Create squares for sides and hypotenuse
        square_a = Square(side_length=a, color=YELLOW)
        square_a.move_to(square_a.get_center() + DOWN)

        square_b = Square(side_length=b, color=YELLOW)
        square_b.move_to(square_b.get_center() + LEFT)

        square_c = Square(side_length=c, color=YELLOW)
        square_c.move_to(square_c.get_center() + RIGHT + UP)

        # Create labels for squares
        square_a_label = Tex(f"$a^2$").next_to(square_a, DOWN)
        square_b_label = Tex(f"$b^2$").next_to(square_b, LEFT)
        square_c_label = Tex(f"$c^2$").next_to(square_c, UP)

        # Arrange objects
        self.play(
            Create(triangle),
            Write(side_a_label),
            Write(side_b_label),
            Write(hypotenuse_label),
        )
        self.wait()

        self.play(Create(square_a), Create(square_b), Create(square_c))
        self.wait()

        self.play(Write(square_a_label), Write(square_b_label), Write(square_c_label))
        self.wait()
