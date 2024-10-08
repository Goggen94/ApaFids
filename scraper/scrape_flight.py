import scrapy
from scrapy_playwright.page import PageCoroutine

class KefSpider(scrapy.Spider):
    name = "kef_spider"
    start_urls = ['https://fids.kefairport.is/site/apaops/?theme=%2Fthemes%2Fbootstrap.theme.darkly.min.css']

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            meta={
                "playwright": True,
                "playwright_page_coroutines": [
                    PageCoroutine("wait_for_selector", "table.table")
                ],
            },
            callback=self.parse
        )

    def parse(self, response):
        table = response.css('table.table')
        rows = table.css('tr')

        html_output = """
        <html>
        <head>
            <title>Flight Information</title>
            <meta http-equiv="refresh" content="600">
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
                    <th>Expected Time</th>
                    <th>Status</th>
                    <th>Gate</th>
                </tr>
        """

        for row in rows[1:]:
            cells = row.css('td')
            if len(cells) > 5:
                flight_number = cells[0].css('::text').get().strip()
                destination = cells[2].css('::text').get().strip()
                sched_time = cells[4].css('::text').get().strip()
                expected_time = cells[5].css('::text').get().strip()
                status = cells[7].css('::text').get().strip()
                gate = cells[9].css('::text').get().strip()

                html_output += f"""
                <tr>
                    <td>{flight_number}</td>
                    <td>{destination}</td>
                    <td>{sched_time}</td>
                    <td>{expected_time}</td>
                    <td>{status}</td>
                    <td>{gate}</td>
                </tr>
                """

        html_output += """
            </table>
        </body>
        </html>
        """

        # Lagre innholdet til index.html
        with open("scraper/output/index.html", "w", encoding="utf-8") as file:
            file.write(html_output)

        self.log("Flydata har blitt skrevet til index.html!")
