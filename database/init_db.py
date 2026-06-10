from . import db
from .models import Card, Spread, SpreadPosition

MAJOR_ARCANA = [
    {"name": "愚者", "name_en": "The Fool", "number": 0, "upright": "新开始、冒险、天真、自由", "reversed": "鲁莽、冒失、犹豫不决", "desc": "愚者代表着新的开始和无限的可能性，象征着纯真和冒险精神。"},
    {"name": "魔术师", "name_en": "The Magician", "number": 1, "upright": "创造力、才能、意志力、自信", "reversed": "欺骗、缺乏自信、技能不足", "desc": "魔术师象征着将想法变为现实的能力，代表着创造力和行动力。"},
    {"name": "女祭司", "name_en": "The High Priestess", "number": 2, "upright": "直觉、潜意识、神秘、内在智慧", "reversed": "秘密、隐藏的动机、缺乏直觉", "desc": "女祭司代表着潜意识和直觉的力量，象征着内在的智慧和神秘。"},
    {"name": "女皇", "name_en": "The Empress", "number": 3, "upright": "丰收、母性、自然、富足", "reversed": "依赖、过度保护、创意受阻", "desc": "女皇象征着丰收和母性，代表着自然界的丰饶和创造力。"},
    {"name": "皇帝", "name_en": "The Emperor", "number": 4, "upright": "权威、结构、控制、稳定", "reversed": "专制、固执、缺乏纪律", "desc": "皇帝代表着权威和秩序，象征着稳定和结构的力量。"},
    {"name": "教皇", "name_en": "The Hierophant", "number": 5, "upright": "传统、教育、信仰、指导", "reversed": "打破常规、个人信念、反叛", "desc": "教皇象征着传统和精神指导，代表着信仰和教育的力量。"},
    {"name": "恋人", "name_en": "The Lovers", "number": 6, "upright": "爱情、和谐、关系、选择", "reversed": "失衡、冲突、错误的选择", "desc": "恋人代表着爱情和关系，象征着选择和和谐的重要性。"},
    {"name": "战车", "name_en": "The Chariot", "number": 7, "upright": "决心、胜利、意志力、前进", "reversed": "缺乏方向、失败、失控", "desc": "战车象征着决心和胜利，代表着通过意志力克服困难。"},
    {"name": "力量", "name_en": "Strength", "number": 8, "upright": "勇气、耐心、内在力量、同情", "reversed": "自我怀疑、软弱、缺乏自信", "desc": "力量代表着内在的勇气和耐心，象征着温柔而坚定的力量。"},
    {"name": "隐士", "name_en": "The Hermit", "number": 9, "upright": "独处、内省、智慧、指导", "reversed": "孤独、固执、逃避现实", "desc": "隐士象征着独处和内省，代表着通过沉思获得智慧。"},
    {"name": "命运之轮", "name_en": "Wheel of Fortune", "number": 10, "upright": "命运、转折点、运气、周期", "reversed": "坏运气、抗拒改变、破坏循环", "desc": "命运之轮代表着命运的转折和生命的周期，象征着变化和机遇。"},
    {"name": "正义", "name_en": "Justice", "number": 11, "upright": "公正、真理、因果、责任", "reversed": "不公正、逃避责任、偏见", "desc": "正义象征着公正和真理，代表着因果报应和责任。"},
    {"name": "倒吊人", "name_en": "The Hanged Man", "number": 12, "upright": "牺牲、放下、新视角、等待", "reversed": "拖延、抗拒、不必要的牺牲", "desc": "倒吊人代表着牺牲和放下，象征着从新角度看问题。"},
    {"name": "死神", "name_en": "Death", "number": 13, "upright": "结束、转变、新生、放手", "reversed": "抗拒改变、停滞、恐惧", "desc": "死神象征着结束和转变，代表着旧事物的终结和新事物的开始。"},
    {"name": "节制", "name_en": "Temperance", "number": 14, "upright": "平衡、耐心、适度、和谐", "reversed": "失衡、过度、缺乏耐心", "desc": "节制代表着平衡和适度，象征着耐心和和谐的重要性。"},
    {"name": "恶魔", "name_en": "The Devil", "number": 15, "upright": "束缚、物欲、阴暗面、成瘾", "reversed": "解脱、打破束缚、觉醒", "desc": "恶魔象征着束缚和物欲，代表着我们内心的阴暗面和成瘾。"},
    {"name": "塔", "name_en": "The Tower", "number": 16, "upright": "突变、破坏、觉醒、真相", "reversed": "逃避灾难、恐惧改变、延迟", "desc": "塔象征着突然的变化和破坏，代表着真相的揭示和觉醒。"},
    {"name": "星星", "name_en": "The Star", "number": 17, "upright": "希望、灵感、宁静、更新", "reversed": "绝望、缺乏信心、断开连接", "desc": "星星代表着希望和灵感，象征着宁静和更新的力量。"},
    {"name": "月亮", "name_en": "The Moon", "number": 18, "upright": "幻觉、恐惧、潜意识、直觉", "reversed": "释放恐惧、清晰、误解消除", "desc": "月亮象征着幻觉和潜意识，代表着直觉和内心的恐惧。"},
    {"name": "太阳", "name_en": "The Sun", "number": 19, "upright": "快乐、成功、活力、乐观", "reversed": "暂时的挫折、过度乐观、延迟", "desc": "太阳代表着快乐和成功，象征着活力和乐观的精神。"},
    {"name": "审判", "name_en": "Judgement", "number": 20, "upright": "觉醒、更新、召唤、反思", "reversed": "自我怀疑、拒绝召唤、逃避", "desc": "审判象征着觉醒和更新，代表着对人生的反思和召唤。"},
    {"name": "世界", "name_en": "The World", "number": 21, "upright": "完成、整合、成就、旅程结束", "reversed": "未完成、缺乏闭合、延迟", "desc": "世界代表着完成和成就，象征着旅程的圆满结束。"},
]

