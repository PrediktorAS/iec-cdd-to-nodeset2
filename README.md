# iec-cdd-to-nodeset2
This is a python-script that crawls the "IEC 61987 - Common Data Dictionary" specification found here:
https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/TreeFrameset?OpenFrameSet&ongletactif=1. It then generates a nodeset2.xml document containing the relevant information. This file can then be transferred to a ua-server.


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
The application is split in three parts. One is a used to run the two other scripts through a CLI. One is used to crawl the specification website and generate a .json file. While the third script is used to read the .json file and genrate the .xml file.  
To run the program you have to be in the root folder of the project  
```bash
cd root_folder
```
### Run through CLI-script
This script is called `main.py`. You start it with the following code in a terminal
```bash
python main.py
```
The script will then start and give you some options....
