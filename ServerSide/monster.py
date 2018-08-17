import random as rd
import numpy as np
import math


class Monster:

    def __init__(self):
        self.name = ''
        self.pos_x = 0
        self.pos_y = 0
        self.hp = 150
        self.attribute = []
        self.shield = ()
        self.damage = 20
        self.player_previous_turn = []
        self.player_similarity_count = 0
        self.enemy_pos = ()
        self.first_turn = True
        self.random_init()

    def random_init(self):
        def _get_random_name():
            return open('names', 'r').readlines()[rd.randint(0, 4945)].replace('\n', '')
        def _get_random_pos():
            return rd.randint(0, 100), rd.randint(0, 100)

        self.name = _get_random_name()
        self.pos_x, self.pos_y = 75, 75
        self.shield = self.get_protection()
        if rd.random() <= 0.1:
            self.damage = rd.randint(20, 150)
        if rd.random() <= 0.1:
            self.hp += rd.randint(1, 3000)

    def introduce_yourself(self):
        return (f'Monster known as {self.name}. It stands at {(self.pos_x, self.pos_y)}.\nIt\'s hp is {self.hp}.'
                f'Deals {self.damage} damage per hit.\n')

    def die(self):
        def _gen_prize():
            pass
        return _gen_prize()

    @staticmethod
    def check_intersection(xa1, ya1, xa2, ya2, xb1, yb1, xb2, yb2):
        a1 = ya2 - ya1
        b1 = xa1 - xa2

        a2 = yb2 - yb1
        b2 = xb1 - xb2
        c1 = a1 * xa1 + b1 * ya1
        c2 = a2 * xb1 + b2 * yb1

        det = a1*b2 - a2*b1
        if det == 0:
            return False
        else:
            intersectX = (b2 * c1 - b1 * c2) / det
            intersectY = (a1 * c2 - a2 * c1) / det
            rx0 = 0
            if xa2 - xa1==0:
                rx0 = -1
            else:
                rx0 = (intersectX - xa1) / (xa2 - xa1)

            ry0 = 0
            if ya2 - ya1==0:
                ry0 = -1
            else:
                ry0 = (intersectY - ya1) / (ya2 - ya1)

            rx1 = 0
            if  xb2 - xb1 == 0:
                rx1 = -1
            else:
                rx1 = (intersectX - xb1) / (xb2 - xb1)

            ry1 = 0
            if yb2 - yb1 == 0:
                ry1 = -1
            else:
                ry1 = (intersectY - yb1) / (yb2 - yb1)

        return ((rx0 >= 0 and rx0 <= 1) or (ry0 >= 0 and ry0 <= 1)) and\
               ((rx1 >= 0 and rx1 <= 1) or (ry1 >= 0 and ry1 <= 1))

    def reduce_damage(self, dmg):
        return max(0.95, math.hypot(self.shield[1][0] - self.shield[0][0], self.shield[1][1] - self.shield[1][0])) * dmg

    def apply_human_attack(self, path, dmg):
        def compare_paths(path1, path2):
            if len(path1) == 0 or len(path1) != len(path2) or len(path2) == 0:
                return False

            for i in range(len(path1)):
                if path1[i][0]!=path2[i][0] or path1[i][1]!=path2[i][1]:
                    return False

            return True

        reduced = False
        for x in range(1, len(path)):
            if self.check_intersection(self.shield[0][0], self.shield[0][1], self.shield[1][0], self.shield[1][1],
                                    path[x-1][0], path[x-1][1], path[x][0], path[x][1]):
                if not reduced:
                    dmg = self.reduce_damage(dmg)

            if math.floor(path[x-1][0]) == self.pos_x and math.floor(path[x-1][1]) == self.pos_y:
                self.hp -= dmg
                break

        if self.hp <= 0:
            self.die()

        if compare_paths(self.player_previous_turn, path):
            self.player_similarity_count += 1

        self.player_previous_turn = path

    def get_monster_turn(self, dictionary):
        action = dictionary['act']
        if self.first_turn:
            self.first_turn = False
            return self.get_protection(hero_pos=self.enemy_pos)
        else:
            if action=='atk':
                self.apply_human_attack(dictionary['way'], dictionary['dmg'])
                if self.player_similarity_count >= 2:
                    return self.move(self.pos_x, self.pos_y)
                else:
                    return self.get_attack(self.enemy_pos)
            elif action == 'mov':
                self.enemy_pos = (dictionary['x'], dictionary['y'])
                return self.get_attack(self.enemy_pos)
            else:
                return self.get_attack(self.enemy_pos)


    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        return {'act':'mov', 'x':x, 'y':y}


    def get_attack(self, hero_pos = (1,1)):
        def calc_parabola_vertex(x1, y1, x2, y2, x3, y3):
            denom = (x1 - x2) * (x1 - x3) * (x2 - x3)
            a = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom
            b = (x3 * x3 * (y1 - y2) + x2 * x2 * (y3 - y1) + x1 * x1 * (y2 - y3)) / denom
            c = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom
            return a,b,c

        def _get_middle_point(x, y, hero_pos):
            if rd.random()>= 0.2:
                return (x + hero_pos[0]) / 2, y
            else:
                return (x + hero_pos[0]) / 2, hero_pos[1]
            pass

        middle_x, middle_y = _get_middle_point(self.pos_x, self.pos_y, hero_pos)
        a,b,c = calc_parabola_vertex(self.pos_x, self.pos_y, middle_x, middle_y, hero_pos[0], hero_pos[1])
        #
        # middle_x, middle_y = (x0+x1)/2, y0
        # a,b,c = calc_parabola_vertex(x0, y0, middle_x, middle_y, x1, y1)


        # xs = [x for x in np.arange(0, x1, 0.1)]

        xs = [x for x in np.arange(hero_pos[0], self.pos_x, 0.5)]
        ys = [a * y ** 2 + b * y + c for y in xs]
        path = tuple(zip(xs,ys))

        return {'act':'atk', 'way':path, 'dmg':self.damage}


    def setup_opponent(self, dictionary):
        self.enemy_pos = (dictionary['x'], dictionary['y'])

# get_attack(1,1,77.1,22.6)

    def get_protection(self, hero_pos = (1,1)):
    # def get_protection(x0,y0,x1,y1):
        # x1, y1 = hero_pos
        # m = (self.pos_y - y1)/(self.pos_x - x1)
        def rotate(x,y, theta):
            xprime = x * math.cos(theta) - y * math.sin(theta)
            yprime = y * math.cos(theta) - x * math.sin(theta)
            return xprime, yprime

        line = [(self.pos_x-0.2, self.pos_y), (self.pos_x, self.pos_y-0.2)]

        self.shield = line
        return {'act':'prt'}
