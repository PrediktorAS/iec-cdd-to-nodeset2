# IEC Common Data Dictionary to nodeset2.xml
This is a python-script that crawls the "IEC Common Data Dictionary" specification found here:
[IEC Common Data Dictionary](https://cdd.iec.ch/cdd/iec61360/iec61360.nsf/Welcome?OpenPage)

It then generates a nodeset2.xml document containing the relevant information. This file can then be transferred to a ua-server.


## Dependencies
- Docker
- Python
- Splash
### Python libraries
- minidom
- json
- scrapy
- time
- scrapy_splash


## Setup

### Splash 
Docker is mandatory for splash to work
```bash
docker pull scrapinghub/splash
docker run -p 8050:8050 scrapinghub/splash
```
Splash should now run at http://localhost:8050 
### Git
Then you have to install the project locally on your computer
```bash
git clone 'http...'
```

## Running
The application is split in three parts. One part of the program will crawl and scrap the website where the IEC dictionaries are located and the second part will use this information to build a nodeset2.xml file. The third part puts the two other parts together so the application can easily be run from the CLI. 

To run the program you have to be in the root folder of the project  
```bash
cd root_folder
```
### Run through CLI-script
This script is called `main.py`. The script has three different options; run the crawler, run the json-to-xml script or run both. 

Type in the following code in a terminal to run the crawler:
```bash
python main.py crawler
```
Type in the following code in a terminal to run the json-to-xml script:
```bash
python main.py xml-builder
```
Type in the following code in a terminal to run both:
```bash
python main.py both
```
