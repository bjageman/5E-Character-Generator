from v1.apps import app, db

import random

class Dice(db.Model):
    __tablename__ = 'dice'
    id = db.Column(db.Integer, primary_key= True)
    quantity = db.Column(db.Integer, default=1)
    min = db.Column(db.Integer, default=1)
    max = db.Column(db.Integer)
    def roll(self, quantity=None):
        if quantity is None:
            quantity = self.quantity
        total = 0
        for i in range(quantity):
            total = total + random.randint(self.min, self.max)
        return total
