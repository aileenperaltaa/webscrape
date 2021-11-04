import scrapy


class SecondbotSpider(scrapy.Spider):
    name = 'secondbot'
    allowed_domains = ['https://www.investindia.gov.in/bip/resources/list-ngos-providing-relief-during-covid-19']
    start_urls = ['https://www.investindia.gov.in/bip/resources/list-ngos-providing-relief-during-covid-19']

    def parse(self, response):
        #Extracting the content using css selectors
        a = response.css("tr")
                #Give the extracted content row wise
        for tr in a[1:]:
            #create a dictionary to store the scraped info
            b = tr.css("td")
            name = b[0].css("::text").extract()[0]
            description = " ".join(b[1].css("p::text").extract())
            if not description:
                description = b[1].css("::text").extract()[0]
            state = b[2].css("td::text").extract()[0]
            emails = "None"
            emails = b[3].css("p::text").extract()
            Contact = "\n  ".join(b[3].css("a::attr(href)").extract())
            scraped_info = {
                'Name' : name,
                'Description': description,
                'State': state,
                'Contact' : Contact,
                "Email" : emails
            }

            #yield or give the scraped info to scrapy
            yield scraped_info


