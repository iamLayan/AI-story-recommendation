# business_logic_layer/catalog_service/models.py
#الذي يمثل القصة أو المادة الرقمية.
class MediaItem:
    def __init__(self, id, title, author, genre, description):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description
# لتحويل الكائن إلى JSON.
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "genre": self.genre,
            "description": self.description
        }
