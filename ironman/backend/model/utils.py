# model/utils.py

import cv2
import numpy as np

def preprocess_image(image):
    # image: raw np.array
    image = image.astype("float32") / 255.0
    return image  # shape should be (224, 224, 3)

def extract_embedding(image, embedding_model):
    preprocessed = preprocess_image(image)
    # REMOVE the extra dimension here:
    embedding = embedding_model.predict(np.expand_dims(preprocessed, axis=0))[0]
    return embedding
