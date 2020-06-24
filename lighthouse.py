#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:30:59 2020

@author: kburchardt
"""
import json 
import pandas as pd 

from datetime import date

today = date.today().strftime("%Y-%m-%d")

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

        #Getting Scores
        LCP = data['audits']['largest-contentful-paint']['displayValue']
        CLS = data['audits']['cumulative-layout-shift']['displayValue']

        #selecting the categories for scores
        df = data['categories']

        #creating date column
        today = today
        
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
        
        #adding date to scores
        scores.loc[6] = today
        
        #Adding LCP to Scores
        scores.loc[7] = LCP
        
        #Adding LCP to Scores
        scores.loc[8] = CLS
               
        #adding url to column 0
        scores.iloc[5,0]='url'
    
        #adding Dates to column 0
        scores.iloc[6,0]='date'
        
        #adding LCP to column 0
        scores.iloc[7,0]='LCP'
    
        #adding LCA to column 0
        scores.iloc[8,0]='CLS'
    
        #transposing column  so that we can check multiple urls and have one big list
        scores = scores.transpose()
        
        #making row 0 the header
        scores.columns = scores.iloc[0]
        
        #selecting removing top row as we just made it the header
        scores = scores.iloc[1:]
        
        #moving url column to index 0
        scores = scores[['url','performance','accessibility','best-practices','seo','pwa','LCP','CLS','date']]
        
        all_scores.append(scores)
        
        print(all_scores)
        
    all_scores = pd.concat(all_scores)

    #removing s from LCA so we can get mean also transforming it to float
    all_scores['LCP'] = all_scores['LCP'].astype(str).str.replace(r's', '').astype(float)
        
    #transforming into integer 
    all_scores['LCP'] = all_scores['LCP'].astype(int)
    #transforming into integer 
    all_scores['CLS'] = all_scores['CLS'].astype(int)

    #spitting out a CSV 
    import datetime
    filename =  datetime.date.today().strftime("%d-%m-%Y")+ 'all_scores.csv'    
    all_scores.to_csv(filename)

        
    #spitting out a CSV       
    all_scores.to_csv('all_scores.csv')
        
    
#calling function    
get_scores()
        
    





### Here we need to create Google sheets connection to send it to the Gsheets


# import datetime
# import pygsheets



# #selecting the row index where we want to place recuperados
# rowIndex = df.index[16]

# #creating the column name and add value at the totals 
# df.loc[rowIndex, 'Recuperados'] = recuperados