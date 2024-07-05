import scrapy

class HTMLSpider(scrapy.Spider):
    name = 'html_spider'
    
    # URL to scrape
    start_urls = ['https://googlevertexai.devpost.com/']  # Change this URL to the one you want to scrape

    def parse(self, response):
        # Extract HTML code
        html_code = response.body.decode(response.encoding)
        print(html_code)
        # Save HTML code to a text file
        filename = 'scraped_html.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_code)

        self.log(f'Saved HTML to {filename}')