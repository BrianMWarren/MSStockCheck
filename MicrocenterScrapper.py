import requests
from time import sleep
from datetime import datetime
from playsound import playsound
from lxml import html
import time


class MicrocenterScrapper(object):
    def __init__(self):
        #user agent spoof to fool site
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        self.header = {'User-Agent': user_agent}
        #product page that you wish to refresh to check stock
        self.URLRequests = ["https://www.microcenter.com/product/628318/asus-geforce-rtx-3080-tuf-gaming-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #asus tuff
                            "https://www.microcenter.com/product/631533/msi-geforce-rtx-3080-suprim-x-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #MSI GeForce RTX 3080 SUPRIM X
                            "https://www.microcenter.com/product/628330/msi-geforce-rtx-3080-gaming-x-trio-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #MSI GeForce RTX 3080 Gaming X Trio
                            "https://www.microcenter.com/product/628343/gigabyte-geforce-rtx-3080-eagle-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #Gigabyte GeForce RTX 3080 Eagle Overclocked Triple-Fan
                            "https://www.microcenter.com/product/628346/evga-geforce-rtx-3080-ftw3-ultra-gaming-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #EVGA GeForce RTX 3080 FTW3 Ultra Gaming Triple-Fan
                            "https://www.microcenter.com/product/628686/asus-geforce-rtx-3080-strix-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121", #ASUS GeForce RTX 3080 Strix Overclocked Triple-Fan
                            "https://www.microcenter.com/product/628331/msi-geforce-rtx-3080-ventus-3x-overclocked-triple-fan-10gb-gddr6x-pcie-40-graphics-card?storeid=121"] #MSI GeForce RTX 3080 Ventus 3X Overclocked Triple-Fan

        self.ProductName = ["Asus Tuff",
                            "MSI GeForce RTX 3080 SUPRIM X",
                            "MSI GeForce RTX 3080 Gaming X Trio",
                            "Gigabyte GeForce RTX 3080 Eagle Overclocked Triple-Fan",
                            "EVGA GeForce RTX 3080 FTW3 Ultra Gaming Triple-Fan",
                            "ASUS GeForce RTX 3080 Strix Overclocked Triple-Fan",
                            "MSI GeForce RTX 3080 Ventus 3X Overclocked Triple-Fan"]

        #location of the alert
        self.NOTIFICATION_SOUND_PATH = "Notification/alarm-frenzy-493.mp3"
        #sold out state of text
        self.inStockText = "in stock"
        self.inStock = False

        #main function, sleep hardcode is the amount of seconds between refreshes
        while not self.inStock:
            self.CheckForStock()
            sleep(30)

    def CheckForStock(self):
        try:
            for productNum in range(len(self.URLRequests)):
                with requests.get(self.URLRequests[productNum], headers=self.header) as url:
                    tree = html.fromstring(url.content)
                    #the xpath of the text object in the HTML page that will be checked
                    try:
                        stockText = tree.xpath("/html/body/main/article/div[3]/div[1]/div[1]/div/div[2]/div[1]/p/span/text()")[0]
                    except:
                        stockText = "none"
                        print("unexpected return from stock text location!")
                    
                    print("at " + str(datetime.now()) + " for " + self.ProductName[productNum] + " sock text is: " + str(stockText))
                    #Checks the text of the object, this hardcode string must be the exact sold out text
                if(str(stockText).lower() in (self.inStockText)):
                    self.inStock = True
                    print("at " + str(datetime.now()) + " ######################################STOCK FOUND######################################")
                    print("For " + self.ProductName[productNum])
                    # This is the In stock condition! Modify this line if you wish to have a different location. Plays terrible audio x times in a row
                    for num in range(10):
                        self.PlayAudio(self.NOTIFICATION_SOUND_PATH)

        except Exception as e:
            print("Network or scraping error in CheckForStock()")
            print(e)


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
