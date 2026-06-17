class Recommendation:
    def __init__(self, user_id, suggested_items):
        self.user_id = user_id
        self.suggested_items = suggested_items

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "suggested_items": self.suggested_items
        }
