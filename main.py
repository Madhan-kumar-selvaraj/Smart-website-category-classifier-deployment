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
    return {"Hi!": "Welcome to website classifier API"}


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
    

