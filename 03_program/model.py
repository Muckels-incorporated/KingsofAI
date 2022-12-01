#!/usr/bin/env python3

import streamlit as st
import tensorflow as tf
from PIL import Image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

model = load_model('fruits_recognition_CNN_model_V2.h5')
labels = { 0: 'Apple Red 1', 1: 'Orange', 2: 'Banana', 3: 'Grape', 4: 'Kiwi', 5: 'Mandarin', 6: 'Nectarine', 7: 'Pear', 8: 'Plum' }
fruits = ['Apple','Orange','Banana','Grape','Kiwi','Mandarin','Nectarine','Pear','Plum']


def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()

def run():
    st.title("Fruits🍍-Vegetable🍅 Classification")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250,250))
        st.image(img,use_column_width=False)
        save_image_path = './upload_images/'+img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result= processed_img(save_image_path)
            print(result)
            if result in vegetables:
                st.info('**Category : Vegetables**')
            else:
                st.info('**Category : Fruit**')
            st.success("**Predicted : "+result+'**')
            cal = fetch_calories(result)
            if cal:
                st.warning('**'+cal+'(100 grams)**')
run()