from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# استيراد الخدمات والأنماط
from business_layer.catalog_service.catalog_service import CatalogService
from business_layer.recommendation_service.recommendation_service import RecommendationService
from business_layer.recommendation_service.strategies import (
    BaseStoryStrategy, 
    CreativeStoryStrategy, 
    MoralStoryStrategy, 
    HorrorStoryStrategy
)

import os
app = Flask(__name__)
CORS(app)

# الخدمات
catalog_service = CatalogService()

# توليد قصة باستخدام الذكاء الاصطناعي (API مباشر)
@app.route("/story", methods=["POST"])
def get_story():
    """يولّد قصة جديدة بالذكاء الاصطناعي مباشرة بدون اختيار نوع"""
    data = request.get_json()
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "يرجى إدخال نص القصة أولاً"}), 400

    # استخدام استراتيجية افتراضية (إبداعية)
    strategy = CreativeStoryStrategy()
    ai_service = RecommendationService(strategy)

    story = ai_service.generate_story(prompt)
    return jsonify({"story": story}), 200

# Route خاص بالـ Strategy Pattern (واجهة اختيار نوع القصة)
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    data = request.json
    prompt = data.get("prompt", "")
    story_type = data.get("type", "creative")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # اختيار نوع القصة بناءً على المدخل
    if story_type == "moral":
        strategy = MoralStoryStrategy()
    elif story_type == "horror":
        strategy = HorrorStoryStrategy()
    else:
        strategy = CreativeStoryStrategy()

    recommendation = RecommendationService(strategy)
    story = recommendation.generate_story(prompt)
    return jsonify({"story": story})

    
# عرض كل القصص من الكتالوج
@app.route("/catalog", methods=["GET"])
def get_catalog():
    items = catalog_service.get_all_items()
    return jsonify(items), 200

# تشغيل السيرفر
if __name__ == "__main__":
    print("Recommendation Service running with Strategy Pattern (AI Integrated)")
    app.run(port=5003, debug=True)
