# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin
# from pymongo import MongoClient
# from tensorflow.keras.models import load_model
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np
# import base64
# from PIL import Image
# from io import BytesIO
# import os
# from dotenv import load_dotenv
# from model.utils import preprocess_image, extract_embedding
# from config import build_model
# import cv2


# # Load environment variables
# load_dotenv()

# # Initialize Flask app
# app = Flask(__name__)
# # CORS setup
# CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# # MongoDB connection
# MONGO_URI = os.getenv("MONGO_URI")
# client = MongoClient(MONGO_URI)
# db = client["repulser"]
# users = db["users"]
# embeddings_collection = db["embeddings"]

# # Load models
# model, embedding_model = build_model()


# # Utility: Decode base64 image to numpy array
# def decode_image(image_data_url):
#     image_data = image_data_url.split(",")[1]
#     decoded = base64.b64decode(image_data)
#     image = Image.open(BytesIO(decoded)).resize((224, 224))
#     return np.array(image)


# # -------------------- Routes ----------------------

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     user = users.find_one({"email": data["email"]})

#     if not user or user["password"] != data["password"]:
#         return jsonify({"error": "Invalid credentials"}), 401

#     user_data = {
#         "id": str(user["_id"]),
#         "name": user["name"],
#         "email": user["email"],
#         "role": user["role"],
#         "balance": user.get("balance", 0),
#     }
#     return jsonify(user_data), 200


# @app.route("/register_with_palm", methods=["POST"])
# @cross_origin(supports_credentials=True, origins="http://localhost:5173")
# def register_with_palm():
#     data = request.get_json()

#     name = data["name"]
#     email = data["email"]
#     password = data["password"]
#     role = data["role"]
#     palm_images = data["palm_images"]

#     # Process and generate embeddings
#     embeddings = []
#     for img in palm_images:
#         img_arr = decode_image(img)
#         embedding = extract_embedding(img_arr, embedding_model)
#         embeddings.append(embedding.tolist())

#     # Save everything in one user document
#     user_doc = {
#         "name": name,
#         "email": email,
#         "password": password,
#         "role": role,
#         "balance": 1000,
#         "embeddings": embeddings,
#     }

#     users.insert_one(user_doc)

#     return jsonify({"message": "Registered user + palm embeddings successfully!"}), 200

# @app.route('/match_palm', methods=['POST'])
# @cross_origin(supports_credentials=True, origins="http://localhost:5173")

# def match_palm():
#     data = request.get_json()
#     img_base64 = data['image']

#     try:
#         # Decode base64 image
#         img_data = base64.b64decode(img_base64.split(',')[1])
#         img_arr = np.frombuffer(img_data, np.uint8)
#         img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

#         # ✅ Resize image to model input size (224x224)
#         img = cv2.resize(img, (224, 224))

#         # Extract normalized embedding from the image
#         embedding = extract_embedding(img, embedding_model)
#         embedding = embedding / np.linalg.norm(embedding)

#         # Search through all user embeddings in MongoDB
#         users = users_collection.find()
#         best_match = None
#         best_similarity = 0
#         threshold = 0.99  # Adjust this threshold based on accuracy tests

#         for user in users:
#             stored_embeddings = user.get('embeddings', [])
#             for stored_emb in stored_embeddings:
#                 stored_emb = np.array(stored_emb)
#                 stored_emb = stored_emb / np.linalg.norm(stored_emb)
#                 similarity = cosine_similarity([embedding], [stored_emb])[0][0]

#                 if similarity > best_similarity:
#                     best_similarity = similarity
#                     best_match = user

#         # Return user info if a match was found above the threshold
#         if best_match and best_similarity >= threshold:
#             return jsonify({
#                 "success": True,
#                 "user": {
#                     "id": str(best_match["_id"]),
#                     "name": best_match["name"],
#                     "email": best_match["email"],
#                     "balance": best_match["balance"]
#                 },
#                 "similarity": best_similarity
#             }), 200
#         else:
#             return jsonify({
#                 "success": False,
#                 "message": "No matching palm found."
#             }), 404

#     except Exception as e:
#         print("Error during palm match:", e)
#         return jsonify({
#             "success": False,
#             "error": str(e)
#         }), 500


# # -------------------- Run Server ----------------------

# if __name__ == "__main__":
#     app.run(port=3001, debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import base64
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv
from model.utils import preprocess_image, extract_embedding
from config import build_model
import cv2
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# CORS setup
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["repulser"]
users = db["users"]
transactions_collection = db["transactions"]  # ✅ add this line

