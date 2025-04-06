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
        per_emb_threshold = 0.3  # Minimum similarity per embedding
        overall_threshold = 0.35  # Average of best matches required

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

        # Main match condition
        if best_match and best_score >= overall_threshold:
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

        # Fallback strategy: pick top single similarity match if nothing meets above criteria
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

        # If no match at all
        print("❌ No match found.")
        print("--- End of Debug Log ---\n")
        return jsonify({"success": False, "message": "No matching palm found."}), 404

    except Exception as e:
        print("❌ Error during palm match:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    

@app.route("/perform_transaction", methods=["POST"])
@cross_origin(supports_credentials=True)
def perform_transaction():
    data = request.get_json()
    user_id = data["user_id"]
    amount = float(data["amount"])
    owner_email = "admin@repulser.com"  # or get from data if needed

    user = users.find_one({"_id": ObjectId(user_id)})
    owner = users.find_one({"email": owner_email})

    if not user or not owner:
        return jsonify({"error": "User or owner not found"}), 404

    if user["balance"] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Update balances
    users.update_one({"_id": ObjectId(user_id)}, {"$inc": {"balance": -amount}})
    users.update_one({"email": owner_email}, {"$inc": {"balance": amount}})

    # Add transaction logs
    transaction = {
        "from": user["email"],
        "to": owner_email,
        "amount": amount,
        "timestamp": datetime.datetime.now(),
    }

    users.update_one({"_id": ObjectId(user_id)}, {"$push": {"transactions": transaction}})
    users.update_one({"email": owner_email}, {"$push": {"transactions": transaction}})

    return jsonify({"message": "Transaction successful"}), 200


# -------------------- Run Server ----------------------

if __name__ == "__main__":
    app.run(port=3001, debug=True)
