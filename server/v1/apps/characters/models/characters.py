from v1.apps import app, db


def get_ability(name):
    return Ability.query.filter_by(name=name).first()

def get_skill(name):
    return Skill.query.filter_by(name=name).first()

def get_class(name):
    return ClassInfo.query.filter_by(name=name).first()

def get_race(name):
    return Race.query.filter_by(name=name).first()

class_skill_table = db.Table('class_skill', db.Model.metadata,
    db.Column('class_info_id', db.Integer, db.ForeignKey('class_info.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class_weapon_proficiency_table = db.Table('class_weapon_proficiency', db.Model.metadata,
    db.Column('class_info_id', db.Integer, db.ForeignKey('class_info.id')),
    db.Column('weapon_id', db.Integer, db.ForeignKey('weapon.id'))
)

class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    player_character = db.Column(db.Boolean, default=False)
    race = db.relationship("Race", backref="characters")
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
    character_classes = db.relationship("CharacterClass", lazy='dynamic')
    abilities = db.relationship("CharacterAbility", lazy='dynamic')
    skills = db.relationship("CharacterSkill", lazy='dynamic')
    def get_ability(self, ability):
        return self.abilities.filter(CharacterAbility.ability.has(name=ability)).first()
    def get_skill(self, skill):
        return self.skills.filter(CharacterSkill.skill.has(name=skill)).first()
    def add_race_modifiers(self):
        for ability_mod in self.race.ability_mods:
            iterator = (char_ability for char_ability in self.abilities if ability_mod.ability.name in char_ability.ability.name)
            for ability in iterator:
                ability.score = ability.score + ability_mod.modifier

class CharacterClass(db.Model):
    __tablename__ = 'character_class'
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    starting = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer)
    class_info_id = db.Column(db.Integer, db.ForeignKey('class_info.id'), primary_key=True)
    class_info = db.relationship("ClassInfo")
    def __init__(self, class_info, level, starting=False):
        self.class_info = class_info
        self.level = level
        self.starting = starting

class CharacterSkill(db.Model):
    __tablename__ = 'character_skill'
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    proficient = db.Column(db.Boolean, default=False)
    modifier = db.Column(db.Integer)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    skill = db.relationship("Skill")
    def __init__(self, skill):
        self.skill = skill
        self.proficient = True

class CharacterAbility(db.Model):
    __tablename__ = 'character_ability'
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    score = db.Column(db.Integer)
    modifier = db.Column(db.Integer)
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'), primary_key=True)
    ability = db.relationship("Ability")
    def __init__(self, ability, score):
        self.ability = ability
        self.score = score

    def __setattr__(self, name, value):
        # Call the parent class method first.
        super(CharacterAbility, self).__setattr__(name, value)
        if (name == "score"):
            self.modifier = int((self.score - 10) / 2)

class RaceAbility(db.Model):
    __tablename__ = 'race_ability'
    race_id = db.Column(db.Integer, db.ForeignKey('race.id'), primary_key=True)
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'), primary_key=True)
    modifier = db.Column(db.Integer)
    ability = db.relationship("Ability")
    def __init__(self, ability, modifier):
        self.ability = ability
        self.modifier = modifier

class ClassInfo(db.Model):
    __tablename__ = 'class_info'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    spell_ability = db.relationship("Ability")
    spell_ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'))
    skill_proficiencies = db.relationship("Skill",
                    secondary=class_skill_table,
                    backref="class_skills")

class Ability(db.Model):
    __tablename__ = 'ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    saving_throw_id = db.Column(db.Integer, db.ForeignKey('saving_throw.id'))

class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    ability = db.relationship("Ability")
    ability_id = db.Column(db.Integer, db.ForeignKey('ability.id'))

class SavingThrow(db.Model):
    __tablename__ = 'saving_throw'
    id = db.Column(db.Integer, primary_key=True)
    ability = db.relationship("Ability", uselist=False, backref="ability_saving_throw")

class Race(db.Model):
    __tablename__ = 'race'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
    size = db.Column(db.String(32))
    speed = db.Column(db.Integer, default=30)
    ability_mods = db.relationship("RaceAbility")
    def get_ability_modifier(self, ability):
        iterator = ( modifier for modifier in self.ability_mods if ability in modifier.ability.name )
        for modifier in iterator:
            return modifier
        return RaceAbility(get_ability(ability), modifier=0)

class Weapon(db.Model):
    __tablename__ = 'weapon'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(32))
