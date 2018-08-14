import random
import numpy as np
import matplotlib.pyplot as plt


class Monster:

    def __init__(self):
        self.name = ''
        self.pos_x = 0
        self.pos_y = 0
        self.hp = 100
        self.attribute = []
        self.str = 0
        self.int = 0
        self.shield = ()

    def random_init(self):
        return self

    def get_description(self):
        pass

    def die(self):
        def _gen_prize():
            pass
        return _gen_prize()


# def get_attack(self, hero_pos):
def get_attack(x0,y0,x1,y1):
    def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
        denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
        a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
        b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
        c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
        return a,b,c

    def get_middle_point(previous_results):
        pass

    # middle_x, middle_y = (self.pos_x + hero_pos[0])/ 2, self.pos_y
    # a,b,c = calc_parabola_vertex(self.pos_x, self.pos_y, middle_x, middle_y, hero_pos[0], hero_pos[1])

    middle_x, middle_y = x1-1, y0
    a,b,c = calc_parabola_vertex(x0, x0, middle_x, middle_y, x1, y1)


    xs = [x for x in np.arange(x0, x1, 0.1)]
    ys = []
    for y in xs:
        ys.append(a*y**2 + b*y + c)

    plt.plot(xs, ys)
    plt.ylabel('parab')
    plt.show()


get_attack(1,1,77.1,22.6)









mon = Monster()


