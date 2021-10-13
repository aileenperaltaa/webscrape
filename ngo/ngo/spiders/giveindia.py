import scrapy

class GiveIndiaSpider(scrapy.Spider):
    name = "GiveIndia"

    start_urls = [
        'https://www.giveindia.org/certified-indian-ngos',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'ngos-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')