import requests
from time import sleep
from datetime import datetime
from playsound import playsound
from lxml import html


class MicrocenterScrapper(object):
    def __init__(self):
        #user agent spoof to fool site
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        self.header = {'User-Agent': user_agent}
        #product page that you wish to refresh to check stock
        self.URLRequest = "https://www.microcenter.com/product/628318/asus-geforce-rtx-3080-tuf-gaming-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121"
        #location of the alert
        self.NOTIFICATION_SOUND_PATH = "Notification/alarm-frenzy-493.mp3"
        #sold out state of text
        self.soldOutStockText = "Sold Out"
        self.inStock = False

        #main function, sleep hardcode is the amount of seconds between refreshes
        while not self.inStock:
            self.CheckForStock()
            sleep(30)

    def CheckForStock(self):
        try:
            with requests.get(self.URLRequest, headers=self.header) as url:
                tree = html.fromstring(url.content)
                #the xpath of the text object in the HTML page that will be checked
                stockText = tree.xpath("/html/body/main/article/div[3]/div[1]/div[1]/div/div[2]/div[1]/p/span/text()")[0]
                
                print("at " + str(datetime.now()) +  " sock text is: " + str(stockText))
                #Checks the text of the object, this hardcode string must be the exact sold out text
            if(str(stockText) != self.soldOutStockText):
                self.inStock = True
                print("at " + str(datetime.now()) + " ######################################STOCK FOUND######################################")
                # This is the In stock condition! Modify this line if you wish to have a different location. Plays terrible audio x times in a row
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
