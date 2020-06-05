# SEO: Run multiple URLs and get ligthhouse V6 Scores.

Run lighthosue with multiple URLs and get different scores all in one master csv file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine. In this project we only have two important files:
	- lighthouse.sh
	- lighthouse.py

### Prerequisites

To run this project we need python3 and Lighthouse Node CLI. The Node CLI provides the most flexibility in how Lighthouse runs can be configured and reported. Users who want more advanced usage, or want to run Lighthouse in an automated fashion should use the Node CLI.


### Installing

**Lighthouse Node Cli Installation:**

```shell
npm install -g lighthouse
# or use yarn: 
# yarn global add lighthouse 
```

### Testing 

Once we install it we should test its running correclyt by opening a terminal window and running

```
lighthouse https://www.kburchardt.com
```

By default, Lighthouse writes the report to an HTML file. You can control the output format by passing flags. If you want more detail about the flags please check [the official documentation](https://www.npmjs.com/package/lighthouse)


### Shell script

Once we made our test we will go to our shell script (lighthouse.sh) and add our URLs on the <url> part.

For example:

```shell
lighthouse https://www.uselessthingstobuy.com --quiet --chrome-flags="--headless" --output=json --output-path=./json/report1.json --save-assets 
lighthouse https://www.uselessthingstobuy.com/gifts/gifts-for-women/ --quiet --chrome-flags="--headless" --output=json --output-path=./json/report2.json --save-assets
lighthouse https://www.uselessthingstobuy.com/gifts/gifts-under-25/ --quiet --chrome-flags="--headless" --output=json --output-path=./json/report3.json --save-assets
```

## Passed Flags

On the shell script we are passing the following flags:
	- ```--quiet --chrome-flags="--headless"``` :Is so that the shell script runs in headless mode and we can just leave it running on the backend.
	- ```--output=json --output-path=./json/report1.json ```: We want to save it as a Json file so that we can get the data with Python. We are also saving it in a specific path. *** Here we need to make sure that we change the report number to something different, if we dont do this then it will overwrite the report. I have no idea how to make a increment number on shell. But if somebody is reading this and knows how to do that so that we dont have to add it manually that would be great ***
	- ``` --save-assets ``` : To save the file.

## Running shell script

After you added all your URLs, we go to the terminal and go to our folder where the script lives and give the script executing rights.


```shell
chmod +x lighthouse.sh
```

After we do this we run our file by doing:

```shell
./lighthouse.sh
```

this will take some time, but all your json files should be exported to the `/json` folder.

### Python Script

Once we have all the desired Json Files we need to open our Python file and change one important thing. On line 16 there is a for loop that has a range. This range should be the same size of the amount of URLs you added on the shell file. For example if I run only 3 URLs we would change ``` range(19) ``` to ``` range(2)``` remember that python start  countring from 0.

``` python
#Remember to change the range number depending on how many urls you have. Default is 20.
    for k in range(19):  
        # returns JSON object as a dictionary
        f = open('json/report' + str(k + 1) + '.json')
        data = json.load(f)
```

Once we do this we are able tu run our ```get_scores()``` function. Once finished this will  output one master file with all your scores for your different URLs

** For Example: **

| url                                	| Performance 	| accessibility 	| best-practices 	| seo 	| pwd 	|
|------------------------------------	|-------------	|---------------	|----------------	|-----	|-----	|
| https://www.kburchardt.com         	| 80          	| 90            	| 100            	| 100 	| 100 	|
| https://www.uselessthingstobuy.com 	| 89          	| 91            	| 100            	| 99  	| 100 	|



## Contributing

If you want to contribute please open an issue or  send me an email hello@kburchardt.com . If not just give me a star/

## Authors

* **Konrad Burchardt** - *Initial work* - [Sundios](https://github.com/sundios)



