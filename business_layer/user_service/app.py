
from flask import Flask, request, jsonify
from business_layer.user_service.user_service import UserService

app = Flask(__name__)
user_service = UserService()

# تسجيل مستخدم جديد
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = user_service.register_user(data["username"], data["email"], data["password"])
    if user:
        return jsonify(user), 201
    return jsonify({"error": "User already exists"}), 400

# تسجيل الدخول
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = user_service.login_user(data["email"], data["password"])
    if user:
        return jsonify(user), 200
    return jsonify({"error": "Invalid credentials"}), 401

# عرض بيانات مستخدم
@app.route("/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5002)
