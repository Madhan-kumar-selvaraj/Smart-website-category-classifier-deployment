# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 20:43:02 2020

@author: Madhan Kumar Selvaraj
"""

import os
import json
import configuration

news_website = ["https://www.ndtv.com/","https://timesofindia.indiatimes.com/",
        "https://www.indiatoday.in/","https://www.kadaza.in/news",
        "https://www.news18.com/","https://news.google.co.in/",
        "https://www.cnet.com/news/","https://www.timesnownews.com/",
        "https://www.hindustantimes.com/","https://www.bbc.com/news/world"]
    
job_website = ["https://www.iimjobs.com/", "https://www.shine.com/", 
               "https://www.firstnaukri.com/", "https://www.freshersworld.com/", 
               "https://www.linkedin.com/", "https://www.freelancemyway.com/", 
               "https://www.indeed.co.in/", "https://www.fresherslive.com/",
               "https://www.jobsarkari.com/", "https://angel.co/jobs" ]
            
adult_website = ["https://www.xvideos.com/", "https://www.pornhub.com/", 
                "https://xhamster.com/", "https://www.xnxx.com/",
                "https://www.youporn.com/", "https://www.vporn.com/",
                "https://www.porn.com/", "https://www.tnaflix.com/", 
                "http://www.tube8.com/","https://spankbang.com/"]
technology_website = ["https://techcrunch.com/", "https://gizmodo.com/", 
                      "https://www.techhive.com/", "https://www.cbinsights.com/", 
                      "https://www.cordcuttersnews.com/", "https://www.makeuseof.com/", 
                      "https://lifehacker.com/", "https://www.computerworld.com/in/",
                      "https://www.howtogeek.com/", "https://www.pymnts.com/"]

animal_website = ["http://www.worldanimalnet.org/", "http://animaladay.blogspot.com/", 
                  "http://www.animalcorner.co.uk/", "http://www.zooborns.com/", 
                  "http://www.arkive.org/education", "http://www.vitalground.org/", 
                  "http://www.bestanimalsites.com/", "http://www.kidsplanet.org/", 
                  "http://www.wildlifearchives.com/", "http://switchzoo.com/"]
              
space_website = ["http://amazing-space.stsci.edu/", "http://www.astroengine.com/", 
                 "http://chandra.harvard.edu/", "http://hubblesite.org/", "http://www.spaceweather.com/", 
                 "http://www.nineplanets.org/", "http://www.worldwidetelescope.org/",
                 "http://www.kidsastronomy.com/", "http://www.fourmilab.ch/solar/solar.html", "http://www.space.com/"]
            
site_list = [news_website, adult_website, space_website, animal_website]

site_list_dict = {"news_website": news_website, "adult_website": adult_website, "space_website": space_website, "animal_website":animal_website}

def website_category(url_dict):

    if os.path.exists(configuration.website_category_path):
        os.remove(configuration.website_category_path)
        
    file = open(configuration.website_category_path,"a+")
    file.close()
           
    file = open(configuration.website_category_path, "r+")
    output = file.read()
    file.close()
    
    file = open(configuration.website_category_path, "w+")
    print("output:", output)
    try:
        json.dump(url_dict, file)
    except Exception as error:
        print("Error:", error)
    file.close()
    return "successfully wesbite url dictionary file created"
