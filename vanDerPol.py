from manim import *

class VanDerPol(Scene):
    def construct(self):

        VanDerPol = StreamLines(func=lambda pos: (pos[1])*RIGHT + (-(pos[0]**4-1)*pos[1]-pos[0]  )*UP)

        self.add(VanDerPol)
        VanDerPol.start_animation(warm_up=True, flow_speed=1.5, )

        self.wait(8)
        