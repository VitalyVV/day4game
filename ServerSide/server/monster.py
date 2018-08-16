import matplotlib.pyplot as plt
import random as rd
import numpy as np
import math


class Monster:

    def __init__(self):
        self.name = ''
        self.pos_x = 0
        self.pos_y = 0
        self.hp = 100
        self.attribute = []
        self.shield = ()
        self.damage = 20

    def random_init(self):
        def _get_random_name():
            return open('names', 'r').readlines()[rd.randint(0, 4945)].replace('\n', '')
        def _get_random_pos():
            return rd.randint(0, 100), rd.randint(0, 100)

        self.name = _get_random_name()
        self.pos_x, self.pos_y = _get_random_pos()
        self.shield = self.get_protection()
        if rd.random() <= 0.1:
            self.damage = rd.randint(20, 150)

    def introduce_yourself(self):
        print(f'Monster known as {self.name}. Stands at {(self.pos_x, self.pos_y)}.\nIt\'s hp is {self.hp}.')
        print(f'Deals {self.damage} damage per hit.')

    def get_description(self):
        pass

    def die(self):
        def _gen_prize():
            pass
        return _gen_prize()


    def get_attack(self, hero_pos):
    # def get_attack(x0,y0,x1,y1):
        def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
            denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
            a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
            b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
            c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
            return a,b,c

        def get_middle_point(previous_results):
            pass

        middle_x, middle_y = (self.pos_x + hero_pos[0])/ 2, self.pos_y
        a,b,c = calc_parabola_vertex(self.pos_x, self.pos_y, middle_x, middle_y, hero_pos[0], hero_pos[1])
        #
        # middle_x, middle_y = (x0+x1)/2, y0
        # a,b,c = calc_parabola_vertex(x0, y0, middle_x, middle_y, x1, y1)


        # xs = [x for x in np.arange(0, x1, 0.1)]

        xs = [x for x in np.arange(0, self.pos_x, 0.5)]
        print(len(xs))
        ys = []
        for y in xs:
            ys.append(a*y**2 + b*y + c)


        plt.plot(xs, ys)
        plt.ylabel('parab')
        plt.show()


# get_attack(1,1,77.1,22.6)

    def get_protection(self, hero_pos = (1,1)):
    # def get_protection(x0,y0,x1,y1):
        # x1, y1 = hero_pos
        # m = (self.pos_y - y1)/(self.pos_x - x1)
        def rotate(x,y, theta):
            xprime = x * math.cos(theta) - y * math.sin(theta)
            yprime = y * math.cos(theta) - x * math.sin(theta)
            return xprime, yprime

        line = [(self.pos_x-0.5, self.pos_y), (self.pos_x, self.pos_y-0.5)]

        return line







mon = Monster()
mon.random_init()
mon.introduce_yourself()


