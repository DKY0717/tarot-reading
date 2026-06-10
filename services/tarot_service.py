import random
import json
from database.models import Card, Spread, Reading
from database import db

class TarotService:
    @staticmethod
    def get_all_cards():
        return Card.query.all()
    
    @staticmethod
    def get_card_by_id(card_id):
        return Card.query.get(card_id)
    
    @staticmethod
    def get_cards_by_arcana(arcana):
        return Card.query.filter_by(arcana=arcana).all()
    
    @staticmethod
    def get_cards_by_suit(suit):
        return Card.query.filter_by(suit=suit).all()
    
    @staticmethod
    def get_all_spreads():
        return Spread.query.all()
    
    @staticmethod
    def get_spread_by_id(spread_id):
        return Spread.query.get(spread_id)
    
    @staticmethod
    def draw_cards(spread_id):
        spread = Spread.query.get(spread_id)
        if not spread:
            return None
        
        all_cards = Card.query.all()
        drawn_cards = random.sample(all_cards, spread.positions)
        
        result = []
        for i, card in enumerate(drawn_cards):
            is_reversed = random.random() < 0.3
            result.append({
                'card': card.to_dict(),
                'is_reversed': is_reversed,
                'position': i + 1,
                'position_meaning': spread.positions_list[i].meaning if i < len(spread.positions_list) else ''
            })
        
        return result
    
    @staticmethod
    def draw_single_card():
        all_cards = Card.query.all()
        card = random.choice(all_cards)
        is_reversed = random.random() < 0.3
        return {
            'card': card.to_dict(),
            'is_reversed': is_reversed
        }
    
    @staticmethod
    def save_reading(spread_id, question, cards_drawn, ai_interpretation=None):
        reading = Reading(
            spread_id=spread_id,
            question=question,
            cards_drawn=json.dumps(cards_drawn, ensure_ascii=False),
            ai_interpretation=ai_interpretation
        )
        db.session.add(reading)
        db.session.commit()
        return reading
    
    @staticmethod
    def get_readings(limit=20):
        return Reading.query.order_by(Reading.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_readings_paginated(page=1, per_page=10):
        total = Reading.query.count()
        total_pages = max(1, (total + per_page - 1) // per_page)
        readings = Reading.query.order_by(Reading.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        return readings, total, total_pages
    
    @staticmethod
    def get_reading_by_id(reading_id):
        return Reading.query.get(reading_id)
    
    @staticmethod
    def delete_reading(reading_id):
        reading = Reading.query.get(reading_id)
        if reading:
            db.session.delete(reading)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def search_cards(keyword):
        return Card.query.filter(
            (Card.name.like(f'%{keyword}%')) |
            (Card.name_en.like(f'%{keyword}%')) |
            (Card.upright_meaning.like(f'%{keyword}%')) |
            (Card.reversed_meaning.like(f'%{keyword}%'))
        ).all()
