import scrapy

# A limitation (or a bug) on pages pagination on the website:
    # 1) Navigate to page 1900: https://www.theguardian.com/australia-news/all?page=1900
    # 2) Scroll down then click next to go to the next page
    # 3) You will be re-directed to the main page again https://www.theguardian.com/australia-news
MAX_PAGES = 1900

class AustraliaSpider(scrapy.Spider):
    name = "australia"
    allowed_domains = ["www.theguardian.com"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "theguardian.pipelines.TheguardianPipeline": 300
        }
        
    }

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.theguardian.com/australia-news/all',
            callback=self.page,
            meta = {
                "page_no": 1
            }
        )

    
    def page(self, response):
        page_no = response.meta["page_no"]
        articles = response.xpath("//div[@class='u-cf index-page']/section/div/div//div[contains(@class, 'fc-item ')]")
        
        for article in articles:
            url = article.xpath(".//div[@class='fc-item__header']//a[@data-link-name='article']/@href").get()
            uid = article.xpath(".//@data-id").get()
            yield scrapy.Request(
            url=url,
            callback=self.articles,
            meta = {
                    "uid": uid
                }
        )

        while page_no <= MAX_PAGES:
            page_no +=1
            yield scrapy.Request(
                url=f'https://www.theguardian.com/australia-news/all?page={page_no}',
                callback=self.page,
                meta = {
                    "page_no": page_no
                }
        )   

    def articles(self, response):
        
        # save the html to be archived
        html = response.body
        
        # article objects
        uid = response.meta['uid']
        s_uid = hash(uid)
        title = response.xpath("//div[@data-gu-name='headline']//h1/text()").get()
        author = response.xpath("//a[@rel='author']/text()").get()
        category = response.xpath("//a[@data-link-name='article section']/span/text()").get()
        
        # record example: 25 Sep 2023 14.37 BST
        publication_object = response.xpath("//details[@class='dcr-1tedu3j']//span[@class='dcr-u0h1qy']/text()").get()
        pubilication_dt, pubilication_tz = self.extract_publication_date_info(publication_object)

        # record example: 'Last modified on 25 Sep 2023 14.37 BST'
        last_modified_object = response.xpath("//details[@class='dcr-1tedu3j']/text()").get()
        last_modified_dt, last_modified_tz = self.extract_last_modified_date_info(last_modified_object)

        url = response.url
        references = response.xpath("//div[@id='maincontent']/div/p/a/@href").getall()

        content = " ".join(response.xpath("//div[@id='maincontent']/div/p//text()").getall())

        yield {
            'uid': uid,
            's_uid': s_uid,
            'title': title,
            'author':author,
            'category': category,
            'references': references,
            'pubilication_dt': pubilication_dt,
            'pubilication_tz': pubilication_tz,
            'last_modified_dt': last_modified_dt,
            'last_modified_tz': last_modified_tz,
            'url': url,
            'content': content
        }

    def extract_publication_date_info(self, publication_object):
        if publication_object:
            publication_object_list = publication_object.split(" ")
            pubilication_dt = " ".join(publication_object_list[:-1])
            
            pubilication_tz = publication_object_list[-1]

            return pubilication_dt, pubilication_tz

        return None, None

    def extract_last_modified_date_info(self, last_modified_object):
            if last_modified_object:
                # clean object
                last_modified_object_list = last_modified_object.split("on ")[-1].split(" ")
                
                # extract data
                last_modified_dt = " ".join(last_modified_object_list[:-1])
                last_modified_tz = last_modified_object_list[-1]

                return last_modified_dt, last_modified_tz

            return None, None