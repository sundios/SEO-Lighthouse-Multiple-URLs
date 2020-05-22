#Add your URLs on <url>
#We are running lighthouse headless and saving the output as a json file on the /json folder
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report1.json --save-assets 
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report2.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report3.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report4.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report5.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report6.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report7.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report8.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report9.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report10.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report11.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report12.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report13.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report14.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report15.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report16.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report17.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report18.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report19.json --save-assets
lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=./json/report20.json --save-assets
#Add more URLs by copying the last line. ** Make sure to change the output-path report number to something different if not it will overwrite the file.
#I have no idea how to make a variable that counts up in bash so it has to be done manually


