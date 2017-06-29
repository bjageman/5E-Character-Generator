
from v1.apps import app, db

class Spell(db.Model):
    __tablename__ = 'spell'
    id = db.Column(db.Integer, primary_key= True)
    casting_time = db.Column(db.String(32))
    components = db.Column(db.String(32))
    description = db.Column(db.String(256))
    duration = db.Column(db.String(32))
    level = db.Column(db.Integer, default=0)
    range_distance = db.Column(db.Integer, default=0)
    school = db.Column(db.String(32))
