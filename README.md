# SEO: Run multiple URLs and get Ligthhouse V5 Scores

## How the Script Works

This Python script is designed to extract web performance metrics, specifically Core Web Vitals, from a list of URLs using the Google PageSpeed Insights API. It utilizes the `aiohttp` library for asynchronous HTTP requests and `asyncio` for handling concurrency. The extracted metrics are then processed and saved to an Excel file for further analysis.

### Script Workflow

1. **URL List**: The script starts with a predefined list of URLs to analyze. You can customize this list by adding or removing URLs in the `url_list` variable.

2. **API Configuration**: Key configuration parameters are set, including:
    - `category`: The performance category for analysis.
    - `today`: The current date in the format "dd-mm-yyyy."
    - `locale`: The locale for analysis (e.g., 'br' for Brazil).
    - `key`: Your API key, which you can obtain from [Google's PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started).

3. **API Data Extraction**: The script defines an asynchronous function `webcorevitals` to make API requests for each URL, both for 'mobile' and 'desktop' devices. It extracts various performance metrics, such as First Input Delay (FID), Interaction to Next Paint (INP), Time to First Byte (TTFB), First Contentful Paint (FCP), Speed Index (SI), Largest Contentful Paint (LCP), Time to Interactive (TTI), Total Blocking Time (TBT), Cumulative Layout Shift (CLS), Total Page Size, and the overall performance score.

4. **Data Transformation**: The extracted data is transformed and processed to ensure consistency and proper data types.

5. **DataFrame Creation**: A Pandas DataFrame is created to organize the extracted metrics. The DataFrame is structured with columns for Date, URL, Score, FCP, SI, LCP, TTI, TBT, CLS, Size in MB, and Device.

6. **Concurrent Execution**: The script uses asyncio to run API requests concurrently for all URLs and devices, significantly speeding up the data extraction process.

7. **Excel Output**: The final DataFrame is concatenated from all requests and saved as an Excel file named 'output.xlsx' in the same directory as the script.

## How to Use It

1. **Install Dependencies**: Make sure you have the required Python libraries installed. You can install them using pip:

   `pip install aiohttp asyncio pandas`

2. **API Key**: Obtain an API key from [Google's PageSpeed Insights API](https://developers.google.com/speed/docs/insights/v5/get-started) and replace the `key` variable in the script with your key.

3. **Customize URL List**: Customize the list of URLs to analyze by modifying the `url_list` variable in the script.

4. **Run the Script**: Execute the script using Python:

   `python your_script_name.py`

5. **Output**: Once the script finishes execution, you will find an Excel file named 'output.xlsx' containing the extracted web performance metrics in the same directory as the script.

**For Example:**

| Date       | URL                                 | Score | FCP | SI  | LCP | TTI | TBT | CLS   | Size (MB)   | Device  |
|------------|-------------------------------------|-------|-----|-----|-----|-----|-----|-------|-------------|---------|
| 2023-09-25 | [https://www.google.com](https://www.google.com) | 76    | 2   | 3.2 | 2   | 8.5 | 910 | 0.014 | 1.123100281 | mobile  |
| 2023-09-25 | [https://www.google.com](https://www.google.com) | 92    | 0.4 | 0.8 | 0.6 | 1.9 | 220 | 0.007 | 1.246808052 | desktop |

## Contributing

If you want to contribute please open an issue or send me an email hello@kburchardt.com. If not just give me a star.

## Authors

* **Konrad Burchardt** - *Initial work* - [Sundios](https://github.com/sundios)
* **Vinicius Stanula** - *Added new metrics and implemented Async Function* - [Vinicius](https://github.com/ViniciusStanula)