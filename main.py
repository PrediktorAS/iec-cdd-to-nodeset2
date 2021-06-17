import os
import sys

arguments = (str(sys.argv))
trimmed_arguments = arguments.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
li = list(trimmed_arguments.split(","))

if li[1] == 'both':
    os.system('cd iec-cdd-crawler/cddCrawler/cddCrawler & scrapy crawl cddCrawler -O ../../../nodes.json & cd ../../../ & python nodeset2Converter/filereader.py')

if li[1] == 'crawler':
    os.system('cd iec-cdd-crawler/cddCrawler/cddCrawler & scrapy crawl cddCrawler -O ../../../nodes.json')

if li[1] == 'xml-builder':
    os.system('python nodeset2Converter/filereader.py')