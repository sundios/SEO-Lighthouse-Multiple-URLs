#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 11:22:38 2026

@author: kburchardt
"""

import aiohttp
import asyncio
import pandas as pd
from datetime import date

# =============================================================================
#         # Config
# =============================================================================

## Path to the xlsx file containing the list of URLs to run
## The file must have a column named "URL" (case-insensitive)
INPUT_XLSX = 'urls.xlsx'

## Definition of analysis type, date, analysis location, and API key
category = 'performance'
today = date.today().strftime("%Y-%m-%d")
locale = 'en'
key = 'get api key here --> https://developers.google.com/speed/docs/insights/v5/get-started'

## How many requests to run at the same time (PageSpeed API is rate-limited,
## so keep this modest — see note near the bottom of the script)
CONCURRENCY_LIMIT = 5


## Function to load the list of URLs from the xlsx file
def load_urls(path):
    df = pd.read_excel(path)

    # Find the URL column regardless of case (URL, url, Url, etc.)
    url_col = None
    for col in df.columns:
        if str(col).strip().lower() == 'url':
            url_col = col
            break

    if url_col is None:
        raise ValueError(
            f"Could not find a 'URL' column in {path}. "
            f"Found columns: {list(df.columns)}"
        )

    urls = df[url_col].dropna().astype(str).str.strip()
    urls = [u for u in urls if u]  # drop any empty strings
    return urls


# =============================================================================
#         # Extracting Metrics from API Response
# =============================================================================

## Function to Extract API Data
async def webcorevitals(session, url, device, category, today, progress):

    ## Header to ensure requests have no caching
    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
    }

    progress['started'] += 1
    print(f"[{progress['started']}/{progress['total']}] Fetching  {url}  ({device})...")

    ## API Call
    async with session.get(
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url + "&key=" + key + "&strategy=" + device + "&category=" + category + "&locale=" + locale,
        headers=headers
    ) as response:
        data = await response.json()

        test = url
        run_date = today

        try:
            # To get the Metrics: FIP, TTFB, INP, FID:
            data_loading = data['loadingExperience']
        except KeyError:
            data_loading = {}

        try:
            # To get the Metrics: FCP, LCP, CLS, SI, TTI, Size in MB, TBT, Score:
            data = data['lighthouseResult']
        except KeyError:
            print(f"    ! No lighthouseResult for {url} ({device}) — skipping metrics, filling with defaults")
            data = {}

        # First Contentful Paint (FCP)
        try:
            fcp = data['audits']['first-contentful-paint']['displayValue']
        except KeyError:
            fcp = 0

        # Largest Contentful Paint (LCP)
        try:
            lcp = data['audits']['largest-contentful-paint']['displayValue']
        except KeyError:
            lcp = 0

        # Cumulative Layout Shift (CLS)
        try:
            cls = data['audits']['cumulative-layout-shift']['displayValue']
        except KeyError:
            cls = 0

        # Speed Index (SI)
        try:
            si = data['audits']['speed-index']['displayValue']
        except KeyError:
            si = 0

        # Time to Interactive (TTI)
        try:
            tti = data['audits']['interactive']['displayValue']
        except KeyError:
            tti = 0

        # Total Page Size (Size in MB)
        try:
            total_bytes = data['audits']['total-byte-weight']['numericValue']
        except KeyError:
            total_bytes = 0

        # Total Blocking Time (TBT)
        try:
            tbt = data['audits']['total-blocking-time']['displayValue']
        except KeyError:
            tbt = 0

        # Score
        try:
            score = data['categories']['performance']['score']
        except KeyError:
            score = 0

        # First Input Delay (FID)
        try:
            fid = data_loading["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"]
        except KeyError:
            fid = 0

        # Interaction to Next Paint (INP)
        try:
            inp = data_loading["metrics"]["INTERACTION_TO_NEXT_PAINT"]["percentile"]
        except KeyError:
            inp = 0

        # Time to First Byte (TTFB)
        try:
            ttfb = data_loading["metrics"]["EXPERIMENTAL_TIME_TO_FIRST_BYTE"]["percentile"]
        except KeyError:
            ttfb = 0

        ## List with all Metrics
        values = [test, score, fid, inp, ttfb, fcp, si, lcp, tti, tbt, cls, total_bytes, run_date, device]

        ## Create a DataFrame with the Result
        df_score = pd.DataFrame(values)

        ## Transpose to Columns
        df_score = df_score.transpose()

        ## Naming the Columns
        df_score.columns = ['URL', 'Score', 'FID', 'INP', 'TTFB', 'FCP', 'SI', 'LCP', 'TTI', 'TBT', 'CLS', 'Size in MB', 'Date', 'Device']

        ## Transformations and Calculations to represent Metrics correctly
        df_score['FID'] = df_score['FID'].astype(str).str.replace(r',', '').astype(float)
        df_score['INP'] = df_score['INP'].astype(str).str.replace(r',', '').astype(float)
        df_score['TTFB'] = df_score['TTFB'].astype(float) / 1000
        df_score['LCP'] = df_score['LCP'].astype(str).str.replace(r's', '').astype(float)
        df_score['FCP'] = df_score['FCP'].astype(str).str.replace(r's', '').astype(float)
        df_score['SI'] = df_score['SI'].astype(str).str.replace(r's', '').astype(float)
        df_score['TTI'] = df_score['TTI'].astype(str).str.replace(r's', '').astype(float)
        df_score['TBT'] = df_score['TBT'].astype(str).str.replace(r'ms', '')
        df_score['TBT'] = df_score['TBT'].astype(str).str.replace(r',', '').astype(float)
        df_score['Score'] = df_score['Score'].astype(float) * 100
        df_score['CLS'] = df_score['CLS'].astype(float)
        df_score['Size in MB'] = df_score['Size in MB'] / (1024 * 1024)
        df_score['Device'] = device

        ## Reorganize the column order
        df_score = df_score[['Date', 'URL', 'Score', 'FID', 'INP', 'TTFB', 'FCP', 'SI', 'LCP', 'TTI', 'TBT', 'CLS', 'Size in MB', 'Device']]
        df_score.columns = ['Date', 'URL', 'Score', 'First Input Delay (FID)', 'Interaction to Next Paint (INP)', 'Time to First Byte (TTFB)', 'First Contentful Paint (FCP)', 'Speed Index (SI)', 'Largest Contentful Paint (LCP)', 'Time to Interactive (TTI)', 'Total Blocking Time (TBT)', 'Cumulative Layout Shift (CLS)', 'Size in MB', 'Device']

        progress['done'] += 1
        score_display = df_score['Score'].iloc[0]
        print(f"[{progress['done']}/{progress['total']}] Done      {url}  ({device})  — Score: {score_display}")

        return df_score


# =============================================================================
#         # Run the Requests and pass the DataFrame to an Excel File
# =============================================================================

## Function to run the Requests and build the DataFrame with Desktop and Mobile data
async def main():
    print(f"Loading URLs from {INPUT_XLSX} ...")
    url_list = load_urls(INPUT_XLSX)
    print(f"Loaded {len(url_list)} URL(s).\n")

    total_requests = len(url_list) * 2  # mobile + desktop per URL
    progress = {'started': 0, 'done': 0, 'total': total_requests}

    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    async def run_with_limit(session, url, device):
        async with semaphore:
            return await webcorevitals(session, url, device, category, today, progress)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in url_list:
            tasks.append(run_with_limit(session, url, 'mobile'))
            tasks.append(run_with_limit(session, url, 'desktop'))

        results = await asyncio.gather(*tasks)

        ## Combine all results into one DataFrame
        df_final = pd.concat(results, ignore_index=True)

        # Save the DataFrame to an Excel file
        df_final.to_excel('output.xlsx', index=False)
        print(f"\nAll done. {len(url_list)} URLs x 2 devices = {total_requests} checks saved to output.xlsx")

if __name__ == '__main__':
    # Create a new asynchronous event loop here
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())