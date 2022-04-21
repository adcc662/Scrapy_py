import scrapy

#Title = //h1/a/text()
#Citas = //span[@class="text" and @itemprop="text"]/text()
#Top ten tags = //div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()
#Next page button = //ul[@class="pager"]/li[@class="next"]/a/@href
#authors = //div[@class="quote"]/span/small[@class="author" and @itemprop="author"]/text()

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com'
    ]
    custom_settings = {
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT' : 'json',
        'CONCURRENT_REQUEST' : 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL':['adcc.97@outlook.com'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'DavidC',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
            authors = kwargs['authors']
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())
        authors.extend( response.xpath('//div[@class="quote"]/span/small[@class="author" and @itemprop="author"]/text()').getall())

        next_page_button = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})
            # yield response.follow(next_page_button, callback=self.parse_only_authors, cb_kwargs={'authors': authors})
        else:
            yield{
                'quotes': quotes,
                'authors' : authors
            }


    def parse(self, response):
      
        # print(response.status, response.headers)
        title = response.xpath('//h1/a/text()').get()
        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()
        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()
        authors = response.xpath('//div[@class="quote"]/span/small[@class="author" and @itemprop="author"]/text()').getall()

        for author in authors:
            print(author)
        

        top = getattr(self, 'top', None)
        if top:
            top = int(top)
            top_tags = top_tags[:top]
        


        yield{
            'title': title,
            'top_tags': top_tags,  
        }
        next_page_button = response.xpath('//ul[@class="pager"]/li[@class="next"]/a/@href').get()
        if next_page_button:
            yield response.follow(next_page_button, callback=self.parse_only_quotes, cb_kwargs={'quotes': quotes, 'authors': authors})
            # yield response.follow(next_page_button, callback=self.parse_only_authors, cb_kwargs={'authors': author})

        
        