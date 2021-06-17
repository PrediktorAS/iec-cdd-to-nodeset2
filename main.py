import os
import sys

#Gets the arguments from the CLI
arguments = (str(sys.argv))
#Removes unnecessary characters 
trimmed_arguments = arguments.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
#Makes a list out of the arguments
li = list(trimmed_arguments.split(","))

#Runs command line commands 
#It it decided by the second argument which part of the program is runned
if li[1] == 'both':
    os.system('cd iec-cdd-crawler/cddCrawler/cddCrawler & scrapy crawl cddCrawler -O ../../../nodes.json & cd ../../../ & python nodeset2-converter/json2xml.py')

if li[1] == 'crawler':
    os.system('cd iec-cdd-crawler/cddCrawler/cddCrawler & scrapy crawl cddCrawler -O ../../../nodes.json')

if li[1] == 'xml-builder':
    os.system('python nodeset2-converter/json2xml.py')