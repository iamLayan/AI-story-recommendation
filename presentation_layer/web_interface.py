# web_interface.py
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json

app = Flask(__name__)
API_GATEWAY_URL = "http://localhost:8080"  # رابط الـ API Gateway
app.secret_key = "secret123" 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    error = None
    if request.method == "POST":
        action = request.form.get("action")
        email = request.form["email"]
        password = request.form["password"]

        if action == "login":
            res = requests.post(f"{API_GATEWAY_URL}/login", json={
                "email": email,
                "password": password
            })
            if res.status_code == 200:
                user_data = res.json() 
                session["user_email"] = email
                return redirect(url_for("catalog"))
            else:
                error = "بيانات الدخول غير صحيحة"

        elif action == "register":
            username = request.form["username"]
            res = requests.post(f"{API_GATEWAY_URL}/register", json={
                "username": username,
                "email": email,
                "password": password
            })
            if res.status_code == 200:
                return redirect(url_for("user"))
            else:
                error = "فشل التسجيل: البريد موجود مسبقاً"

    return render_template("user.html", error=error)

@app.route("/catalog")
@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        genre = request.form["genre"]
        description = request.form["description"]

        # إرسال البيانات إلى الـ API Gateway
        res = requests.post(f"{API_GATEWAY_URL}/catalog", json={
            "title": title,
            "author": author,
            "genre": genre,
            "description": description
        })
        if res.status_code == 201:
            return redirect(url_for("catalog"))

    # 👇 هذا الجزء هو اللي يعرض القصص الموجودة
    res = requests.get(f"{API_GATEWAY_URL}/catalog")
    items = res.json() if res.status_code == 200 else []
    print("📚 Catalog items from API:", items)  # اطبعهم عشان تتأكد
    return render_template("catalog.html", items=items)


# حذف القصص
@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    requests.delete(f"{API_GATEWAY_URL}/catalog/{item_id}")
    return redirect(url_for("catalog"))
    
# @app.route("/recommendations", methods=["GET"])
# def recommendations():
#     res = requests.get(f"{API_GATEWAY_URL}/recommendations") 
#     items = res.json() if res.status_code == 200 else []
#     return render_template("recommendations.html", items=items)

@app.route("/recommendations", methods=["GET", "POST"])
def recommendations():
    story = None
    if request.method == "POST":
        prompt = request.form.get("prompt")
        story_type = request.form.get("type")

        res = requests.post(f"{API_GATEWAY_URL}/recommendations", json={
            "prompt": prompt,
            "type": story_type
        })

        if res.status_code == 200:
            story = res.json().get("story")

    return render_template("recommendations.html", story=story)
@app.route("/add_to_favorites", methods=['POST'])
def add_to_favorites():
    user_email = session.get("user_email")  # البريد للمستخدم الحالي
    if not user_email:
        return redirect(url_for("user"))

    story = request.form.get("story")

    # قراءة ملف المفضلات
    FAV_FILE = "data_layer/favorites.json"
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            favorites = json.load(f)
    except FileNotFoundError:
        favorites = {}

    # إضافة القصة تحت البريد
    if user_email not in favorites:
        favorites[user_email] = []

    if story not in favorites[user_email]:  # لتجنب التكرار
        favorites[user_email].append(story)

    # حفظ الملف
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(favorites, f, ensure_ascii=False, indent=4)

    return redirect(url_for("recommendations"))


if __name__ == "__main__":
   app.run(debug=True, port=5000) 
