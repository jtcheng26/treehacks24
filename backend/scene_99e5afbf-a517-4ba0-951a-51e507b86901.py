from manim import *

class VectorIntro(Scene):
    def construct(self):
        # Set up number line
        number_line = NumberLine(
            x_min=-10, x_max=10,
            unit_size=2,
            number_of_marks=5,
            mark_to_number_mappings={
                2: "$2$",
                4: "$4$",
                6: "$6$",
                8: "$8$",
            }
        )

        # Set up vector
        vector_label = Tex("v", font_size=25).shift(0.5 * RIGHT)
        vector_end = 5 * RIGHT
        vector_start = ORIGIN
        vector_config = Arrow(
            vector_start, vector_end,
            buff=0.2,
            stroke_width=3,
            color=YELLOW
        ).add_label(vector_label)

        # Set up shrinking vector
        shrunk_vector_end = 2 * RIGHT
        shrunk_vector_config = vector_config.copy().shift(
            shrunk_vector_end - vector_end
        )

        # Display all objects
        self.play(
            Create(number_line),
            Create(vector_config),
        )
        self.wait(1)
        self.play(
            vector_config.animate(
                target=(vector_start, shrunk_vector_end)
            ),
        )
        self.wait(1)

        self.play(
            Uncreate(number_line),
            Uncreate(vector_config),
        )