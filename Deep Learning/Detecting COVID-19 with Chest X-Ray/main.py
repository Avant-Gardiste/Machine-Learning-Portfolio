#!/usr/bin/env python
# coding: utf-8

# In[1]:


import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask, render_template


# In[2]:


app= Flask(__name__)

label_dict={0:'Covid-19 Negative', 1:'Covid-19 Positive'}

def get_model():
    global model
    model = load_model('model/model.h5')
    print('[INFO] MODEL LOADED SUCCESSFULLY')
    
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image

print('[INFO] Loading Keras model ...')
get_model()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    message = request.get_json(force=True)
    encoded = message['image']
    decoded = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(decoded))
    processed_image = preprocess_image(image, target_size=(196,196))
    
    prediction = model.predict(processed_image)
    
    output=np.argmax(prediction)
    
    label=label_dict[output]
                     
    print(label)
    
    response = {
        'prediction' : {
            'result': label
        }
    }
    
    return jsonify(response)

app.run(debug=True)