import unittest
from unittest.mock import patch
from business_layer.recommendation_service.recommendation_service import RecommendationService
from business_layer.recommendation_service.strategies import CreativeStoryStrategy

class TestRecommendationService(unittest.TestCase):

    @patch.object(CreativeStoryStrategy, 'generate')
    def test_generate_story_success(self, mock_generate):
        # نجهز الـ mock للـ AI لتجنب استدعاء Groq الفعلي
        mock_generate.return_value = "هذه قصة اختبارية"
        service = RecommendationService()
        story = service.generate_story("فكرة القصة")
        self.assertEqual(story, "هذه قصة اختبارية")

    @patch.object(CreativeStoryStrategy, 'generate')
    def test_generate_story_error(self, mock_generate):
        # نجهز الـ mock ليرمي استثناء
        mock_generate.side_effect = Exception("API Error")
        service = RecommendationService()
        story = service.generate_story("فكرة القصة")
        self.assertIn("حدث خطأ أثناء توليد القصة", story)

if __name__ == "__main__":
    unittest.main()
