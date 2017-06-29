from v1.apps import app, db

class Attack(db.Model):
    __tablename__ = 'attack'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    damage = db.relationship("Dice", uselist=False, backref="damage_dice")
    to_hit_mod = db.Column(db.Integer, default=0)
    damage_mod = db.Column(db.Integer, default=0)
