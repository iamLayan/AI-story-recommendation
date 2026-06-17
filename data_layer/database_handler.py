import json
import os

class DatabaseHandlerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandlerSingleton, cls).__new__(cls)
        return cls._instance

    def read_data(self, filepath):
        """قراءة البيانات من ملف JSON"""
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def write_data(self, filepath, data):
        """كتابة البيانات إلى ملف JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
