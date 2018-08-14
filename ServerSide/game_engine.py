from Monster import Monster
import numpy
import math



class Field:

    def __init__(self):
        self.max_x = 100.0
        self.max_y = 100.0

    def generate_monster(self):
        return Monster().random_init()
