import scrapy


class IndiangoSpider(scrapy.Spider):
    name = 'IndiaNGO'
    allowed_domains = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']
    start_urls = ['https://www.indiangoslist.com/ngo-address/achukuru-welfare-society-in-itanagar-arunachal-pradesh_AR-2009-0015817']

    def parse(self, response):
        ngo_left = response.css(".ngo_left_head::text").extract()
        ngo_right = response.css(".ngo_right_head::text").extract()
        span = response.xpath("//*[@class='ngo_right_head']//text()").extract()
        print(ngo_right)
        print(span)
        count_1 = 0
        count_2 = 0
        for i in range(len(span)):
            if span[i] == ' ':
                count_1 += 1
            elif span[i] == '\n':
                count_2 += 1
        for _ in range(count_1):
            span.remove(' ')
        for _ in range(count_2):
            span.remove('\n')
        print(span)
        span = span[0:len(ngo_left)]
        span[len(span)-4] = span[len(span)-4] + span[len(span)-3]
        span = span[0:len(span)-3] + span[len(span)-2:]
        print(span)
        for item in zip(ngo_left,span):

            scraped = {
                'name' : item[0],
                'description' : item[1]
            }
            yield scraped
        pass