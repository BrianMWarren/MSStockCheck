import requests
from time import sleep
from datetime import datetime
from playsound import playsound
from lxml import html


class MicrocenterScrapper(object):
    def __init__(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        self.header = {'User-Agent': user_agent}
        self.URLRequest = "https://www.microcenter.com/product/630285/amd-ryzen-5-5600x-vermeer-37ghz-6-core-am4-boxed-processor-with-wraith-stealth-cooler?storeid=181"
        self.NOTIFICATION_SOUND_PATH = "Notification/alarm-frenzy-493.mp3"
        self.inStock = False

        while not self.inStock:
            self.CheckForStock()
            sleep(30)

    def CheckForStock(self):
        try:
            with requests.get(self.URLRequest, headers=self.header) as url:
                tree = html.fromstring(url.content)
                stockText = tree.xpath("/html/body/main/article/div[3]/div[1]/div[1]/div/div[3]/div[1]/p/span/text()")[0]
                print("at " + str(datetime.now()) +  " sock text is: " + str(stockText))
            if(str(stockText) != "Sold Out"):
                self.inStock = True
                print("######################################STOCK FOUND######################################")
                for num in range(10):
                    self.PlayAudio(self.NOTIFICATION_SOUND_PATH)

        except Exception as e:
            print("network or scrapping error!   " + e)


    def PlayAudio(self, audio_file=None, **kwargs):
        try:
            # See https://github.com/TaylorSMarks/playsound
            playsound(audio_file, True)
        except Exception as e:
            print(e)
            print(
                "Error playing notification sound. Disabling local audio notifications."
            )
            self.enabled = False

if __name__ == "__main__":
    MicrocenterScrapper()
