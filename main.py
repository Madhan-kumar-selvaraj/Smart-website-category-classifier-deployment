# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 19:59:08 2020

@author: Madhan Kumar Selvaraj
"""

from fastapi import FastAPI
from typing import Optional
import website_classifier
import classifier_model_creation
from site_data import site_list

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hi!": "Welcome to the website classifier API. By using this API one can get to know the catergory of the website URL and the most commonly used words. It can able to learn from your input that's why it is knows as smart classifier", "API's Rule book": "You can get to know the category of this website and also you can add your own category for your website. It will help our API to learn from your data and the result will be more accurate", "Rule 1" : "To get to know the category, send the request in this format 'https://smart-website-classifier.herokuapp.com/(url)'. For example if the url is 'https://news.google.co.in' them replace the '/' with '*' and send the request like this 'https://smart-website-classifier.herokuapp.com/https:**news.google.co.in'", "Rule 2" : "You can add your own category in this format https://smart-website-classifier.herokuapp.com/(url)?category=(category). For example if your url is 'https://www.mdpi.com/journal/agriculture' and category is 'agriculture'. request format is 'https://smart-website-classifier.herokuapp.com/https:**www.mdpi.com*journal*agriculture?category=agriculture'"}


@app.get("/{url}")
def read_item(url: str, category : Optional[str] = None):
    print(category)
    print(url)
    if category is None:
        result, remark, add_category, category_list, top_words = website_classifier.classify(url)
        return {"Website category": result, "Remarks":remark, "Add your own category": add_category ,"Available category list": category_list, "100 most common words in the website": top_words}
    else:
        status = classifier_model_creation.content_extractor(url, category)
        return {"Status" : status}



@app.get("/rootaccess/{password}")
def read_user(password: str):
    print(password)
    if password == "madhan123":
        status = classifier_model_creation.content_extractor(site_list, None)
        return{"Status" : status}

    else:
        return{"Status" : "Unauthenticated user"}
    

