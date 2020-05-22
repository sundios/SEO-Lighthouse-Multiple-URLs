#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:30:59 2020

@author: kburchardt
"""
import json 
import pandas as pd 


def get_scores():
    #empty DF to push all scores together into one DF
    all_scores =[]
    #Remember to change the range number depending on how many urls you have. Default is 20.
    for k in range(19):  
        # returns JSON object as a dictionary
        f = open('json/report' + str(k + 1) + '.json')
        data = json.load(f)
    
        #Getting URL we are checking scores
        url = data['requestedUrl']   
        
        #selecting the categories for scores
        df = data['categories']
        
        #going through the dictionary categories and pulling out scores into scores list
        scores = []
        for i in df:
            print(i , df[i]['score'])
            s = i , df[i]['score']
            scores.append(s)
        
        # create DataFrame using from score list 
        scores = pd.DataFrame(scores, columns =['Category', 'Score'])
      
        #adding url to scores
        scores.loc[5] = url
        
        #adding url to column 0
        scores.iloc[-1:,0]='url'
    
        #transposing column  so that we can check multiple urls and have one big list
        scores = scores.transpose()
        
        #making row 0 the header
        scores.columns = scores.iloc[0]
        
        #selecting removing top row as we just made it the header
        scores = scores.iloc[1:]
        
        #moving url column to index 0
        scores = scores[['url','performance','accessibility','best-practices','seo','pwa']]
        
        all_scores.append(scores)
        
        print(all_scores)
        
    all_scores = pd.concat(all_scores)
        
    #spitting out a CSV       
    all_scores.to_csv('all_scores.csv')
        
    
#calling function    
get_scores()
        
    








# import datetime
# import pygsheets



# #selecting the row index where we want to place recuperados
# rowIndex = df.index[16]

# #creating the column name and add value at the totals 
# df.loc[rowIndex, 'Recuperados'] = recuperados