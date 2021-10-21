import re
import scrapy


class HelpYourNgoSpider(scrapy.Spider):
    name = 'HelpYourNgo'
    # allowed_domains = ['https://www.helpyourngo.com/ngos-by-region-v1.php']
    start_urls = ['https://www.helpyourngo.com/ngos-by-region-v1.php']


    def parse(self, response):
        ngo_links = response.css('.font14 a')
        yield from response.follow_all(ngo_links, self.parse_ngo)


    def parse_ngo(self, response):
        ngo_summary = response.css('.activediv+ .newtabdiv a::attr(href)').get()
        if ngo_summary is not None:
            yield response.follow(ngo_summary, self.parse_ngo_summary)


    def parse_ngo_summary(self, response):
        # For the daanmatch_ngo table
        name = response.css(".font24::text, .font19::text").extract_first()
        address = response.css(".valign\=~ .font11+ .font11::text").extract_first()
        mobile = response.css("tr:nth-child(4) .font11~ .font11+ .font11::text").extract_first()
        email = response.css("tr:nth-child(2) .font11 a::text").extract_first()
        website = response.css(".currbrd tr:nth-child(3) a::text").extract_first()
        
        # Get latest updated year
        last_updated_years = response.css(".fitexthdr_new+ .fitexthdr_new::text").extract()
        if last_updated_years:
            last_updated = last_updated_years[-1]
        else:
            last_updated = None

        # Description is separated into multiple sections
        description_parts = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "font11", " " ))]//td//*[contains(concat( " ", @class, " " ), concat( " ", "font12", " " ))]/descendant::text()').extract()
        description = ' '.join(description_parts)
        description = re.sub('\r', '', description) # Need to remove escape chars
        description = re.sub('\n', '', description)
        description = re.sub('\t', '', description)

        # For the finance table
        annual_expenditure = response.css(".fitextrow_new:nth-child(25) .fitextsubhdr_new:nth-child(4)::text").extract_first()

        yield {
            'name' : name,
            'last_updated' : last_updated,
            'address' : address,
            'mobile' : mobile,
            'email' : email,
            'website' : website,
            'annual_expenditure' : annual_expenditure,
            'description' : description,
        }
