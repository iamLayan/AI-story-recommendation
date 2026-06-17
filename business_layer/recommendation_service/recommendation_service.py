from business_layer.recommendation_service.strategies import BaseStoryStrategy, CreativeStoryStrategy

class RecommendationService:
    def __init__(self, strategy: BaseStoryStrategy = None):
        # استراتيجية افتراضية إذا ما تم تمرير واحدة
        self.strategy = strategy or CreativeStoryStrategy()

    def set_strategy(self, strategy: BaseStoryStrategy):
        """تغيير الاستراتيجية أثناء التشغيل"""
        self.strategy = strategy

    def generate_story(self, prompt: str):
        """ينفذ الاستراتيجية المختارة لتوليد القصة"""
        try:
            return self.strategy.generate(prompt)
        except Exception as e:
            return f"حدث خطأ أثناء توليد القصة: {e}"