# Load models
model, embedding_model = build_model()


# Utility: Decode base64 image to numpy array
def decode_image(image_data_url):
    image_data = image_data_url.split(",")[1]
    decoded = base64.b64decode(image_data)
    image = Image.open(BytesIO(decoded)).resize((224, 224))
    return np.array(image)


# -------------------- Routes ----------------------


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
        "balance": user.get("balance", 0),
    }
    return jsonify(user_data), 200


# @app.route("/register_with_palm", methods=["POST"])
# @cross_origin(supports_credentials=True, origins="http://localhost:5173")
# def register_with_palm():
#     data = request.get_json()

#     name = data["name"]
#     email = data["email"]
#     password = data["password"]
#     role = data["role"]
#     palm_images = data["palm_images"]

#     # Process and generate embeddings
#     embeddings = []
#     for img in palm_images:
#         img_arr = decode_image(img)
#         embedding = extract_embedding(img_arr, embedding_model)
#         embeddings.append(embedding.tolist())

#     # Save everything in one user document
#     user_doc = {
#         "name": name,
#         "email": email,
#         "password": password,
#         "role": role,
#         "balance": 1000,
#         "embeddings": embeddings,
#     }

#     users.insert_one(user_doc)


#     return jsonify({"message": "Registered user + palm embeddings successfully!"}), 200
@app.route("/register_with_palm", methods=["POST"])
@cross_origin(supports_credentials=True, origins="http://localhost:5173")
def register_with_palm():
    data = request.get_json()

    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]
    palm_images = data["palm_images"]

    embeddings = []

    for img in palm_images:
        # Decode image
        img_arr = decode_image(img)  # This should return a (224, 224, 3) numpy array

        # Extract embedding from model
        embedding = extract_embedding(img_arr, embedding_model)

        # Normalize embedding vector
        norm = np.linalg.norm(embedding)
        if norm == 0:
            normalized_embedding = embedding
        else:
            normalized_embedding = embedding / norm

        # Store as list (MongoDB cannot store numpy arrays)
        embeddings.append(normalized_embedding.tolist())

    # Save user document in MongoDB
    user_doc = {
        "name": name,
        "email": email,
        "password": password,
        "role": role,
        "balance": 1000,
        "embeddings": embeddings,
    }

    users.insert_one(user_doc)

    return jsonify({"message": "Registered user + palm embeddings successfully!"}), 200


from flask import request, jsonify, session
from flask_cors import cross_origin
import base64
import numpy as np
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from bson import ObjectId

app.secret_key = "JAIMATAJIIIIIIIIIIIIII"


