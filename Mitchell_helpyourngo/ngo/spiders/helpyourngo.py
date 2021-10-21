import re
import scrapy


class HelpYourNgoSpider(scrapy.Spider):
    name = 'HelpYourNgo'
    allowed_domains = ['https://www.helpyourngo.com/']
    start_urls = [
        'https://www.helpyourngo.com/ngo-details.php?ngo=249&name=Aai-Caretaker&ngo_sect_id=snapshot',
        'https://www.helpyourngo.com/ngo-details.php?ngo=1564&name=Abhinav&ngo_sect_id=snapshot',
        'https://www.helpyourngo.com/ngo-details.php?ngo=242&name=Aarambh-Trust&ngo_sect_id=snapshot'
    ]

    def parse(self, response):

        # For the daanmatch_ngo table
        name = response.css(".font24::text").extract_first()
        last_updated = response.css(".fitexthdr_new:nth-child(4)::text").extract_first()
        address = response.css(".valign\=~ .font11+ .font11::text").extract_first()
        mobile = response.css("tr:nth-child(4) .font11~ .font11+ .font11::text").extract_first()
        email = response.css("tr:nth-child(2) .font11 a::text").extract_first()
        website = response.css(".currbrd tr:nth-child(3) a::text").extract_first()
        
        # Description is separated into multiple sections
        description_parts = response.css(".font11 td .font12::text , .font12 li::text, .font12 p::text").extract()
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
