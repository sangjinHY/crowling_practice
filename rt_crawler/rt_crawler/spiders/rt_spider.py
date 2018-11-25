import scrapy

from rt_crawler.items import RTItem

#using scrapy crawl RottenTomatoes -o rt.csv
class RTSpider(scrapy.Spider) :
    #spider naming
    name = "RottenTomatoes"
    #allowed_domains
    allowed_domains = ["rottentomatoes.com"]
    #start_url
    start_urls = ["https://www.rottentomatoes.com/top/bestofrt/?year=2018"]

    #response of start_url
    def parse(self, response) :
        #print("start"+response.string)
        for tr in response.xpath('//*[@id="top_movies_main"]/div/table/tr') :
        # tr = response.xpath('//*[@id="top_movies_main"]/div/table/tr')
            href = tr.xpath('./td[3]/a/@href')
            url = response.urljoin(href[0].extract())
            yield scrapy.Request(url, callback=self.parse_page_contents, dont_filter=True)
    
    #response of "parse" function
    def parse_page_contents(self, response) :
         item = RTItem()
         item['title'] = response.xpath('//*[@id="heroImageContainer"]/a/h1/text()')[0].extract().strip()
         item['score'] = response.xpath('//*[@id="tomato_meter_link"]/span[2]/span/text()')[0].extract()
         #print(item['title'])
         yield item