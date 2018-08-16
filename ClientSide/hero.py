from ClientSide.connection import send_data
import math

class Hero:

    def __init__(self, name, strength, intelligence):
        if strength + intelligence > 40:
            raise RuntimeError('You spent more points on strength({}) and intelligence({}) than possible.'.format(strength, intelligence))
        self.name = name
        self.pos_x = 1
        self.pos_y = 1
        self.hp = 100
        self.str = strength
        self.int = intelligence
        self.shield = ()
        self._enabled = True

    def attack(self, func, attack_type):
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

        attack = {'act':'att','type':attack_type}
        if _check_func(func):
            attack['way'] = func()
        else:
            raise RuntimeError('Wrong function')

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
            prot = {'line':[(1,2), (2,1)]}
        if _check_line(self.pos_x, self.pos_y, line):
            prot = {'line':line}
        else:
            raise RuntimeError('Wrong parameters')

        self._send(prot)

    def move(self, x=1, y=1):
        """
        Move to a point specified, for 1 step at a turn.
        :param x: x coordinate of destination
        :param y: y coordinate of destination
        :return:
        """
        if self._enabled:
            if x<=100 and y <=100:
                move = {'act':'move', 'x':x, 'y':y}
            else: raise RuntimeError('You run outside the battlefield')
        else:
            raise RuntimeError('You died')

    def _to_json(self):
        pass

    def _send(self, dictionary):
        send_data(dictionary)

    @staticmethod
    def _receive(self):
        pass

    def _die(self):
        self._enabled = False
