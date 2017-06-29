from v1.apps import app, db

class Statistics(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer, primary_key= True)
    gender = db.Column(db.String(32))
    alignment = db.Column(db.String(32))
    level = db.Column(db.Integer, default=1)
    hp_dice = db.relationship("Dice", uselist=False, backref="hp_dice")
    strength = db.Column(db.Integer, default=8)
    dexterity = db.Column(db.Integer, default=8)
    constitution = db.Column(db.Integer, default=8)
    intelligence = db.Column(db.Integer, default=8)
    wisdom = db.Column(db.Integer, default=8)
    charisma = db.Column(db.Integer, default=8)
    skills = db.relationship("SkillEntity")
    race = db.relationship("Race")
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    class_info = db.relationship("ClassInfo")
    class_info_id = db.Column(db.Integer, db.ForeignKey('class_info.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    def get_modifier(self, stat):
        return int(float(stat - 10)/2)
    def get_initiative(self):
        return self.get_modifier(self.dexterity)
    def get_armor_class(self):
        return 10 + self.get_modifier(self.dexterity)

class AbilityEntity(db.Model):
    __tablename__ = 'ability_entity'
    statistics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'), primary_key=True)
    modifier = db.Column(db.Integer, default=0)
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'))
    ability = db.relationship("Ability")

class SkillEntity(db.Model):
    __tablename__ = 'skill_entity'
    statistics_id = db.Column(db.Integer, db.ForeignKey('statistics.id'), primary_key=True)
    modifier = db.Column(db.Integer, default=0)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'))
    skill = db.relationship("Skill")
