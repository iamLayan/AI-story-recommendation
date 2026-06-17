#يربط CatalogService بـ Flask API
from flask import Flask, jsonify, request
from business_layer.catalog_service.catalog_service import CatalogService

app = Flask(__name__)
catalog = CatalogService()

@app.route("/catalog", methods=["GET"])
def get_all():
    return jsonify(catalog.get_all_items()), 200

@app.route("/catalog/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = catalog.get_item(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/catalog", methods=["POST"])
def add_item():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400
    # تحقق من وجود الحقول المطلوبة
    required_fields = ["title", "author", "genre", "description"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_item = catalog.add_item(
        title=data["title"],
        author=data["author"],
        genre=data["genre"],
        description=data["description"]
    )
    return jsonify(new_item), 201

@app.route("/catalog/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    catalog.delete_item(item_id)
    return jsonify({"message": f"Item {item_id} deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
