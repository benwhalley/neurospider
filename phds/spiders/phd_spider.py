import scrapy


class PhdSpider(scrapy.Spider):
    name = "phds"

    start_urls = [
        # "https://www.findaphd.com/search/phd.aspx?keywords=brain+imaging",
        "https://www.findaphd.com/search/phd.aspx?keywords=human+neuroscience"
    ]

    def parse_phd(self, response):

        page = response.url.split("?")[-1]
        filename = "__phd-%s.html" % page

        with open(filename, "wb") as f:
            f.write(response.body)
        self.log("Saved file %s" % filename)

        yield {
            "url": response.url,
            "description": "".join(response.css("#Description").extract()),
            "title": "".join(response.css("#H1Area h1::text").extract()).strip(),
        }

    def parse(self, response):
        page = response.url.split("?")[-1]

        print("pagelinks")
        print(response.css(".pagi1ngArea a::attr(href)").extract())

        for href in response.css(".courseLink").css("a::attr(href)").extract():
            yield response.follow(href, callback=self.parse_phd)

        # for href in response.css(".pagi1ngArea a::attr(href)").extract():
        #     yield response.follow(href, callback=self.parse)

        filename = "__phd-list-%s.html" % page
        with open(filename, "wb") as f:
            f.write(response.body)
