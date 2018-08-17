from ClientSide.client_socket import Connection
import math

class Hero:

    def __init__(self, name):
        self.name = name
        self.pos_x = 1
        self.pos_y = 1
        self.hp = 100
        self.damage = 20
        self.shield = [(1.1, 1),(1, 1.1)]
        self.conn = Connection()
        self._enabled = True



    def attack(self, func):
        """
        Perform checking of a function by following criteria:
            Between every tuple of an array should be not more than 0.5 distance.

        Check the array of function and attacking the monster.
        Raising Runtime Error if checking failed.
        :param func:
        :return:
        """

        if not self._enabled:
            raise RuntimeError('You died')

        def _check_func(func):
            arr = func()
            for i in range(len(arr)):
                if i+1 < len(arr):
                    if math.hypot(math.fabs(arr[i+1][0] - arr[i][0]),math.fabs(arr[i+1][1] - arr[i][1]))>0.5:
                        return False
            return True

        attack = {'act':'atk'}
        if _check_func(func):
            attack['way'] = func()
            attack['dmg'] = self.damage
        else:
            raise RuntimeError('Wrong function')

        self._send(attack)
        self._receive()

    def protect(self, line):
        """
        Creates line for protection. Protection reduces amount of damage coming.
        By default creates line from [1,2] to [2,1]
        If you passing line it should be list of tuples with coordinates, specifies
        your position of a shield. Cannot be far than 1 unit from player
        :param line: list of 2 tuples
        :return:
        """
        def _check_line(x,y, line):
            if len(line)==2 and isinstance(line[0], tuple) and isinstance(line[1], tuple):
                x0, y0, x1, y1 = line[0][0], line[0][1], line[1][0], line[1][1]
                return math.hypot(x-x0, y - y0)<=1 and math.hypot(x-x1, y-y1)<=1
            else: return False

        if not self._enabled:
            raise RuntimeError('You died')

        prot = {'act': 'def'}
        if line is None:
            prot['line'] = [(1,2), (2,1)]
        if _check_line(self.pos_x, self.pos_y, line):
            prot['line'] = line
        else:
            raise RuntimeError('Wrong parameters')

        self._send(prot)
        self._receive()

    def _get_step(self,x, y):
        if self.pos_x != x:
            if self.pos_x > x:
                self.pos_x -= 1
            else:
                self.pos_x += 1
        if self.pos_y != y:
            if self.pos_y > y:
                self.pos_y -= 1
            else:
                self.pos_y += 1

    def move(self, x=1, y=1):
        """
        Move to a point specified, for 1 step at a turn.
        :param x: x coordinate of destination
        :param y: y coordinate of destination
        :return:
        """
        if self._enabled:
            if x<=100 and y <=100:
                while(self.pos_x != x or self.pos_y != y):
                    self._get_step(x, y)
                    move = {'act':'mov', 'x':self.pos_x, 'y':self.pos_y}
                    self._send(move)
                    self._receive()
            else: raise RuntimeError('You ran outside the battlefield')
        else:
            raise RuntimeError('You died')

    def _send(self, dictionary):
        self.conn.send_message(dictionary)

    def apply_attack(self, path, dmg):
        reduced = False
        for x in range(1, len(path)):
            if self.check_intersection(self.shield[0][0], self.shield[0][1], self.shield[1][0], self.shield[1][1],
                                       path[x - 1][0], path[x - 1][1], path[x][0], path[x][1]):
                if not reduced:
                    dmg = self.reduce_damage(dmg)

            if math.floor(path[x-1][0]) == self.pos_x and math.floor(path[x-1][1]) == self.pos_y:
                self.hp -= dmg
                break

        if self.hp <= 0:
            self._die()

    @staticmethod
    def check_intersection(xa1, ya1, xa2, ya2, xb1, yb1, xb2, yb2):
        a1 = ya2 - ya1
        b1 = xa1 - xa2

        a2 = yb2 - yb1
        b2 = xb1 - xb2
        c1 = a1 * xa1 + b1 * ya1
        c2 = a2 * xb1 + b2 * yb1

        det = a1 * b2 - a2 * b1
        if det == 0:
            return False
        else:
            intersectX = (b2 * c1 - b1 * c2) / det
            intersectY = (a1 * c2 - a2 * c1) / det
            rx0 = 0
            if xa2 - xa1 == 0:
                rx0 = -1
            else:
                rx0 = (intersectX - xa1) / (xa2 - xa1)

            ry0 = 0
            if ya2 - ya1 == 0:
                ry0 = -1
            else:
                ry0 = (intersectY - ya1) / (ya2 - ya1)

            rx1 = 0
            if xb2 - xb1 == 0:
                rx1 = -1
            else:
                rx1 = (intersectX - xb1) / (xb2 - xb1)

            ry1 = 0
            if yb2 - yb1 == 0:
                ry1 = -1
            else:
                ry1 = (intersectY - yb1) / (yb2 - yb1)

        return ((rx0 >= 0 and rx0 <= 1) or (ry0 >= 0 and ry0 <= 1)) and \
               ((rx1 >= 0 and rx1 <= 1) or (ry1 >= 0 and ry1 <= 1))

    def reduce_damage(self, dmg):
        return max(0.95, math.hypot(self.shield[1][0] - self.shield[0][0], self.shield[1][1] - self.shield[1][0])) * dmg

    def _receive(self):
        actions = self.conn.receive_message()
        enemy = ''
        if self.conn.game_type == 'solo':
            enemy = 'monster'
        else:
            enemy = 'other hero'
        if actions['act'] == 'intro':
            print(actions['msg'])
            self._send({'act': 'intro', 'x': self.pos_x, 'y': self.pos_y})
            return actions

        if actions['act'] == 'atk':
            self.apply_attack(actions['way'], actions['dmg'])
            print('You receive a hit from {}. It deals {} damage and your hp now is '
                  '{}.'.format(enemy, actions['dmg'], self.hp))
        elif actions['act'] == 'prt':
            print('Enemy put a protection barrier.')
        elif actions['act'] == 'mov':
            print('Enemy had moved onto position ({}, {})'.format(actions['x'], actions['y']))

        return actions


    def _die(self):
        self._enabled = False
        self.conn.close()
