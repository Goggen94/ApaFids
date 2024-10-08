import scrapy

class KefSpider(scrapy.Spider):
    name = "kef_spider"
    start_urls = ['https://fids.kefairport.is/site/apaops/']

    def parse(self, response):
        # Finn data fra tabellen og lagre informasjonen
        table = response.css('table.table')
        
        # Hvis det ikke finnes noen tabell, logg en feilmelding
        if not table:
            self.log("No table found on the page. Check the selector!")
            return

        for row in table.css('tr')[1:]:  # Hopp over header
            cells = row.css('td')
            if len(cells) > 3:
                yield {
                    'flight_number': cells[0].css('::text').get(),
                    'destination': cells[2].css('::text').get(),
                    'scheduled_time': cells[4].css('::text').get(),
                    'expected_time': cells[5].css('::text').get(),
                    'status': cells[7].css('::text').get(),
                    'gate': cells[9].css('::text').get(),
                }
