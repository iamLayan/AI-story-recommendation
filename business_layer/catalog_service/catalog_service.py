# business_logic_layer/catalog_service/catalog_service.py

import os
from data_layer.database_handler import DatabaseHandlerSingleton
from .factory import MediaFactory

# مسار مطلق للـ JSON لتجنب مشاكل المسار عند تشغيل السيرفر
CATALOG_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../data_layer/catalog_data.json")
)

class CatalogService:
    def __init__(self):
        # إنشاء نسخة Singleton للقراءة والكتابة على JSON
        self.db = DatabaseHandlerSingleton()
        self.media_catalog = self.db.read_data(CATALOG_FILE)

    def get_all_items(self):
        """عرض جميع القصص"""
        return self.media_catalog

    def get_item(self, item_id):
        """عرض قصة واحدة حسب الـ id"""
        for item in self.media_catalog:
            if item["id"] == item_id:
                return item
        return None

    def add_item(self, title, author, genre, description):
        """إضافة قصة جديدة باستخدام Factory Pattern"""
        new_id = len(self.media_catalog) + 1
        # 🏭 هنا نستخدم المصنع بدلاً من إنشاء الكائن مباشرة
        new_item = MediaFactory.create_media(new_id, title, author, genre, description)
        self.media_catalog.append(new_item.to_dict())
        # حفظ البيانات بعد الإضافة
        self.db.write_data(CATALOG_FILE, self.media_catalog)
        return new_item.to_dict()

    def delete_item(self, item_id):
        """حذف قصة حسب الـ id"""
        self.media_catalog = [i for i in self.media_catalog if i["id"] != item_id]
        # حفظ التغييرات بعد الحذف
        self.db.write_data(CATALOG_FILE, self.media_catalog)
