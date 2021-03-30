# SEO: Run multiple URLs and get ligthhouse V6 Scores.

Run lighthosue with multiple URLs and get different scores all in one master csv file.

## Getting Started

Previously we had a different script that urn a bash file and used node lightouse. I re-did the script and made it less complicated. Now we can run evertyhgin just from python using a csv file

### Prerequisites
```
pandas
requests
```

### Running Script 

Once we install the prerequistes we can go ahead and add the URLs we want to get the scores on urls.xlsx.

After that we go into the command line and run:



```
python lighthouse.py
```

Once finished this will  output one master file with all your scores for your different URLs

**For Example:**

| url                                	| Performance 	| accessibility 	| best-practices 	| seo 	| pwd 	|
|------------------------------------	|-------------	|---------------	|----------------	|-----	|-----	|
| https://www.kburchardt.com         	| 80          	| 90            	| 100            	| 100 	| 100 	|
| https://www.uselessthingstobuy.com 	| 89          	| 91            	| 100            	| 99  	| 100 	|



## Contributing

If you want to contribute please open an issue or send me an email hello@kburchardt.com. If not just give me a star.

## Authors

* **Konrad Burchardt** - *Initial work* - [Sundios](https://github.com/sundios)



