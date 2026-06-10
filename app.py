import os
import json
import time
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
from functools import wraps
from dotenv import load_dotenv
from config import config
from database import db
from database.init_db import init_database
from services.tarot_service import TarotService
from services.ai_service import ai_service

load_dotenv()

_rate_limit_store = {}

def rate_limit(max_calls=30, window=60):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            ip = request.remote_addr
            now = time.time()
            key = f"{ip}:{f.__name__}"
            if key not in _rate_limit_store:
                _rate_limit_store[key] = []
            _rate_limit_store[key] = [t for t in _rate_limit_store[key] if now - t < window]
            if len(_rate_limit_store[key]) >= max_calls:
                return jsonify({'error': '请求过于频繁，请稍后再试'}), 429
            _rate_limit_store[key].append(now)
            return f(*args, **kwargs)
        return decorated
    return decorator

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'tarot.db')
    
    db.init_app(app)
    
    @app.template_filter('from_json')
    def from_json_filter(value):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []
    
    @app.template_filter('nl2br')
    def nl2br_filter(value):
        if value:
            return value.replace('\n', '<br>')
        return ''
    
    with app.app_context():
        init_database(app)
    
    @app.route('/')
    def index():
        daily_card = TarotService.draw_single_card()
        spreads = TarotService.get_all_spreads()
        return render_template('index.html', daily_card=daily_card, spreads=spreads)
    
    @app.route('/reading/<int:spread_id>')
    def reading(spread_id):
        spread = TarotService.get_spread_by_id(spread_id)
        if not spread:
            return redirect(url_for('index'))
        return render_template('reading.html', spread=spread)
    
    @app.route('/immersive/<int:spread_id>')
    def immersive_reading(spread_id):
        spread = TarotService.get_spread_by_id(spread_id)
        if not spread:
            return redirect(url_for('index'))
        return render_template('immersive_reading.html', spread=spread)
    
    @app.route('/api/draw/<int:spread_id>', methods=['POST'])
    @rate_limit(max_calls=10, window=60)
    def draw_cards(spread_id):
        question = request.json.get('question', '')
        spread = TarotService.get_spread_by_id(spread_id)
        if not spread:
            return jsonify({'error': '牌阵不存在'}), 404
        
        cards = TarotService.draw_cards(spread_id)
        if not cards:
            return jsonify({'error': '抽牌失败'}), 500
        
        saved_reading = TarotService.save_reading(
            spread_id=spread_id,
            question=question,
            cards_drawn=cards,
            ai_interpretation=None
        )
        
        return jsonify({
            'cards': cards,
            'reading_id': saved_reading.id,
            'spread_name': spread.name
        })
    
    @app.route('/api/card_pool')
    def card_pool():
        import random as _random
        all_cards = TarotService.get_all_cards()
        pool = [c.to_dict() for c in all_cards]
        _random.shuffle(pool)
        return jsonify({'cards': pool})
    
    @app.route('/api/select_cards', methods=['POST'])
    @rate_limit(max_calls=10, window=60)
    def select_cards():
        data = request.json or {}
        spread_id = data.get('spread_id')
        question = data.get('question', '')
        card_ids = data.get('card_ids', [])
        
        spread = TarotService.get_spread_by_id(spread_id)
        if not spread:
            return jsonify({'error': '牌阵不存在'}), 404
        if len(card_ids) != spread.positions:
            return jsonify({'error': f'需要选择 {spread.positions} 张牌'}), 400
        
        import random as _random
        cards = []
        positions_list = spread.positions_list
        for i, cid in enumerate(card_ids):
            card = TarotService.get_card_by_id(cid)
            if not card:
                return jsonify({'error': f'卡牌 {cid} 不存在'}), 400
            is_reversed = _random.random() < 0.3
            cards.append({
                'card': card.to_dict(),
                'is_reversed': is_reversed,
                'position': i + 1,
                'position_meaning': positions_list[i].meaning if i < len(positions_list) else ''
            })
        
        saved_reading = TarotService.save_reading(
            spread_id=spread_id,
            question=question,
            cards_drawn=cards,
            ai_interpretation=None
        )
        
        return jsonify({
            'cards': cards,
            'reading_id': saved_reading.id,
            'spread_name': spread.name
        })
    
    @app.route('/api/stream/<int:reading_id>')
    def stream_interpretation(reading_id):
        reading = TarotService.get_reading_by_id(reading_id)
        if not reading:
            return jsonify({'error': '记录不存在'}), 404
        
        cards = json.loads(reading.cards_drawn)
        question = reading.question
        spread_name = reading.spread.name if reading.spread else '塔罗牌阵'
        
        def generate():
            full_text = []
            for chunk in ai_service.generate_reading_stream(cards, question=question, spread_name=spread_name):
                full_text.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
            
            complete_text = ''.join(full_text)
            with app.app_context():
                reading = TarotService.get_reading_by_id(reading_id)
                if reading:
                    reading.ai_interpretation = complete_text
                    db.session.commit()
            
            yield f"data: {json.dumps({'type': 'done', 'content': complete_text}, ensure_ascii=False)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream',
                       headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
    
    @app.route('/api/chat', methods=['GET', 'POST'])
    @rate_limit(max_calls=20, window=60)
    def chat():
        if request.method == 'POST':
            data = request.json or {}
        else:
            data = {}
        
        reading_id = data.get('reading_id') or request.args.get('reading_id', type=int)
        message_text = data.get('message') or request.args.get('message', '')
        
        messages = data.get('messages', [])
        if not messages and message_text:
            messages = [{"role": "user", "content": message_text}]
        
        if not messages:
            return jsonify({'error': '消息不能为空'}), 400
        
        reading = TarotService.get_reading_by_id(reading_id) if reading_id else None
        if reading:
            context_msg = {
                "role": "user",
                "content": f"[上下文] 用户刚完成了一次「{reading.spread.name}」占卜。"
            }
            if reading.question:
                context_msg["content"] += f"问题是：{reading.question}。"
            cards = json.loads(reading.cards_drawn)
            card_names = [c['card']['name'] + ('（逆位）' if c['is_reversed'] else '') for c in cards]
            context_msg["content"] += f"抽到的牌：{'、'.join(card_names)}。"
            if reading.ai_interpretation:
                context_msg["content"] += f"AI解读摘要：{reading.ai_interpretation[:300]}。"
            context_msg["content"] += "现在用户想进一步了解。"
            messages = [context_msg] + messages
        
        def generate():
            full_text = []
            for chunk in ai_service.chat_stream(messages):
                full_text.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'content': ''.join(full_text)}, ensure_ascii=False)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream',
                       headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
    
    @app.route('/api/daily')
    @rate_limit(max_calls=20, window=60)
    def daily_card():
        card = TarotService.draw_single_card()
        return jsonify({'card': card})
    
    @app.route('/api/daily_stream', methods=['POST'])
    def daily_stream():
        data = request.json or {}
        card = data.get('card')
        if not card:
            return jsonify({'error': '缺少卡牌数据'}), 400
        
        def generate():
            full_text = []
            for chunk in ai_service.generate_reading_stream([card], spread_name="每日一牌"):
                full_text.append(chunk)
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'content': ''.join(full_text)}, ensure_ascii=False)}\n\n"
        
        return Response(generate(), mimetype='text/event-stream',
                       headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
    
    @app.route('/cards')
    def cards_database():
        arcana_filter = request.args.get('arcana', '')
        suit_filter = request.args.get('suit', '')
        search = request.args.get('search', '')
        
        if search:
            cards = TarotService.search_cards(search)
        elif arcana_filter:
            cards = TarotService.get_cards_by_arcana(arcana_filter)
        elif suit_filter:
            cards = TarotService.get_cards_by_suit(suit_filter)
        else:
            cards = TarotService.get_all_cards()
        
        return render_template('cards.html', cards=cards, 
                             arcana_filter=arcana_filter, 
                             suit_filter=suit_filter,
                             search=search)
    
    @app.route('/card/<int:card_id>')
    def card_detail(card_id):
        card = TarotService.get_card_by_id(card_id)
        if not card:
            return redirect(url_for('cards_database'))
        return render_template('card_detail.html', card=card)
    
    @app.route('/history')
    def history():
        page = request.args.get('page', 1, type=int)
        per_page = 10
        readings, total, total_pages = TarotService.get_readings_paginated(page=page, per_page=per_page)
        return render_template('history.html', readings=readings, 
                             page=page, total_pages=total_pages, total=total)
    
    @app.route('/history/<int:reading_id>')
    def reading_detail(reading_id):
        reading = TarotService.get_reading_by_id(reading_id)
        if not reading:
            return redirect(url_for('history'))
        return render_template('reading_detail.html', reading=reading)
    
    @app.route('/api/reading/<int:reading_id>', methods=['DELETE'])
    def delete_reading(reading_id):
        success = TarotService.delete_reading(reading_id)
        return jsonify({'success': success})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
