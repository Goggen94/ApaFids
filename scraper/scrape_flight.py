import scrapy
from scrapy_playwright.page import PageCoroutine
from bs4 import BeautifulSoup
import os

class FlightSpider(scrapy.Spider):
    name = "flight_spider"
    start_urls = ['https://fids.kefairport.is/site/apaops/?theme=%2Fthemes%2Fbootstrap.theme.darkly.min.css&sorts[arr_dep]=1&sorts[sched_time]=1&sorts[expected_time]=1&sorts[block_time]=1']

    custom_settings = {
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",  # Bruk Chromium for å rendere JavaScript
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    PageCoroutine("wait_for_selector", "table")  # Vent på at tabellen skal vises
                ],
            },
            callback=self.parse
        )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finn tabellen med flyinformasjon
        table = soup.find('table', {'class': 'table'})
        
        if table:
            # Generer HTML-fil med scraped data
            html_output = """
            <html>
            <head>
                <title>Flight Information</title>
                <meta http-equiv="refresh" content="600">  <!-- Oppdater hver 10. minutt -->
                <style>
                    table { width: 100%; border-collapse: collapse; }
                    th, td { padding: 8px 12px; border: 1px solid black; text-align: left; }
                    th { background-color: #4CAF50; color: white; }
                </style>
            </head>
            <body>
                <h2>KEF Airport Flight Information</h2>
                <table>
                    <tr>
                        <th>Flight Number</th>
                        <th>Destination</th>
                        <th>Scheduled Time</th>
                        <th>Status</th>
                    </tr>
            """

            # Gå gjennom rader og celler i tabellen
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) > 3:
                    flight_number = cells[0].text.strip()
                    destination = cells[1].text.strip()
                    scheduled_time = cells[2].text.strip()
                    status = cells[3].text.strip()

                    html_output += f"""
                    <tr>
                        <td>{flight_number}</td>
                        <td>{destination}</td>
                        <td>{scheduled_time}</td>
                        <td>{status}</td>
                    </tr>
                    """

            html_output += """
                </table>
            </body>
            </html>
            """

            # Lagre filen
            os.makedirs("output", exist_ok=True)
            with open("output/index.html", "w", encoding="utf-8") as file:
                file.write(html_output)

            print("Data har blitt skrevet til index.html i tabellformat!")
        else:
            print("Ingen flydata funnet.")

