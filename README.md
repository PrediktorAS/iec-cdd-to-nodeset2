# iec-cdd-to-nodeset2
This is a python-script that crawls the "IEC 61987 - Common Data Dictionary" specification found here:
https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/TreeFrameset?OpenFrameSet&ongletactif=1. It then generates a nodeset2.xml document containing the relevant information. This file can then be transferred to a ua-server.


## Dependencies
- Docker
- Python
- Splash


## Setup
docker
git clone
...

## Running
The application is split in three parts. One is a used to run the two other scripts through a CLI. One is used to crawl the specification website and generate a .json file. While the third script is used to read the .json file and genrate the .xml file. 
To run the program ...
