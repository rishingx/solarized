#========== IMPORT ==========#

import random

#========== GRID CLASS ==========#

class Grid:
    def __init__(self, houses, fluc, chg, pay):
        self.houses = houses
        self.fluc = fluc
        self.chg = chg
        self.pay = pay
        self.cur_sheet = []
        self.revenue = 0

    def cycle(self):
        self.cur_sheet = []
        self.revenue = 0
        for i in range(self.houses):
            prod = round((random.random()-0.5)*self.fluc, 4)
            cons = round((random.random()-0.5)*self.fluc, 4)
            diff = round((prod - cons), 4)
            self.revenue -= diff
            self.cur_sheet.append((prod, cons, diff))

    def get_amount(self):
        if self.revenue >= 0:
            return self.revenue * self.chg
        else:
            return self.revenue * self.pay
