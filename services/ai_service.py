import os
from openai import OpenAI

class AIService:
    def __init__(self):
        mimo_key = os.getenv('MIMO_API_KEY', '')
        mimo_base = os.getenv('MIMO_BASE_URL', 'https://api.siliconflow.cn/v1')
        openai_key = os.getenv('OPENAI_API_KEY', '')

        if mimo_key:
            self.client = OpenAI(api_key=mimo_key, base_url=mimo_base)
            self.model = os.getenv('MIMO_MODEL', 'XiaomiMiMo/MiMo-7B-RL')
            self.provider = 'mimo'
        elif openai_key:
            self.client = OpenAI(api_key=openai_key)
            self.model = 'gpt-3.5-turbo'
            self.provider = 'openai'
        else:
            self.client = None
            self.model = None
            self.provider = None

    def _has_api(self):
        return self.client is not None and self.client.api_key

    def generate_reading(self, cards, question=None, spread_name=None):
        if not self._has_api():
            return self._generate_fallback_reading(cards, question, spread_name)

        prompt = self._build_prompt(cards, question, spread_name)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI解读失败: {e}")
            return self._generate_fallback_reading(cards, question, spread_name)

    def generate_reading_stream(self, cards, question=None, spread_name=None):
        if not self._has_api():
            yield self._generate_fallback_reading(cards, question, spread_name)
            return

        prompt = self._build_prompt(cards, question, spread_name)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"AI流式解读失败: {e}")
            yield self._generate_fallback_reading(cards, question, spread_name)

    def chat_stream(self, messages):
        if not self._has_api():
            yield "AI 对话功能暂不可用，请在 .env 文件中配置 MIMO_API_KEY。"
            return

        system_msg = {
            "role": "system",
            "content": self._get_chat_system_prompt()
        }
        full_messages = [system_msg] + messages

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=0.7,
                max_tokens=800,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"AI对话失败: {e}")
            yield f"抱歉，AI 服务暂时不可用（{self.provider}）。请稍后再试。"

    def _get_chat_system_prompt(self):
        return """你是一位资深塔罗牌解读师，正在与用户进行一对一的深度对话。用户刚完成了一次塔罗占卜，现在想要进一步探讨。

你的角色：
- 用温暖、专业的方式回答用户关于塔罗牌的疑问
- 可以深入解读某张牌的含义、象征、历史
- 可以结合用户的实际情况给出建议
- 可以解释牌与牌之间的关系
- 保持积极建设性的态度，但不回避挑战性牌面的警示

对话风格：
- 简洁有力，不要过于冗长
- 用"你"称呼用户，保持亲切感
- 适当使用比喻和意象
- 每次回答控制在200字以内"""

    def _get_system_prompt(self):
        return """你是一位经验丰富、富有洞察力的塔罗牌解读师。你的解读风格温暖、富有启发性，能够将塔罗牌的象征意义与用户的实际情况相结合。

解读要求：
1. 首先总结整体牌面的能量和主题
2. 逐一解读每张牌在其位置上的含义
3. 分析牌与牌之间的关系和故事
4. 结合用户的问题给出具体的建议和指引
5. 保持积极、建设性的语气，即使出现挑战性牌面也要指出成长的机会
6. 使用诗意但不失专业的语言

请注意：
- 如果牌是逆位，需要解读逆位的含义
- 要考虑每张牌在牌阵中位置的特殊含义
- 给出的建议要具体可行
- 整体解读要有逻辑性和连贯性

格式要求（重要）：
- 使用 Markdown 格式，用 ### 作为小标题
- 用 **加粗** 强调关键词
- 用 - 或数字列表呈现要点
- 每行开头不要缩进或添加空格
- 段落之间用空行分隔"""

    def _build_prompt(self, cards, question, spread_name):
        prompt = f"牌阵类型：{spread_name}\n"
        if question:
            prompt += f"用户问题：{question}\n"
        prompt += "\n抽到的牌：\n"

        for card_info in cards:
            card = card_info['card']
            is_reversed = card_info['is_reversed']
            position_meaning = card_info.get('position_meaning', '')

            orientation = "逆位" if is_reversed else "正位"
            meaning = card['reversed_meaning'] if is_reversed else card['upright_meaning']

            prompt += f"- 位置{card_info['position']}（{position_meaning}）：{card['name']}（{card['name_en']}）{orientation}\n"
            prompt += f"  牌义：{meaning}\n"

        prompt += "\n请根据以上信息进行详细的塔罗牌解读。"
        return prompt

    def _generate_fallback_reading(self, cards, question, spread_name):
        if len(cards) == 1:
            card = cards[0]
            orientation = "逆位" if card['is_reversed'] else "正位"
            meaning = card['card']['reversed_meaning'] if card['is_reversed'] else card['card']['upright_meaning']
            return f"【{card['card']['name']} - {orientation}】\n\n{meaning}\n\n这是今日给你的指引，希望你能从中获得启发。"

        reading = f"【{spread_name}解读】\n\n"
        if question:
            reading += f"关于你的问题「{question}」，牌面给出了以下指引：\n\n"

        reading += "整体来看，这组牌展示了一个关于"

        themes = []
        for card_info in cards:
            card = card_info['card']
            if card['arcana'] == '大阿卡纳':
                themes.append('重要人生课题')
                break
            elif card['suit'] == '权杖':
                themes.append('行动与创造')
            elif card['suit'] == '圣杯':
                themes.append('情感与关系')
            elif card['suit'] == '宝剑':
                themes.append('思考与决策')
            elif card['suit'] == '星币':
                themes.append('物质与成长')

        if themes:
            reading += f"「{themes[0]}」的故事。\n\n"

        for card_info in cards:
            card = card_info['card']
            is_reversed = card_info['is_reversed']
            position_meaning = card_info.get('position_meaning', f'位置{card_info["position"]}')

            orientation = "逆位" if is_reversed else "正位"
            meaning = card['reversed_meaning'] if is_reversed else card['upright_meaning']

            reading += f"【{position_meaning}】{card['name']}（{orientation}）\n{meaning}\n\n"

        reading += "综合来看，牌面提醒你保持觉察，相信自己的直觉，勇敢面对生活中的变化与挑战。"

        return reading

ai_service = AIService()
