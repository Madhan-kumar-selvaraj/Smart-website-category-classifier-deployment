# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:04:25 2020

@author: Madhan Kumar Selvaraj
"""

import _pickle as cPickle
import pickle
import os
import json
import nltk
import spacy
import requests
import numpy as np
from bs4 import BeautifulSoup
from nltk.tokenize.treebank import TreebankWordDetokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('words')
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import configuration
import site_data

def content_extractor(site_url, target):
    check_content = 1
    website = []
    target_data = []
    
    if target is None:
        if os.path.exists(configuration.input_file_path):
            os.remove(configuration.input_file_path)
            
        if os.path.exists(configuration.output_file_path):
            os.remove(configuration.output_file_path)
            
        target_dict = {}
        site_dict_keys = list(site_data.site_list_dict.keys())
        for index, value in enumerate(site_dict_keys):
            target_dict[index+1] = value
        print(target_dict)
        print(site_data.website_category(target_dict))
            
        for values in site_url:
            website.extend(values)
            
        for index, data in enumerate (site_url):
            target_data.extend([index+1] * len(data))          
    else:
        file = open(configuration.website_category_path, "r+")
        output = file.read()
        website_category_dict = json.loads(output)
        print(website_category_dict)        
        file.close()
        
        key_value = None
        for key, value in website_category_dict.items(): 
            if target == value: 
                key_value = key 
        
        if key_value is None:       
            file = open(configuration.website_category_path, "w+")
            print("output:", output)
            dict_length = len(website_category_dict)+1
            website_category_dict.update({dict_length : target})
            print("website_category_dict:", website_category_dict)
            json.dump(website_category_dict, file)
            file.close()
            target = dict_length
        else:
            target = key_value
            
        print("Target value:", target)
        
        website.append(site_url)
        target_data.append(target)
        
    website_target = dict(zip(website, target_data))
    print("Dictionary:",website_target)
    for key, value in website_target.items():
        url = key.replace("*","/")
        try:
            print(key, value)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            for script in soup(["script", "style"]):
                script.extract()
            raw_data = soup.get_text()
            words = set(nltk.corpus.words.words())
            raw_data = " ".join(w for w in nltk.wordpunct_tokenize(raw_data) if w.lower() in words)
            nlp = spacy.load("en")
            file_text = nlp(raw_data)
            words = [token.lemma_ for token in file_text if not token.is_punct and not token.like_num and not token.is_space
                    and not token.is_stop]
            strip_data = [token.lower() for token in words if not len(token.strip())<2 and not len(token.strip())>15]
            print(len(strip_data))
            if len(strip_data) > 200:
                untokenize_data = TreebankWordDetokenizer().detokenize(strip_data)
                input_content = open(configuration.input_file_path, "a+", encoding="utf-8") 
                input_content.write(untokenize_data + "\r")
                input_content.close()
                
                target_content = open(configuration.output_file_path, "a+", encoding="utf-8") 
                target_content.write(str(value) + "\r")
                target_content.close()
                
            else:
                check_content = 0
                
                          
        except Exception as error:
            check_content = 0
            print("Error: ", error)

    if ((check_content == 1 and len(website) == 1 ) or len(website)> 1):
        file = open(configuration.input_file_path, "r")
        input_data = []
        for content in file:
            content = content.replace("\n","")
            input_data.append(content)
        file.close()   
        file = open(configuration.output_file_path, "r")
        output_list = []
        for content in file:
            content = content.replace("\n", "")
            output_list.append(int(content))
        file.close()
        output = np.array(output_list)
        output = np.reshape(output_list, (len(output_list),1))
    
    
        xtrain, xtest, ytrain, ytest = train_test_split(input_data, output, test_size = 0.15, random_state = 5)
        vectorizer = TfidfVectorizer()
        voacb_fit = vectorizer.fit(xtrain)
        
        xtrain_df = vectorizer.transform(xtrain)
        xtest_df = vectorizer.transform(xtest)
        
        pickle.dump(voacb_fit, open(configuration.vocabulary_path, "wb"))
        
        model = MultinomialNB()
        model.fit(xtrain_df, ytrain)
        
        y_predict = model.predict(xtest_df)
        print(y_predict)
        print(metrics.accuracy_score(ytest, y_predict))
        with open(configuration.classifier_model_path, 'wb') as fid:
            cPickle.dump(model, fid)
        if target is None:
            return "Successfully reloaded the model"
        else:
            return "New category added in our database. Thanks for your valuable contribution"
    else:
        return "Can't add your data due to less content in the site"
        


