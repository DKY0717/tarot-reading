from datetime import datetime, timezone
from . import db

class Card(db.Model):
    __tablename__ = 'cards'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    arcana = db.Column(db.String(20), nullable=False)
    suit = db.Column(db.String(20))
    upright_meaning = db.Column(db.Text, nullable=False)
    reversed_meaning = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'number': self.number,
            'arcana': self.arcana,
            'suit': self.suit,
            'upright_meaning': self.upright_meaning,
            'reversed_meaning': self.reversed_meaning,
            'description': self.description,
            'image_path': self.image_path
        }

class Spread(db.Model):
    __tablename__ = 'spreads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    positions = db.Column(db.Integer, nullable=False)
    layout_type = db.Column(db.String(20), nullable=False)
    
    positions_list = db.relationship('SpreadPosition', backref='spread', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'positions': self.positions,
            'layout_type': self.layout_type,
            'positions_list': [p.to_dict() for p in self.positions_list]
        }

class SpreadPosition(db.Model):
    __tablename__ = 'spread_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    spread_id = db.Column(db.Integer, db.ForeignKey('spreads.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    meaning = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'spread_id': self.spread_id,
            'position': self.position,
            'meaning': self.meaning
        }

class Reading(db.Model):
    __tablename__ = 'readings'
    
    id = db.Column(db.Integer, primary_key=True)
    spread_id = db.Column(db.Integer, db.ForeignKey('spreads.id'), nullable=False)
    question = db.Column(db.Text)
    cards_drawn = db.Column(db.Text, nullable=False)
    ai_interpretation = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    spread = db.relationship('Spread', backref='readings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'spread_id': self.spread_id,
            'spread_name': self.spread.name if self.spread else None,
            'question': self.question,
            'cards_drawn': self.cards_drawn,
            'ai_interpretation': self.ai_interpretation,
            'created_at': self.created_at.isoformat()
        }
