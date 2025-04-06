from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

# Initialize app
app = Flask(__name__)

# Enable CORS for specific frontend origin
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# MongoDB setup — replace with your own connection string
client = MongoClient(
    "mongodb+srv://repulser_user:aFY09Gs2v9LHmI3Q@cluster0.y0alncz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["repulser"]
users = db["users"]

# -------------------- Routes ----------------------


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    existing_user = users.find_one({"email": data["email"]})
    if existing_user:
        return jsonify({"error": "User already exists"}), 409

    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],  # 🔐 You can hash this later
        "role": data["role"],  # 'user' or 'business'
        "balance": 5000,
        "embeddings": [],
    }

    users.insert_one(new_user)
    return jsonify({"message": "User registered successfully"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    if not user or user["password"] != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    user_data = {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "balance": user["balance"],
    }
    return jsonify(user_data), 200


# -------------------- Run Server ----------------------

if __name__ == "__main__":
    app.run(port=3001, debug=True)
