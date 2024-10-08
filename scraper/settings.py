BOT_NAME = 'scraper'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'

# For å kjøre Scrapy headless uten å bli blokkert
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
ROBOTSTXT_OBEY = False

# Eksport til JSON-fil
FEED_FORMAT = 'json'
FEED_URI = 'output/flight_data.json'
