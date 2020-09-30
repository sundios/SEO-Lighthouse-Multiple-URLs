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

def get_scores(today):
    #empty DF to push all scores together into one DF
    all_scores =[]
    #Remember to change the range number depending on how many urls you have. Default is 20.
    for k in range(19):  
        # returns JSON object as a dictionary
        f = open('./json/report' + str(k + 1) + '.json')
        data = json.load(f)
    
        #Getting URL we are checking scores
        url = data['requestedUrl']   
        
# =============================================================================
#         #Getting Metrics
#         
# =============================================================================
        
        #First Contentful Paint
        try:
            #First Contentful Paint
            FCP  = data['audits']['first-contentful-paint']['displayValue']
        except KeyError:
            print('no Values')
            FCP = 0
        pass
        
        #Largest Contentful Paint
        try:
             
            LCP = data['audits']['largest-contentful-paint']['displayValue']
        except KeyError:
            print('no Values')
            LCP = 0
        pass
    
        #Cumulative layout shift
        try:
            
            CLS = data['audits']['cumulative-layout-shift']['displayValue']
        except KeyError:
            print('no Values')
            CLS = 0
        pass
        
        try: 
            #Speed Index
            SI = data['audits']['speed-index']['displayValue']
        except KeyError:
            print('no Values')
            SI = 0
        pass
        try:
            
            #Time to Interactive
            TTI = data['audits']['interactive']['displayValue']
        except KeyError:
            print('no Values')
            TTI = 0
        try:
            
            #Total Blocking Time
            TBT = data['audits']['total-blocking-time']['displayValue']
        except KeyError:
            print('no Values')
            TBT = 0
        pass
        
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
        scores.loc[7] = FCP
        
        #Adding LCP to Scores
        scores.loc[8] = LCP
        
        #Adding LCP to Scores
        scores.loc[9] = CLS
               
        #Adding LCP to Scores
        scores.loc[10] = SI
               
        #Adding LCP to Scores
        scores.loc[11] = TTI
        
         #Adding LCP to Scores
        scores.loc[12] = TBT
               
               
        #adding url to column 0
        scores.iloc[5,0]='url'
    
        #adding Dates to column 0
        scores.iloc[6,0]='date'
        
        #adding LCP to column 0
        scores.iloc[7,0]='FCP'
    
        #adding LCA to column 0
        scores.iloc[8,0]='LCP'
        
        #adding LCP to column 0
        scores.iloc[9,0]='CLS'
    
        #adding LCA to column 0
        scores.iloc[10,0]='SI'
        
        #adding LCA to column 0
        scores.iloc[11,0]='TTI'
        
        #adding LCA to column 0
        scores.iloc[12,0]='TBT'
        
        #transposing column so that we can check multiple urls and have one big list
        scores = scores.transpose()
        
               
        #making row 0 the header
        scores.columns = scores.iloc[0]
        
        #selecting removing top row as we just made it the header
        scores = scores.iloc[1:]
        
        #moving url column to index 0
        scores = scores[['url','performance','accessibility','best-practices','seo','pwa','LCP','CLS','FCP','SI','TTI','TBT','date']]
        
        all_scores.append(scores)
        
    
    print(all_scores)
        
    all_scores = pd.concat(all_scores)
    
    all_scores = all_scores.fillna(0)
        
    
    #removing s from LCA so we can get mean also transforming it to float
    all_scores['LCP'] = all_scores['LCP'].astype(str).str.replace(r's', '').astype(float)
    all_scores['FCP'] = all_scores['FCP'].astype(str).str.replace(r's', '').astype(float)
    all_scores['SI'] = all_scores['SI'].astype(str).str.replace(r's', '').astype(float)
    all_scores['TTI'] = all_scores['TTI'].astype(str).str.replace(r's', '').astype(float)
    all_scores['TBT'] = all_scores['TBT'].astype(str).str.replace(r'ms', '')
        
        
    #transforming into integer 
    all_scores['LCP'] = all_scores['LCP'].astype(int)
    all_scores['FCP'] = all_scores['FCP'].astype(int)
    all_scores['SI'] = all_scores['SI'].astype(int)
    all_scores['TTI'] = all_scores['TTI'].astype(int)
    
    #spitting out a CSV 
    import datetime
    filename =  datetime.date.today().strftime("%d-%m-%Y")+ 'all_scores.csv'    
    all_scores.to_csv(filename)

    print(all_scores)
    print('File was saved in ' , filename)

    

    
    
#calling function    
get_scores(today)
        
    

