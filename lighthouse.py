import requests
import pandas as pd
from datetime import date

url_list = pd.read_excel('urls.xlsx')
device = 'mobile' #Select here device it can be mobile or desktop
category = 'performance'
today = date.today().strftime("%Y-%m-%d")


def webcorevitals(url_list,device,category,today):
    df_list = []
    for url in url_list['URL']:
        print(url)
        
           
        #making api call for URL
        response = requests.get("https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url="+url+"&strategy="+device+"&category="+category)
        
        
        #saving response as json
        data = response.json()
        
        print('Running URL #',url)
        
        test = url
        date = today
        
# =============================================================================
#         #Getting Metrics
#         
# =============================================================================
        
        try:   
            data = data['lighthouseResult']
        except KeyError:
            print('no Values')
            data = 'No Values.'
        pass
        #First Contentful Paint
        try:
            #First Contentful Paint
            fcp  = data['audits']['first-contentful-paint']['displayValue']
        except KeyError:
            print('no Values')
            fcp = 0
        pass
        
        #Largest Contentful Paint
        try:
             
            lcp = data['audits']['largest-contentful-paint']['displayValue']
        except KeyError:
            print('no Values')
            lcp = 0
        pass
        
        #Cumulative layout shift
        try:
            
            cls = data['audits']['cumulative-layout-shift']['displayValue']
        except KeyError:
            print('no Values')
            cls = 0
        pass
        
        try: 
            #Speed Index
            si = data['audits']['speed-index']['displayValue']
        except KeyError:
            print('no Values')
            si = 0
        pass
        try:
            
            #Time to Interactive
            tti = data['audits']['interactive']['displayValue']
        except KeyError:
            print('no Values')
            tti = 0
        try: 
            #Total Blocking Time
            tbt= data['audits']['total-blocking-time']['displayValue']
        except KeyError:
            print('no Values')
            tbt = 0
        pass
        
        try:
            #score
            score = data['categories']['performance']['score']
        except KeyError:
            print('no Values')
        pass
            
        #list with all values
        values = [test, score,fcp,si,lcp,tti,tbt,cls,date]
        
        # create DataFrame using from score list 
        df_score = pd.DataFrame( values )
        
        #transpose so its columns
        df_score = df_score.transpose()
        
        #appending scores to empty df outside for loop
        df_list.append(df_score)

    #concatinating list of dataframe into one
    df = pd.concat(df_list)
    
    #naming columns
    df.columns = ['URL','Score', 'FCP','SI','LCP','TTI','TBT','CLS','Date']
    
    #removing s from LCA so we can get mean also transforming it to float so we can get mean values
    df['LCP'] = df['LCP'].astype(str).str.replace(r's', '').astype(float)
    df['FCP'] = df['FCP'].astype(str).str.replace(r's', '').astype(float)
    df['SI'] = df['SI'].astype(str).str.replace(r's', '').astype(float)
    df['TTI'] = df['TTI'].astype(str).str.replace(r's', '').astype(float)
    df['TBT'] = df['TBT'].astype(str).str.replace(r'ms', '')
    df['TBT'] = df['TBT'].astype(str).str.replace(r',', '').astype(float)
    df['Score'] = df['Score'].astype(float)
    df['CLS'] = df['CLS'].astype(float)
    
    CSV(df)
    
## CSV Generator
    
def CSV(df):
    import datetime
    #spitting out a CSV 
    filename =  datetime.date.today().strftime("%d-%m-%Y")+ 'all_scores.csv'    
    df.to_csv(filename)

    print(df)
    print('File was saved in ' , filename)
    

webcorevitals(url_list, device, category, today)
    

