from manim import *
import numpy as np 
import math 

config.frame_height = 8 * 2
config.frame_width = 14.22 * 2

epsilon = 1


class Strength(MovingCameraScene):
    def construct(self):

        # format [[x(m), y(m)], charge(Kl)]
        charges = [[[-3, 0], 6], [[3, 0], -6],]# [[3, 3], -3], [[5, -3], 3], [[1, -1], -4]]

        # cast to required format
        for i in range(len(charges)):
            charges[i] = [np.array(np.array(charges[i][0] + [1.0])), charges[i][1]]

        self.camera.frame.set(width=27)

        def vector_from_points(point1, point2):
            return point2 - point1

        def vector_length(vec):
            return math.sqrt(vec[0] ** 2 + vec[1] ** 2)

        def F(pos): # Coulombs force 
            # pos format - np.array([x, y, 1.0])
            k = 1/ epsilon
            force = np.array([0.0, 0.0])

            for i in range(len(charges)):
                x, y, charge = charges[i][0][0], charges[i][0][1], charges[i][1]
                R = vector_from_points(charges[i][0][:2], pos[:2]) # vector from charge to test charge 
                if(not vector_length(R)): return np.array([0.0, 0.0, 1.0])
                force += k * charge * R / vector_length(R) ** 3 
            force = force / math.sqrt((force[0] ** 2 + force[1] ** 2)) if  math.sqrt((force[0] ** 2 + force[1] ** 2)) != 0 else 0 
            return np.append(force, np.array([1.0]))


        colors = [DARK_GRAY, "#79A870", "#C4D3D0", "#F69347", "#FAD9C2", "#EADB7C", ]

        vector_field = ArrowVectorField(
            F, min_color_scheme_value=0, max_color_scheme_value=3, colors=colors, #length_func=lambda x: math.sqrt(x) / 3
        )

         # add axes 
        ax = Axes(x_range=[-13, 13, 1], y_range=[-7, 7, 1],  x_length = 26, y_length=14, axis_config={"include_numbers": True})
        # self.add(ax)

        self.add(vector_field)  # draw field 

        # draw charges 
        # max_value = max(charges, key = lambda x: abs(x[1]))[1]
        # min_value = min(charges, key = lambda x: abs(x[1]))[1]
        
        R = 0.0001
        for charge in charges:
            for alpha in range(-180, 180, 15):
                xstart, ystart = charge[0][0] + R * math.cos(math.radians(alpha)), charge[0][1] + R * math.sin(math.radians(alpha))
                dot = Dot([xstart, ystart, 1.0], color="#000000")
                trace = TracedPath(dot.get_center, stroke_width=2, stroke_color="#d9b555")
                self.add(dot, trace)
                dot.add_updater(vector_field.get_nudge_updater(speed=10, pointwise = False))

        for i in charges:
            dot = Dot(i[0], color="#FF0000" if i[1] > 0 else "#0000FF",) #radius =(i[1] - min_value)/(max_value - min_value) * 0.30 + 0.08)
            self.add(dot)

        self.wait(6)
