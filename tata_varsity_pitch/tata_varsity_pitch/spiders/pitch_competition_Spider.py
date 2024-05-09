from datetime import datetime
import pyairtable
import scrapy
from scrapy.crawler import CrawlerProcess


class PitchCompetitionSpiderSpider(scrapy.Spider):
    name = "pitch_competition_Spider"
    start_urls = ["https://nacue.com/events/tata-varsity-pitch-competition.html"]
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'pitch_data.json'
    }

    def parse(self, response):
        links = response.css('div.single-team-area a::attr(href)').extract()
        for index, link in enumerate(links, start=1):
            yield scrapy.Request("https://nacue.com" + link, callback=self.parse_details, meta={'index': index})

    def parse_details(self, response):
        items = dict()

        business = response.css('.tlp-name::text').get()
        participants = ''.join(response.css('p:nth-child(6) ::text').extract()).strip('').split('FOUNDERS:')[1].replace(
            '\xa0', '')
        items['year'] = '2023'
        items['competition'] = 'Tata Varsity Pitch'
        items['lastupdate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items['winner business'] = business
        items['winner participants'] = participants

        yield items


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(PitchCompetitionSpiderSpider)
    process.start()
