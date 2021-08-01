import scrapy
import io
import csv
from datetime import datetime

class nepremicnineSpider(scrapy.Spider):
    name = "nepremicnine"

    start_urls = ['https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/cena-do-300000-eur/?s=16&nadst%5B0%5D=vsa&nadst%5B1%5D=vsa']

    def parse(self, response):

        table = []
        foundLast = False
        now = datetime.now()  # current date and time
        datum = now.strftime("%d/%m/%Y")
        ids = []
        filename = 'Link to csv file'

        with open(filename, "r", encoding="utf-8", newline="") as fp:
            reader = csv.reader(fp, delimiter=',')

            for row in reader:
                if(len(row) != 0):
                    ids.append(int(row[0]))


        for oglasi in response.css('div[itemprop="item"]'):
            try:
                naslov = oglasi.css("span.title::text").get().replace('š', "s").replace("ž", "z").replace("č", "c").replace("ć", "c").replace('Š', "S").replace("Ž", "Z").replace("Č", "C").replace("Ć", "C")
                id =  oglasi.css("a::attr(title)").get()

                podjetje = oglasi.css("span.agencija::text").get()
                if(podjetje != "Zasebna ponudba"):
                    podjetje="Podjetje"
                cena = oglasi.css("span.cena::text").get()[:-5]
                leto = oglasi.css("span.leto strong::text").get()
                velikost =  oglasi.css("span.velikost::text").get()[:-3]
                vsebina = oglasi.css("div.kratek::text").get().replace('š', "s").replace("ž", "z").replace("č", "c").replace("ć", "c").replace('Š', "S").replace("Ž", "Z").replace("Č", "C").replace("Ć", "C")
                tip = oglasi.css("span.tipi::text").get().replace('š', "s").replace("ž", "z").replace("č", "c").replace("ć", "c").replace('Š', "S").replace("Ž", "Z").replace("Č", "C").replace("Ć", "C")
                nakvadrat = int(cena.replace('.', '')) / int(velikost.replace(',', ''))

                table.append([id, datum, tip, cena, velikost, leto, podjetje, naslov, vsebina])
                print(id, datum, tip, cena, velikost, nakvadrat, leto, podjetje, naslov, vsebina)

                if int(id) in ids:
                    foundLast = True
                    yield {"id": id}
                    break
            except:
                pass

        with open(filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=',')
            for row in table:
                print(row)
                writer.writerow(row)

        if not foundLast:
            next_pages = response.css("li.paging_next a::attr(href)").get()
            try:
                yield response.follow(next_pages, callback=self.parse)
            except:
                yield{"The end"}