SUITS = {
    "权杖": {"en": "Wands", "theme": "行动、创造、激情"},
    "圣杯": {"en": "Cups", "theme": "情感、关系、直觉"},
    "宝剑": {"en": "Swords", "theme": "思想、冲突、真相"},
    "星币": {"en": "Pentacles", "theme": "物质、工作、财富"},
}

MINOR_CARDS = {
    "权杖": [
        {"name": "权杖王牌", "en": "Ace of Wands", "upright": "新起点、创造力、灵感", "reversed": "延迟、缺乏方向、创意受阻"},
        {"name": "权杖二", "en": "Two of Wands", "upright": "规划、决策、未来展望", "reversed": "缺乏规划、恐惧、犹豫"},
        {"name": "权杖三", "en": "Three of Wands", "upright": "拓展、远见、机遇", "reversed": "障碍、延迟、缺乏远见"},
        {"name": "权杖四", "en": "Four of Wands", "upright": "庆祝、和谐、家庭", "reversed": "不稳定、缺乏支持、过渡"},
        {"name": "权杖五", "en": "Five of Wands", "upright": "竞争、冲突、挑战", "reversed": "避免冲突、妥协、内斗"},
        {"name": "权杖六", "en": "Six of Wands", "upright": "胜利、认可、成功", "reversed": "失败、缺乏认可、自负"},
        {"name": "权杖七", "en": "Seven of Wands", "upright": "防御、坚持、挑战", "reversed": "放弃、压力、疲惫"},
        {"name": "权杖八", "en": "Eight of Wands", "upright": "快速行动、消息、进展", "reversed": "延迟、等待、混乱"},
        {"name": "权杖九", "en": "Nine of Wands", "upright": "坚韧、毅力、最后的努力", "reversed": "疲惫、放弃、过度防御"},
        {"name": "权杖十", "en": "Ten of Wands", "upright": "负担、责任、努力", "reversed": "释放、委托、减轻负担"},
        {"name": "权杖侍从", "en": "Page of Wands", "upright": "探索、热情、新想法", "reversed": "缺乏方向、延迟、不成熟"},
        {"name": "权杖骑士", "en": "Knight of Wands", "upright": "行动、冒险、冲动", "reversed": "鲁莽、延迟、缺乏耐心"},
        {"name": "权杖王后", "en": "Queen of Wands", "upright": "自信、独立、热情", "reversed": "自私、嫉妒、缺乏安全感"},
        {"name": "权杖国王", "en": "King of Wands", "upright": "领导力、远见、魅力", "reversed": "专制、冲动、缺乏远见"},
    ],
    "圣杯": [
        {"name": "圣杯王牌", "en": "Ace of Cups", "upright": "新感情、直觉、创造力", "reversed": "情感压抑、空虚、失去爱"},
        {"name": "圣杯二", "en": "Two of Cups", "upright": "伴侣、关系、和谐", "reversed": "分离、冲突、失去平衡"},
        {"name": "圣杯三", "en": "Three of Cups", "upright": "庆祝、友谊、社交", "reversed": "孤立、过度纵欲、 gossip"},
        {"name": "圣杯四", "en": "Four of Cups", "upright": "冥想、内省、不满", "reversed": "新机会、觉醒、行动"},
        {"name": "圣杯五", "en": "Five of Cups", "upright": "失落、悲伤、后悔", "reversed": "接受、前进、发现希望"},
        {"name": "圣杯六", "en": "Six of Cups", "upright": "怀旧、回忆、纯真", "reversed": "困在过去、不切实际、幼稚"},
        {"name": "圣杯七", "en": "Seven of Cups", "upright": "幻想、选择、想象", "reversed": "清晰、专注、现实"},
        {"name": "圣杯八", "en": "Eight of Cups", "upright": "放弃、寻求更深意义", "reversed": "恐惧改变、停滞、逃避"},
        {"name": "圣杯九", "en": "Nine of Cups", "upright": "满足、愿望成真、幸福", "reversed": "贪婪、不满、物质主义"},
        {"name": "圣杯十", "en": "Ten of Cups", "upright": "幸福、和谐、家庭", "reversed": "家庭问题、不和谐、破碎的梦想"},
        {"name": "圣杯侍从", "en": "Page of Cups", "upright": "创意、直觉、新感情", "reversed": "情绪不成熟、创意受阻"},
        {"name": "圣杯骑士", "en": "Knight of Cups", "upright": "浪漫、魅力、理想主义", "reversed": "不切实际、情绪化、嫉妒"},
        {"name": "圣杯王后", "en": "Queen of Cups", "upright": "同情心、直觉、情感智慧", "reversed": "情绪不稳定、依赖、 martyr"},
        {"name": "圣杯国王", "en": "King of Cups", "upright": "情感成熟、平衡、外交", "reversed": "情绪压抑、操控、冷漠"},
    ],
    "宝剑": [
        {"name": "宝剑王牌", "en": "Ace of Swords", "upright": "清晰、真相、突破", "reversed": "混乱、误解、缺乏清晰"},
        {"name": "宝剑二", "en": "Two of Swords", "upright": "决策、僵局、回避", "reversed": "信息过载、优柔寡断"},
        {"name": "宝剑三", "en": "Three of Swords", "upright": "心碎、悲伤、分离", "reversed": "释放痛苦、原谅、康复"},
        {"name": "宝剑四", "en": "Four of Swords", "upright": "休息、恢复、冥想", "reversed": "疲惫、不安、无法休息"},
        {"name": "宝剑五", "en": "Five of Swords", "upright": "冲突、失败、赢得不光彩", "reversed": "和解、放下、新开始"},
        {"name": "宝剑六", "en": "Six of Swords", "upright": "过渡、离开、前进", "reversed": "无法离开、困住、回溯"},
        {"name": "宝剑七", "en": "Seven of Swords", "upright": "欺骗、策略、逃避", "reversed": "坦白、面对真相、 accountability"},
        {"name": "宝剑八", "en": "Eight of Swords", "upright": "束缚、限制、无助", "reversed": "自由、新视角、解放"},
        {"name": "宝剑九", "en": "Nine of Swords", "upright": "焦虑、恐惧、噩梦", "reversed": "希望、光明、最坏的已过去"},
        {"name": "宝剑十", "en": "Ten of Swords", "upright": "结束、背叛、痛苦的终结", "reversed": "无法放手、延迟结束"},
        {"name": "宝剑侍从", "en": "Page of Swords", "upright": "好奇、警觉、新想法", "reversed": "缺乏计划、急躁、 gossip"},
        {"name": "宝剑骑士", "en": "Knight of Swords", "upright": "果断、行动、直接", "reversed": "鲁莽、冲动、缺乏耐心"},
        {"name": "宝剑王后", "en": "Queen of Swords", "upright": "独立、清晰、 direct", "reversed": "冷酷、尖刻、过于批判"},
        {"name": "宝剑国王", "en": "King of Swords", "upright": "权威、逻辑、公正", "reversed": "专制、冷酷、操控"},
    ],
    "星币": [
        {"name": "星币王牌", "en": "Ace of Pentacles", "upright": "新机会、财富、繁荣", "reversed": "错失机会、财务问题、缺乏计划"},
        {"name": "星币二", "en": "Two of Pentacles", "upright": "平衡、适应、多重任务", "reversed": "失衡、过度承担、组织混乱"},
        {"name": "星币三", "en": "Three of Pentacles", "upright": "团队合作、技能、 mastery", "reversed": "缺乏合作、平庸、缺乏技能"},
        {"name": "星币四", "en": "Four of Pentacles", "upright": "安全、保守、控制", "reversed": "贪婪、吝啬、过度执着"},
        {"name": "星币五", "en": "Five of Pentacles", "upright": "困难、贫穷、孤立", "reversed": "恢复、帮助、结束困难"},
        {"name": "星币六", "en": "Six of Pentacles", "upright": "慷慨、给予、分享", "reversed": "自私、债务、 strings attached"},
        {"name": "星币七", "en": "Seven of Pentacles", "upright": "耐心、投资、长期回报", "reversed": "缺乏耐心、即时满足、 impatience"},
        {"name": "星币八", "en": "Eight of Pentacles", "upright": "专注、技能、勤奋", "reversed": "缺乏 focus、平庸、重复"},
        {"name": "星币九", "en": "Nine of Pentacles", "upright": "独立、 luxury、成功", "reversed": "过度依赖、孤独、 superficial"},
        {"name": "星币十", "en": "Ten of Pentacles", "upright": "财富、家庭、遗产", "reversed": "家庭问题、财务不稳定、孤独"},
        {"name": "星币侍从", "en": "Page of Pentacles", "upright": "学习、机会、新技能", "reversed": "缺乏进展、不切实际、懒惰"},
        {"name": "星币骑士", "en": "Knight of Pentacles", "upright": "勤奋、可靠、 routine", "reversed": "停滞、缺乏动力、 perfectionism"},
        {"name": "星币王后", "en": "Queen of Pentacles", "upright": " practical、 nurturing、 abundance", "reversed": "过度担忧、物质主义、自我忽视"},
        {"name": "星币国王", "en": "King of Pentacles", "upright": "成功、 wealth、 stability", "reversed": "贪婪、固执、过度物质主义"},
    ],
}

