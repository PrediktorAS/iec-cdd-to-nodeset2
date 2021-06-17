import scrapy
import time
from scrapy_splash import SplashRequest

class cddSpider(scrapy.Spider):
    name = 'cddCrawler'

    def start_requests(self):
        #The urls of the trees containing all the links with the dictionary information
        url = 'https://cdd.iec.ch/cdd/iec61360/iec61360.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1'
        url2 = 'https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1'
        url3 = 'https://cdd.iec.ch/cdd/iec62683/iec62683.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1'

        #Gets the url through splash since the website is dynamic
        yield SplashRequest(url = url, callback = self.parse)
        yield SplashRequest(url = url2, callback = self.parse)
        yield SplashRequest(url = url3, callback = self.parse)

    def parse(self, response):
        #Sleeps for 0.5 seconds to prevent the server from crashing
        time.sleep(0.5)
        #Gets all the links inside the a-tags within class n 
        links = response.css('a.n::attr(href)').getall()
        #Checks if the current site contains node links
        #If the site does not contain node links, it is an information site
        if len(links) == 0:
            #Gets all td elements in the table containing all the information
            datas = response.css('td::text').getall()
            #The values are the text within a td-element
            #The values that are wanted, are added to this list
            values = {
                '\nIRDI: ': '',            
                '\nCode: ': '',         
                '\nPreferred name: ': '',
                '\nDefinition: ': '',
                '\nVersion: ': '',
                '\nRevision: ': '',
            }
 
            for index, data in enumerate(datas):  
                #If there is a match in the value of the td-element, the next td-element value will be saved in a variable    
                for value in values:
                    if value == data and not values[value]:
                        values[value] = datas[index + 1][1:]
            all_tds = response.css('td').getall()
            for index, td in enumerate(all_tds): 
                if 'Superclass' in td:
                    specific_td = all_tds[index + 1].replace('%23', '#').replace('-','/')
                    superclass = specific_td[135:(135 + len(values['\nCode: ']))]
                    if superclass[:4] != '0112':
                        superclass = None

            #Returns the information in JSON format
            yield {
                    'library' : response.url[26:31],
                    'code': values['\nCode: '],
                    'id': values['\nIRDI: '],
                    'name': values['\nPreferred name: '],
                    'superclass' : superclass,
                    'definition' : values['\nDefinition: '],
                    'version' : values['\nVersion: '],
                    'revision' : values['\nRevision: ']
                }   
        #Runs if the site is a tree containing links to nodes  
        else:
            if response.url == 'https://cdd.iec.ch/cdd/iec61360/iec61360.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1':
                #Follows each link and runs the parse method with the new link
                for link in links:   
                    new_link = 'https://cdd.iec.ch/cdd/iec61360/iec61360.nsf/' + link
                    yield response.follow(new_link, callback=self.parse)

            if response.url == 'https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1':
                #Follows each link and runs the parse method with the new link
                for link in links:   
                    new_link = 'https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/' + link
                    yield response.follow(new_link, callback=self.parse)

            if response.url == 'https://cdd.iec.ch/cdd/iec62683/iec62683.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1':
                #Follows each link and runs the parse method with the new link
                for link in links:   
                    new_link = 'https://cdd.iec.ch/cdd/iec62683/iec62683.nsf/' + link
                    yield response.follow(new_link, callback=self.parse)