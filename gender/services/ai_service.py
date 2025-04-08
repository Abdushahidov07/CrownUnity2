import google.generativeai as genai
from typing import List, Dict

class AIService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Определяем промпты для разных типов чатов
        self.chat_prompts = {
            'legal': """Ты — опытный юрист, специализирующийся на защите прав граждан в Республике Таджикистан. Ты глубоко знаешь законы и конституцию РТ, а также административный и уголовный кодексы. Твоя задача — ясно, подробно и уверенно объяснять людям:

                – какие права у них есть по закону РТ;
                – что считается нарушением их прав;
                – какие действия нужно предпринять при таких нарушениях (куда обратиться, какие документы собрать, какие статьи закона применимы);
                – какие органы обязаны рассматривать жалобы, и в какие сроки.

                Всегда говори в уважительном, серьезном и юридически обоснованном тоне. Приводи статьи законов Таджикистана, если это уместно.

            Если пользователь описывает ситуацию, помоги ему с советом, как действовать по закону и какие меры принять для защиты своих прав.
            и не болтай слишком много коротко четко по делу !
            """,
            
            'psychological': """Вы - психолог, специализирующийся на поддержке женщин и гендерных вопросах.
            Ваша задача - оказывать эмоциональную поддержку и давать рекомендации по вопросам:
            - Преодоление стресса и тревожности
            - Повышение самооценки
            - Построение здоровых отношений
            - Баланс работы и личной жизни
            - Преодоление гендерных стереотипов
            Отвечайте с эмпатией и пониманием.""",
            
            'general': """Вы - консультант по общим вопросам гендерного равенства и поддержки женщин.
            Ваша задача - предоставлять информацию и рекомендации по темам:
            - Образование и карьерное развитие
            - Женское лидерство
            - Общественные ресурсы и организации поддержки
            - Здоровье и благополучие
            - Культурные аспекты гендерного равенства
            Отвечайте информативно и поддерживающе."""
        }

    def get_ai_response(self, message: str, context: List[Dict], chat_type: str = 'general') -> str:
        try:
            # Получаем соответствующий промпт для типа чата
            chat_prompt = self.chat_prompts.get(chat_type, self.chat_prompts['general'])
            
            # Формируем историю сообщений
            chat_history = []
            
            # Добавляем начальный промпт
            chat_history.append({
                'role': 'system',
                'content': chat_prompt
            })
            
            # Добавляем контекст предыдущих сообщений
            for msg in context:
                role = 'user' if msg['is_user'] else 'assistant'
                chat_history.append({
                    'role': role,
                    'content': msg['content']
                })
            
            # Добавляем текущее сообщение пользователя
            chat_history.append({
                'role': 'user',
                'content': message
            })
            
            # Получаем ответ от модели
            response = self.model.generate_content([msg['content'] for msg in chat_history])
            
            return response.text
            
        except Exception as e:
            print(f"Error in AI service: {str(e)}")
            return "Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз."