SPREADS = [
    {
        "name": "单牌占卜",
        "description": "每日一牌，快速获取指引",
        "positions": 1,
        "layout_type": "single",
        "position_meanings": ["今日指引"]
    },
    {
        "name": "三牌阵",
        "description": "过去-现在-未来，了解事情发展",
        "positions": 3,
        "layout_type": "three_card",
        "position_meanings": ["过去", "现在", "未来"]
    },
    {
        "name": "爱情牌阵",
        "description": "探索感情问题的深层含义",
        "positions": 5,
        "layout_type": "love",
        "position_meanings": ["你的现状", "对方的心态", "关系的障碍", "建议行动", "可能的结果"]
    },
    {
        "name": "凯尔特十字牌阵",
        "description": "最经典的牌阵，全面解读复杂问题",
        "positions": 10,
        "layout_type": "celtic_cross",
        "position_meanings": ["当前处境", "挑战/交叉", "根源", "过去", "可能", "近期未来", "自我认知", "环境", "希望与恐惧", "最终结果"]
    },
    {
        "name": "马蹄牌阵",
        "description": "七张牌呈马蹄形，揭示运势走向",
        "positions": 7,
        "layout_type": "horseshoe",
        "position_meanings": ["过去", "现在", "未来", "你的态度", "环境影响", "希望与恐惧", "最终结果"]
    },
    {
        "name": "生命之树牌阵",
        "description": "卡巴拉生命之树，深度灵性探索",
        "positions": 10,
        "layout_type": "tree_of_life",
        "position_meanings": ["王冠", "智慧", "理解", "慈悲", "严厉", "和谐", "胜利", "荣耀", "基础", "王国"]
    },
    {
        "name": "事业牌阵",
        "description": "专注职场与事业发展的牌阵",
        "positions": 5,
        "layout_type": "career",
        "position_meanings": ["当前工作状态", "面临的挑战", "隐藏的机遇", "需要发展的能力", "事业前景"]
    },
]

