import unittest
from business_layer.user_service.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        # إنشاء كائن الخدمة قبل كل اختبار
        self.service = UserService()
        # تنظيف قائمة المستخدمين قبل كل اختبار
        self.service.users = []

    def test_register_user_success(self):
        user = self.service.register_user("ali", "ali@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "ali")
        self.assertEqual(len(self.service.users), 1)

    def test_register_user_duplicate_email(self):
        self.service.register_user("ali", "ali@example.com", "1234")
        user = self.service.register_user("moh", "ali@example.com", "5678")
        self.assertIsNone(user)  # لا يجب السماح بتكرار البريد

    def test_login_user_success(self):
        self.service.register_user("ali", "ali@example.com", "1234")
        user = self.service.login_user("ali@example.com", "1234")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "ali")

    def test_login_user_wrong_password(self):
        self.service.register_user("ali", "ali@example.com", "1234")
        user = self.service.login_user("ali@example.com", "wrongpass")
        self.assertIsNone(user)

    def test_get_user(self):
        user = self.service.register_user("ali", "ali@example.com", "1234")
        found = self.service.get_user(user["user_id"])
        self.assertIsNotNone(found)
        self.assertEqual(found["email"], "ali@example.com")

if __name__ == "__main__":
    unittest.main()
