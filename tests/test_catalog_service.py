# tests/test_catalog_service.py
import unittest
from business_layer.catalog_service.catalog_service import CatalogService

class TestCatalogService(unittest.TestCase):
    def setUp(self):
        self.catalog = CatalogService()
        self.catalog.media_catalog = []

    def test_add_item(self):
        item = self.catalog.add_item("عنوان", "مؤلف", "قصة", "وصف")
        self.assertEqual(item["title"], "عنوان")
        self.assertEqual(len(self.catalog.media_catalog), 1)

    def test_get_item(self):
        item = self.catalog.add_item("عنوان", "مؤلف", "قصة", "وصف")
        found = self.catalog.get_item(item["id"])
        self.assertEqual(found["title"], "عنوان")

    def test_delete_item(self):
        item = self.catalog.add_item("عنوان", "مؤلف", "قصة", "وصف")
        self.catalog.delete_item(item["id"])
        self.assertEqual(len(self.catalog.media_catalog), 0)

if __name__ == "__main__":
    unittest.main()
