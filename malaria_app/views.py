from django.shortcuts import render, redirect
import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Path to your model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'cnn_model.h5')

# Load the model
try:
    model = tf.keras.models.load_model(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

def preprocess_image(file):
    """
    Preprocess the uploaded image for prediction.
    """
    image = Image.open(file).convert('RGB')
    image = image.resize((130, 130))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

def predict(file):
    """
    Perform prediction using the loaded model.
    """
    if model is None:
        return "Error: Model not loaded."
    processed_image = preprocess_image(file)
    prediction = model.predict(processed_image)
    return "Parasitée" if prediction[0][0] < 0.5 else "Saine"

def index(request):
    """
    Render the home page.
    """
    return render(request, 'index.html', {'title': 'Home'})

def upload(request):
    """
    Handle the image upload and make a prediction.
    """
    if request.method == 'POST' and 'image' in request.FILES:
        file = request.FILES['image']  # Get uploaded image
        result = predict(file)  # Perform prediction
        return render(request, 'result.html', {'title': 'Prediction Result', 'prediction': result})
    return render(request, 'upload.html', {'title': 'Upload Image'})

def result(request):
    """
    Render the result page. (Not used for redirection anymore)
    """
    return render(request, 'result.html', {'title': 'Prediction Result'})
