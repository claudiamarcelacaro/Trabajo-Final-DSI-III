import joblib
import os
import numpy as np

def model_fn(model_dir):
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    return model

def predict_fn(input_object, model):
    if np.ndim(input_object) == 1:
        input_object = np.expand_dims(input_object, axis = 0)
    y_hay = model.predict(input_object)
    return y_hay
