# IEC Common Data Dictionary to nodeset2.xml
This is a python-script that crawls the "IEC Common Data Dictionary". The IEC Common Data Dictionary specification is found here:
[IEC Common Data Dictionary](https://cdd.iec.ch/cdd/iec61360/iec61360.nsf/Welcome?OpenPage)

It then generates an [OPC UA](https://opcfoundation.org/about/opc-technologies/opc-ua/) nodeset2.xml document containing the relevant information. This file can then be imported to a UA-server.


## Dependencies
- Docker
- Python
- Splash
### Python libraries
- scrapy
- scrapy_splash


## Setup

### Splash 
Docker is mandatory for splash to work, meaning docker has to be installed before the following code can be executed

Linux: 
```bash
sudo docker pull scrapinghub/splash
sudo docker run -p 8050:8050 scrapinghub/splash
```
macOS/Windows:
```bash
docker pull scrapinghub/splash
docker run -p 8050:8050 scrapinghub/splash
```
Splash should now run at http://localhost:8050 
### Git
Then you have to install the project locally on your computer
```bash
git clone 'https://github.com/PrediktorAS/iec-cdd-to-nodeset2.git'
```

### Change directory
To install the dependecies and run the program you have to be in the root folder of the project  
```bash
cd IEC-CDD-TO-NODESET2
```

### Install dependencies
To install the necessarily dependencies, run the following code


Windows:
```bash
py -m pip install -r requirements.txt
```
Unix/macOS
```bash
python -m pip install -r requirements.txt
```

## Running
The application is split in two parts. One part of the program will crawl and scrape the website where the IEC dictionaries are located and the second part will use this information to build a OPC UA nodeset2.xml file. 
The two parts can easily be run separately or together from the CLI. 


### Run through CLI-script
This script is called `main.py`. The script has three different options; run the crawler, run the json-to-xml script or run both. 

<br>
Type in the following code in a terminal to run the crawler:

Windows: 
```bash
py main.py crawler
```
Unix/macOS:
```bash
python main.py crawler
```

<br>
Type in the following code in a terminal to run the json-to-xml script:

Windows: 
```bash
py main.py xml-builder
```
Unix/macOS:
```bash
python main.py xml-builder
```

<br>
Type in the following code in a terminal to run both:

Windows: 
```bash
py main.py both
```
Unix/macOS:
```bash
python main.py both
```