def get_image_path(arcana, suit, number, name_en):
    if arcana == "大阿卡纳":
        return f"images/cards/major_{number:02d}_{name_en.replace(' ', '')}.jpg"
    else:
        suit_map = {"权杖": "wands", "圣杯": "cups", "宝剑": "swords", "星币": "pents"}
        suit_en = suit_map.get(suit, "unknown")
        card_num = number - {"权杖": 0, "圣杯": 14, "宝剑": 28, "星币": 42}.get(suit, 0)
        return f"images/cards/minor_{suit_en}_{card_num:02d}.jpg"

def init_database(app):
    with app.app_context():
        db.create_all()
        
        if Card.query.count() == 0:
            for card_data in MAJOR_ARCANA:
                card = Card(
                    name=card_data["name"],
                    name_en=card_data["name_en"],
                    number=card_data["number"],
                    arcana="大阿卡纳",
                    upright_meaning=card_data["upright"],
                    reversed_meaning=card_data["reversed"],
                    description=card_data["desc"],
                    image_path=get_image_path("大阿卡纳", None, card_data["number"], card_data["name_en"])
                )
                db.session.add(card)
            
            number = 1
            for suit, cards in MINOR_CARDS.items():
                for card_data in cards:
                    card = Card(
                        name=card_data["name"],
                        name_en=card_data["en"],
                        number=number,
                        arcana="小阿卡纳",
                        suit=suit,
                        upright_meaning=card_data["upright"],
                        reversed_meaning=card_data["reversed"],
                        description=f"{suit}代表{SUITS[suit]['theme']}",
                        image_path=get_image_path("小阿卡纳", suit, number, card_data["en"])
                    )
                    db.session.add(card)
                    number += 1
            
            for spread_data in SPREADS:
                spread = Spread(
                    name=spread_data["name"],
                    description=spread_data["description"],
                    positions=spread_data["positions"],
                    layout_type=spread_data["layout_type"]
                )
                db.session.add(spread)
                db.session.flush()
                
                for i, meaning in enumerate(spread_data["position_meanings"]):
                    position = SpreadPosition(
                        spread_id=spread.id,
                        position=i + 1,
                        meaning=meaning
                    )
                    db.session.add(position)
            
            db.session.commit()
            print("数据库初始化完成！")
        else:
            print("数据库已存在数据，跳过初始化。")
