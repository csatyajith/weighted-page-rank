import json

import scrapy


class Spider(scrapy.Spider):
    name = "covid"
    start_urls = ["https://coronavirus.jhu.edu/"]
    COUNT_MAX = 100000

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': COUNT_MAX
    }

    def __init__(self):
        self.pc_file = open("parent_child_file.txt", "w")
        self.mapping = {}
        self.counter = 1

    def get_mapping(self, url):
        if url in self.mapping:
            return self.mapping[url]
        self.mapping[url] = self.counter
        self.counter += 1
        if self.counter == 100000:
            with open("mapping_file.json", "w") as mf:
                json.dump(self.mapping, mf)
        return self.mapping[url]

    def parse(self, response, **kwargs):
        parent = response.url
        parent_mapping = self.get_mapping(parent)
        yield {
            "url": response.url,
        }
        # now follow links to other pages
        for href in response.css('li a::attr(href)').getall():
            c = parent + href[1:] if href[0] == "/" else href
            self.pc_file.write("{} {}\n".format(parent_mapping, self.get_mapping(c)))
            yield response.follow(href, callback=self.parse)
