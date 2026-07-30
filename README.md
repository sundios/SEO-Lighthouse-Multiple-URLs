# SEO: Run multiple URLs and get Lighthouse V5 Scores

## How the Script Works

This Python script extracts web performance metrics, specifically Core Web Vitals, from a list of URLs using the Google PageSpeed Insights API. It reads the URLs from an Excel file, uses the `aiohttp` library for asynchronous HTTP requests and `asyncio` for handling concurrency. The extracted metrics are then processed and saved to an Excel file for further analysis.

### Script Workflow

1. **URL List**: The script reads the URLs from an Excel file (`urls.xlsx` by default). The file must contain a column named `URL` (the match is case-insensitive, so `url` or `Url` also work). Empty rows are skipped automatically. Point the script at a different file by changing the `INPUT_XLSX` variable.

2. **API Configuration**: Key configuration parameters are set at the top of the script:
    - `INPUT_XLSX`: Path to the Excel file containing the URLs.
    - `category`: The performance category for analysis.
    - `today`: The current date in the format "yyyy-mm-dd."
    - `locale`: The locale for analysis (e.g., 'en' for English, 'br' for Brazil).
    - `key`: Your API key, which you can obtain from [Google's PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started).
    - `CONCURRENCY_LIMIT`: How many API requests run at the same time (defaults to 5). The PageSpeed API is rate-limited, so keep this modest — raising it too high will start returning errors.

3. **API Data Extraction**: The script defines an asynchronous function `webcorevitals` to make API requests for each URL, both for 'mobile' and 'desktop' devices. It extracts various performance metrics, such as First Input Delay (FID), Interaction to Next Paint (INP), Time to First Byte (TTFB), First Contentful Paint (FCP), Speed Index (SI), Largest Contentful Paint (LCP), Time to Interactive (TTI), Total Blocking Time (TBT), Cumulative Layout Shift (CLS), Total Page Size, and the overall performance score.

4. **Progress Output**: While it runs, the script prints a live progress counter to the terminal so you can see which URLs are being fetched and which have finished, along with their score:

   ```
   Loading URLs from urls.xlsx ...
   Loaded 40 URL(s).

   [1/80] Fetching  https://www.google.com  (mobile)...
   [1/80] Done      https://www.google.com  (mobile)  — Score: 76.0
   ```

5. **Error Handling**: If the API returns no `lighthouseResult` for a URL (for example a timeout or an unreachable page), the script prints a warning, fills that row's metrics with defaults, and keeps going instead of stopping the whole run.

6. **Data Transformation**: The extracted data is transformed and processed to ensure consistency and proper data types.

7. **DataFrame Creation**: A Pandas DataFrame is created to organize the extracted metrics, with columns for Date, URL, Score, FID, INP, TTFB, FCP, SI, LCP, TTI, TBT, CLS, Size in MB, and Device.

8. **Excel Output**: The final DataFrame is concatenated from all requests and saved as an Excel file named 'output.xlsx' in the same directory as the script.

## How to Use It

1. **Install Dependencies**: Make sure you have the required Python libraries installed. You can install them using pip:

   `pip install aiohttp pandas openpyxl`

   (`openpyxl` is what pandas uses to read and write the `.xlsx` files.)

2. **API Key**: Obtain an API key from [Google's PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started) and replace the `key` variable in the script with your key. The page walks you through creating a Google Cloud project, enabling the PageSpeed Insights API, and generating the key.

3. **Add Your URLs**: Put the URLs you want to test in `urls.xlsx`, in a column named `URL` — one URL per row:

   | URL                     |
   |-------------------------|
   | https://www.google.com  |
   | https://www.github.com  |

   If your file has a different name or lives somewhere else, update the `INPUT_XLSX` variable in the script.

4. **Run the Script**: Execute the script using Python:

   `python lighthouse.py`

5. **Output**: Once the script finishes execution, you will find an Excel file named 'output.xlsx' containing the extracted web performance metrics in the same directory as the script. Each URL produces two rows — one for mobile and one for desktop.

**For Example:**

| Date       | URL                                 | Score | FID | INP | TTFB | FCP | SI  | LCP | TTI | TBT | CLS   | Size (MB)   | Device  |
|------------|-------------------------------------|-------|-----|-----|------|-----|-----|-----|-----|-----|-------|-------------|---------|
| 2023-09-25 | [https://www.google.com](https://www.google.com) | 76    | 12  | 180 | 0.8  | 2   | 3.2 | 2   | 8.5 | 910 | 0.014 | 1.123100281 | mobile  |
| 2023-09-25 | [https://www.google.com](https://www.google.com) | 92    | 8   | 120 | 0.4  | 0.4 | 0.8 | 0.6 | 1.9 | 220 | 0.007 | 1.246808052 | desktop |

## Contributing

If you want to contribute please open an issue or send me an email hello@kburchardt.com. If not just give me a star.

## Authors

* **Konrad Burchardt** - *Initial work* - [Sundios](https://github.com/sundios)
* **Vinicius Stanula** - *Added new metrics and implemented Async Function* - [Vinicius](https://github.com/ViniciusStanula)
