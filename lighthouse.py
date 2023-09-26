import aiohttp
import asyncio
import pandas as pd
from datetime import date

# =============================================================================
#         # Extracting Metrics from API Response
# =============================================================================

## List of URLs to run in a loop
url_list = [
    "https://www.google.com",
    "https://www.facebook.com",
    "https://www.amazon.com",
    "https://www.youtube.com",
]

## Definition of analysis type, date, analysis location, and API key
category = 'performance'
today = date.today().strftime("%Y-%m-%d")
locale = 'en'
key = 'get your api key here: https://developers.google.com/speed/docs/insights/v5/get-started'

## Function to Extract API Data
async def webcorevitals(session, url, device, category, today):
    
    ## Header to ensure requests have no caching
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
    }

    ## API call
    async with session.get(
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url + "&key=" + key + "&strategy=" + device + "&category=" + category+ "&locale=" + locale,
        headers=headers
    ) as response:
        data = await response.json()

        print('Running URL #', url, device)

        test = url
        date = today
        
        try:
            data = data['lighthouseResult']
        except KeyError:
            print('No Values')
            data = 'No Values.'

        # First Contentful Paint
        try:
            fcp = data['audits']['first-contentful-paint']['displayValue']
        except KeyError:
            print('No Values')
            fcp = 0

        # Largest Contentful Paint
        try:
            lcp = data['audits']['largest-contentful-paint']['displayValue']
        except KeyError:
            print('No Values')
            lcp = 0

        # Cumulative layout shift
        try:
            cls = data['audits']['cumulative-layout-shift']['displayValue']
        except KeyError:
            print('No Values')
            cls = 0

        try:
            # Speed Index
            si = data['audits']['speed-index']['displayValue']
        except KeyError:
            print('No Values')
            si = 0

        try:
            # Time to Interactive
            tti = data['audits']['interactive']['displayValue']
        except KeyError:
            print('No Values')
            tti = 0

        try:
            # Total Page Size
            bytes = data['audits']['total-byte-weight']['numericValue']
        except KeyError:
            print('No Values')
            bytes = 0
            
        try:
            # Total Blocking Time
            tbt = data['audits']['total-blocking-time']['displayValue']
        except KeyError:
            print('No Values')
            tbt = 0
            
        try:
            # Score
            score = data['categories']['performance']['score']
        except KeyError:
            print('No Values')

        ## List with all Metrics
        values = [test, score, fcp, si, lcp, tti, tbt, cls, bytes, date, device]

        ## Create a DataFrame with the Result
        df_score = pd.DataFrame(values)

        ## Transpose to Columns
        df_score = df_score.transpose()

        ## Naming the Columns
        df_score.columns = ['URL', 'Score', 'FCP', 'SI', 'LCP', 'TTI', 'TBT', 'CLS', 'Size in MB', 'Date', 'Device']

        ## Transformations and Calculations to represent Metrics correctly
        df_score['LCP'] = df_score['LCP'].astype(str).str.replace(r's', '').astype(float)
        df_score['FCP'] = df_score['FCP'].astype(str).str.replace(r's', '').astype(float)
        df_score['SI'] = df_score['SI'].astype(str).str.replace(r's', '').astype(float)
        df_score['TTI'] = df_score['TTI'].astype(str).str.replace(r's', '').astype(float)
        df_score['TBT'] = df_score['TBT'].astype(str).str.replace(r'ms', '')
        df_score['TBT'] = df_score['TBT'].astype(str).str.replace(r',', '').astype(float)
        df_score['Score'] = df_score['Score'].astype(float) * 100
        df_score['CLS'] = df_score['CLS'].astype(float)
        df_score['Size in MB'] = df_score['Size in MB']/ (1024 * 1024)
        df_score['Device'] = device
        
        ## Reorganize the column order
        df_score = df_score[['Date', 'URL', 'Score', 'FCP', 'SI', 'LCP', 'TTI', 'TBT', 'CLS', 'Size in MB', 'Device']]

        return df_score
    
# =============================================================================
#         # Run the Requests and pass the DataFrame to an Excel File
# =============================================================================

## Function to run the Requests and build the DataFrame with Desktop and Mobile data
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            tasks.append(webcorevitals(session, url, 'mobile', category, today))
            tasks.append(webcorevitals(session, url, 'desktop', category, today))

        results = await asyncio.gather(*tasks)

        ## Create an Empty DataFrame to Store the Results
        df_final = pd.concat(results, ignore_index=True)
        
        # Save the DataFrame to an Excel file
        df_final.to_excel('output.xlsx', index=False)        

if __name__ == '__main__':
    # Create a new asynchronous event loop here
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())