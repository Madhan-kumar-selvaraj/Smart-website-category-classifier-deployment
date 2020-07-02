# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 21:00:25 2020

@author: Madhan Kumar Selvaraj
"""

import nltk
from nltk.probability import FreqDist
nltk.download('words')
import spacy
import requests
from bs4 import BeautifulSoup
from nltk.tokenize.treebank import TreebankWordDetokenizer
import _pickle as cPickle
import pickle
import configuration
import json

def classify(url):
    try:
        url = url.replace("*","/")
        complete_data = []
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
        if len(strip_data) > 30:
            frequencies_words = FreqDist(strip_data).most_common(100)
            words_most_frequent = [word[0] for word in frequencies_words]
            untokenize_data = TreebankWordDetokenizer().detokenize(strip_data)
            complete_data.append(untokenize_data)
            
            vocabalary = pickle.load(open(configuration.vocabulary_path, "rb"))
            data = vocabalary.transform(complete_data)
            with open(configuration.classifier_model_path, 'rb') as fid:
                model_load = cPickle.load(fid)
            y_predict = model_load.predict(data)
            array_percentage = model_load.predict_proba(data)
            array_percentage = array_percentage *100
            print(array_percentage[:].round(2))
            
            file = open(configuration.website_category_path, "r+")
            output = file.read()
            dic = json.loads(output)
            file.close()
            target_dict= {}
            category_url_list = []
            for key, value in dic.items():
                target_dict[int(key)] = value
                category_url_list.append(value)
            print(target_dict)
            print(category_url_list)

            result_percent = array_percentage[:,y_predict[0]-1][0]
            result_percent = result_percent.round(2)
            if result_percent > 30 :
                if len(strip_data)<500:
                    return (str(target_dict[y_predict[0]] ), "Note: Classification result may be inaccurate due to minimal content in the website and it's accuracy is " + str(result_percent) + " %" , "You can add you own category for your website. If the name of the category peresent in the below list use that name. Or else create your own in this format http://127.0.0.1:8000/(url)?category=(category). For exmaple: http://127.0.0.1:8000/https:**www.mdpi.com*journal*agriculture?category=agriculture", category_url_list, words_most_frequent)
                else:
                    return (target_dict[y_predict[0]], "Accuracy of the classification is " + str(result_percent) + " %" , "You can add you own category for your website. If the name of the category peresent in the below list use that name. Or else create your own in this format http://127.0.0.1:8000/(url)?category=(category). For exmaple: http://127.0.0.1:8000/https:**www.mdpi.com*journal*agriculture?category=agriculture", category_url_list , words_most_frequent)
            else:
                return ("Given website is not related to space, job portal, adult, animals, news category", "May be it is related to "+ str(target_dict[y_predict[0]]) + " and it's accuracy is " + str(result_percent)  + " %" , "You can add you own category for your website. If the name of the category peresent in the below list use that name. Or else create your own in this format http://127.0.0.1:8000/(url)?category=(category). For exmaple: http://127.0.0.1:8000/https:**www.mdpi.com*journal*agriculture?category=agriculture", category_url_list, words_most_frequent)
            
        else:
            return ("Can't extract content from the website", "Site may be invalid or unavailable or having very few content", "Not available", "Not available", "Not available")
        
    except Exception as e:
        return ("Facing error while parsing the website", e, "Not available", "Not available", "Not available")
