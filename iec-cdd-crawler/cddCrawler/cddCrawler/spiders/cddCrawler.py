import scrapy
import time
from scrapy_splash import SplashRequest

class cddSpider(scrapy.Spider):
    name = 'cddCrawler'

    def start_requests(self):
        #The url of the tree containing all the links with the dictionary information
        url = 'https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/Tree?Readform&BaseTarget=Main&ongletactif=1'

        #Gets the url through splash since the site is dynamic
        yield SplashRequest(url = url, callback = self.parse)

    def parse(self, response):
        #Sleeps for 0.5 seconds to prevent the server from crashing
        time.sleep(0.5)
        #Gets all the links inside the a-tags within class n 
        links = response.css('a.n::attr(href)').getall()

        #Checks if the current site contains node links
        #If the site does not contain node links, it is an information site
        if len(links) == 0:
            code = None
            name = None
            definition = None
            #Gets all td elements in table
            datas = response.css('td::text').getall()
            for index, data in enumerate(datas):  
                #If there is a match in the value of the td-element, the next td-element value will be saved in a variable                
                if data == '\nIRDI: ':
                    id = datas[index + 1][1:]

                if data == '\nCode: ':
                    if code == None:
                        code = datas[index + 1][1:]

                if data == '\nPreferred name: ':
                    if name == None:
                        name = datas[index + 1][1:]
                
                if data == '\nDefinition: ':
                    if definition == None:
                        definition = datas[index + 1][1:]

                if data == '\nVersion: ':
                    version = datas[index + 1][1:]

                if data == '\nRevision: ':
                    revision = datas[index + 1][1:]
            
            #Gets the td's sibling's child (a-element) to all the td elements with class label
            all_links = response.css('td.label + td > a::text').getall()

            #Returns the information in JSON format
            yield {
                    'code': code,
                    'id': id,
                    'name': name,
                    'superclass' : None if all_links == [] else (all_links[0] if all_links[0][:4] == '0112' else all_links[1]), #Checks if the link has a superclass. If it does not, the superclass is set to None
                                                                                                                                #If the first link starts with 0112, the superclass will be to the first link found on the page 
                                                                                                                                #If the first link do not start with 0112, the superclass will be set to the second link 
                    'definition' : definition,
                    'version' : version,
                    'revision' : revision
                }   
        #Runs if the site is a tree containing links to nodes  
        else:
            #Follows each link and runs the parse method with the new link
            for link in links:   
                new_link = 'https://cdd.iec.ch/cdd/iec61987/iec61987.nsf/' + link
                yield response.follow(new_link, callback=self.parse)

#TODO finne ut av virtual environment