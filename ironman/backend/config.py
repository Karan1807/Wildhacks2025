from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from keras import Sequential


def build_model():
    input_shape = (224, 224, 3)
    inputs = Input(shape=input_shape)

    # Simple CNN base
    x = Conv2D(32, (3, 3), activation="relu")(inputs)
    x = MaxPooling2D()(x)
    x = Conv2D(64, (3, 3), activation="relu")(x)
    x = MaxPooling2D()(x)
    x = Flatten()(x)

    # Embedding layer (this is what we’ll extract for DB)
    embedding_output = Dense(128, activation="relu", name="dense_embedding")(x)

    # Final output layer for classification (you probably used this for training)
    output = Dense(1, activation="sigmoid")(embedding_output)

    # Full model (used in training)
    full_model = Model(inputs=inputs, outputs=output)

    # Embedding model (used during registration/matching)
    embedding_model = Model(inputs=inputs, outputs=embedding_output)

    return full_model, embedding_model
