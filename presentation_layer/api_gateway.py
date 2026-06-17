# api_gateway.py
import requests
from requests.exceptions import RequestException
from flask import Flask, request, jsonify

app = Flask(__name__)

# روابط الميكروسيرفيسز 
USER_SERVICE_URL = "http://localhost:5002"
CATALOG_SERVICE_URL = "http://localhost:5001"
RECOMM_SERVICE_URL = "http://localhost:5003"

REQUEST_TIMEOUT = 3  # ثواني

# =====================================================
# دوال مساعدة عامة للـ GET / POST / DELETE
# =====================================================
def proxy_post(url, json_data):
    try:
        res = requests.post(url, json=json_data, timeout=REQUEST_TIMEOUT)
        return jsonify(res.json()), res.status_code
    except RequestException as e:
        return jsonify({"error": "Service unavailable", "details": str(e)}), 503


def proxy_get(url):
    try:
        res = requests.get(url, timeout=REQUEST_TIMEOUT)
        return jsonify(res.json()), res.status_code
    except RequestException as e:
        return jsonify({"error": "Service unavailable", "details": str(e)}), 503


def proxy_delete(url):
    try:
        res = requests.delete(url, timeout=REQUEST_TIMEOUT)
        return jsonify(res.json()), res.status_code
    except RequestException as e:
        return jsonify({"error": "Service unavailable", "details": str(e)}), 503


# =====================================================
# 🧍‍♀️ User Service
# =====================================================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return jsonify({"message": "Use POST to log in."})
    data = request.json
    return proxy_post(f"{USER_SERVICE_URL}/login", data)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return jsonify({"message": "Use POST to register."})
    data = request.json
    return proxy_post(f"{USER_SERVICE_URL}/register", data)

# =====================================================
# 📚 Catalog Service
# =====================================================
@app.route("/catalog", methods=["GET"])
def get_catalog():
    """عرض جميع القصص"""
    return proxy_get(f"{CATALOG_SERVICE_URL}/catalog")


@app.route("/catalog", methods=["POST"])
def add_catalog_item():
    """إضافة قصة جديدة"""
    data = request.json
    return proxy_post(f"{CATALOG_SERVICE_URL}/catalog", data)


@app.route("/catalog/<int:item_id>", methods=["DELETE"])
def delete_catalog_item(item_id):
    """حذف قصة"""
    return proxy_delete(f"{CATALOG_SERVICE_URL}/catalog/{item_id}")

# =====================================================
# 🤖 Recommendation Service
# =====================================================
@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    try:
        data = request.json
        response = requests.post(f"{RECOMM_SERVICE_URL}/recommend", json=data, timeout=REQUEST_TIMEOUT)
        return jsonify(response.json()), response.status_code
    except RequestException as e:
        return jsonify({"error": "Recommendation service unavailable", "details": str(e)}), 503
        
# =====================================================
# 🚀 Main
# =====================================================
if __name__ == "__main__":
    print("API Gateway running on port 8080 ...")
    app.run(debug=True, port=8080)