@app.route("/match_palm", methods=["POST"])
@cross_origin(supports_credentials=True, origins="http://localhost:5173")
def match_palm():
    data = request.get_json()
    img_base64 = data["image"]

    try:
        # Decode base64 image
        img_data = base64.b64decode(img_base64.split(",")[1])
        img_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        # Resize and preprocess image
        img = cv2.resize(img, (224, 224))
        embedding = extract_embedding(img, embedding_model)
        embedding = embedding / np.linalg.norm(embedding)

        # Thresholds
        per_emb_threshold = 0.3
        overall_threshold = 0.35

        best_match = None
        best_score = 0

        print("\n--- Palm Match Debug Log ---")
        for user in users.find():
            match_count = 0
            total_similarity = 0
            user_name = user.get("name")
            stored_embeddings = user.get("embeddings", [])

            for i, stored_emb in enumerate(stored_embeddings):
                stored_emb = np.array(stored_emb)
                stored_emb = stored_emb / np.linalg.norm(stored_emb)
                similarity = cosine_similarity([embedding], [stored_emb])[0][0]

                print(
                    f"User: {user_name}, Embedding #{i+1}, Similarity: {similarity:.6f}"
                )

                if similarity >= per_emb_threshold:
                    match_count += 1
                    total_similarity += similarity

            if match_count >= 3:
                avg_similarity = total_similarity / match_count
                print(
                    f"→ Valid avg similarity for {user_name}: {avg_similarity:.6f} from {match_count} matches"
                )

                if avg_similarity > best_score:
                    best_score = avg_similarity
                    best_match = user

        if best_match and best_score >= overall_threshold:
            session["matched_user_id"] = str(
                best_match["_id"]
            )  # ✅ Store matched user for transaction
            print(f"\nBEST MATCH → User: {best_match['name']}, Score: {best_score:.6f}")
            print("--- End of Debug Log ---\n")
            return (
                jsonify(
                    {
                        "success": True,
                        "user": {
                            "id": str(best_match["_id"]),
                            "name": best_match["name"],
                            "email": best_match["email"],
                            "balance": best_match["balance"],
                        },
                        "similarity": best_score,
                        "fallback": False,
                    }
                ),
                200,
            )

        # Fallback strategy
        print("\n--- Fallback Check ---")
        fallback_best_user = None
        fallback_best_similarity = 0

        for user in users.find():
            user_name = user.get("name")
            for i, stored_emb in enumerate(user["embeddings"]):
                stored_emb = np.array(stored_emb)
                stored_emb = stored_emb / np.linalg.norm(stored_emb)
                similarity = cosine_similarity([embedding], [stored_emb])[0][0]

                print(
                    f"Fallback: User: {user_name}, Embedding #{i+1}, Similarity: {similarity:.6f}"
                )

                if similarity > fallback_best_similarity:
                    fallback_best_similarity = similarity
                    fallback_best_user = user

        if fallback_best_user and fallback_best_similarity > 0.30:
            session["matched_user_id"] = str(
                fallback_best_user["_id"]
            )  # ✅ Store fallback match
            print(
                f"\nFALLBACK MATCH → User: {fallback_best_user['name']}, Score: {fallback_best_similarity:.6f}"
            )
            print("--- End of Debug Log ---\n")
            return (
                jsonify(
                    {
                        "success": True,
                        "user": {
                            "id": str(fallback_best_user["_id"]),
                            "name": fallback_best_user["name"],
                            "email": fallback_best_user["email"],
                            "balance": fallback_best_user["balance"],
                        },
                        "similarity": fallback_best_similarity,
                        "fallback": True,
                    }
                ),
                200,
            )

        print("❌ No match found.")
        print("--- End of Debug Log ---\n")
        return jsonify({"success": False, "message": "No matching palm found."}), 404

    except Exception as e:
        print("❌ Error during palm match:", e)
        return jsonify({"success": False, "error": str(e)}), 500
 
from bson.objectid import ObjectId
from bson.errors import InvalidId

@app.route("/receive_money", methods=["POST"])
@cross_origin(supports_credentials=True, origins="http://localhost:5173")
def receive_money():
    data = request.get_json()
    print("Received transaction data:", data)

    if not data:
        return jsonify({"error": "No data received"}), 400

    receiver_id = data.get("receiverId")
    sender_id = data.get("senderId")

    try:
        amount = float(data.get("amount"))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400

    if not receiver_id or not sender_id:
        return jsonify({"error": "Missing sender or receiver ID"}), 400

    try:
        sender = users.find_one({"_id": ObjectId(sender_id)})
        receiver = users.find_one({"_id": ObjectId(receiver_id)})
    except InvalidId:
        return jsonify({"error": "Invalid sender or receiver ID format"}), 400

    if not sender or not receiver:
        return jsonify({"error": "Sender or receiver not found"}), 404

    if sender["_id"] == receiver["_id"]:
        return jsonify({"error": "You can't send money to yourself"}), 400

    if sender["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Perform transaction
    users.update_one({"_id": ObjectId(sender_id)}, {"$inc": {"balance": -amount}})
    users.update_one({"_id": ObjectId(receiver_id)}, {"$inc": {"balance": amount}})

    transactions_collection.insert_one({
        "from": sender_id,
        "to": receiver_id,
        "amount": amount,
    })

    return jsonify({
        "message": "Transaction successful",
        "from": sender.get("name", "Unknown Sender"),
        "to": receiver.get("name", "Unknown Receiver"),
        "amount": amount
    }), 200


@app.route("/get_user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "_id": str(user["_id"]),
            "name": user["name"],
            "balance": user["balance"],
            "transactions": user.get("transactions", [])
        })
    except Exception as e:
        print("Error in /get_user:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/get_transactions/<user_id>", methods=["GET"])
def get_transactions(user_id):
    transactions = list(db.transactions.find({
        "$or": [
            {"sender_id": user_id},
            {"receiver_id": user_id}
        ]
    }).sort("timestamp", -1))  # Optional: sort by latest

    for txn in transactions:
        txn["_id"] = str(txn["_id"])

    return jsonify(transactions)


# -------------------- Run Server ----------------------

if __name__ == "__main__":
    app.run(port=3001, debug=True)
