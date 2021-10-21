import scrapy


class TablebotSpider(scrapy.Spider):
    name = 'tablebot'
    allowed_domains = ['https://www.indialawyers.org/list-of-ngos-in-india/']
    start_urls = ['https://www.indialawyers.org/list-of-ngos-in-india/']

    def parse(self, response):
        #Extracting the content using css selectors
        a = response.css("tr")
                #Give the extracted content row wise
        for tr in a[1:]:
            #create a dictionary to store the scraped info
            b = tr.css("td::text").extract()
            scraped_info = {
                'Name' : b[0],
                'Address' : b[1],
                'Email' : b[2],
                'Contact' : b[3],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info

