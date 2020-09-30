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
    for k in range(12):  
        # returns JSON object as a dictionary
        f = open('./json/report' + str(k + 1) + '.json')
        data = json.load(f)
    
        #Getting URL we are checking scores
        url = data['requestedUrl']   
        
        #Getting Metrics
        
        #First Contentful Paint
        FCP  = data['audits']['first-contentful-paint']['displayValue']
        #Largest Contentful Paint
        LCP = data['audits']['largest-contentful-paint']['displayValue']
        #Cumulative layout shift
        CLS = data['audits']['cumulative-layout-shift']['displayValue']
        #Speed Index
        SI = data['audits']['speed-index']['displayValue']
        #Time to Interactive
        TTI = data['audits']['interactive']['displayValue']
        #Total Blocking Time
        TBT = data['audits']['total-blocking-time']['displayValue']
        
        
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
    
    #Concatenating all dates on one big master file


    import numpy as np
    import pandas as pd
    import glob

    #Files that we want to run to get totals
    files = sorted(glob.glob('*all_scores.csv'))

    #opening all files
    li = []
    for f in files:
        df = pd.read_csv(f,index_col=False)
        print(df)
        li.append(df)


    #concatenating all Dataframes into one
    df = pd.concat(li)


    #Getting list of regions
    urls = df['url']


    #deduplicate
    urls = list(dict.fromkeys(urls))


    #sort by urls and Date
    df = df.sort_values(by=['url','date'])

    df = df[['url','performance','accessibility','best-practices','seo','LCP','CLS','FCP','SI','TTI','TBT','date']]

    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")


    #grouping urls together by date
    r=[]
    for j in range(1):
        print(j)
        for i in urls:
            print(i)
            r.append(df.loc[df['url'] == i])

    
 #calling function    
get_scores(today)   
   