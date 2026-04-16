import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras import Input


def train_models():
    df = pd.read_csv("data.csv")

    X = df.drop("target", axis=1)
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ---------------- ML MODEL ----------------
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)

    # ---------------- DL MODEL ----------------
    model = Sequential()
    model.add(Input(shape=(X.shape[1],)))   # ✅ FIXED
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(X_train, y_train, epochs=10, verbose=0)

    return rf, model


def predict_models(rf, dl, input_data):
    input_array = np.array(input_data)   # ✅ FIXED

    rf_pred = rf.predict(input_array)[0]
    dl_pred = dl.predict(input_array)[0][0]

    return rf_pred, float(dl_pred)