# business_logic_layer/catalog_service/factory.py

from .models import MediaItem

class MediaFactory:
    @staticmethod
    def create_media(id, title, author, genre, description):
        """ينشئ كائن وسائط جديد"""
        return MediaItem(id, title, author, genre, description)


