'''
TODO: Scrape through each of the items whether hourly or in minutes
    Define the logic for looping through this URL will help:
    https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
    Update the lowest price found if another one is found that's lower than the limit
    Update the command line interface for better functionality

    UPDATE:

'''

from bs4 import BeautifulSoup
import requests
import csv
import argparse


arguments = argparse.ArgumentParser(
    description="This script will take any item you have provided the url and parse through each of items to see which one is the best price")
arguments.add_argument("-link",help='Provide the link of your search',dest='link')
arguments.add_argument("-budget",help="Provide the price you're looking for",dest='budget',required=True)
arguments.add_argument("-file",help='Provide the file of items you would like to go through',dest='file')
arguments.add_argument("-csv",help='Provide the file of items you would like to go through',dest='csv')
args = arguments.parse_args()



HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

class Scraper:

    def __init__(self,limit,file="",link="",csv=False):
        self.limit = float(limit)
        self.products = {}
        self.URLS = []
        self.file = file
        self.link = link
        self.csv = bool(csv)

        if self.file:
            f = open(self.file,"r")
            self.URLS = [line for line in f]
            

    def get_purchase_outcome(self,url):
        response = requests.get(url,headers=HEADERS)
        soup = BeautifulSoup(response.content, 'lxml')

        try:
            soup.select('#availability .a-color-state')[0].text.strip()
            available = 0
        except:
            # checking if there is "Out of stock" on a second possible position
            try:
                soup.select('#availability .a-color-price')[0].text.strip()
                available = 0
            except:
                available = 1


        if available:
            title = soup.find('span',id='productTitle').text.strip()
            try:
                price = float(soup.find(id='priceblock_ourprice').text.replace('$','').replace(',','').strip())
            
            except:
                try:
                    price = float(soup.find(id='priceblock_saleprice').text.replace('$','').replace(',','').strip())
                except:
                    price = ''
            try:
                review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-5"]')[0].text.split(' ')[0])
                review_count = int(soup.select('#acrCustomerReviewText')[0].text.split(' ')[0].replace(",", ""))
            except:
                try:
                    review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-5"]')[1].text.split(' ')[0])
                    review_count = int(soup.select('#acrCustomerReviewText')[0].text.split(' ')[0].replace(",", ""))
                except:
                    review_score = ''
                    review_count = ''
        
            if self.limit > 0:
                if price < self.limit:
                    print("Found a price for: {}".format(title))
                    print("This item is ${}".format(price))
                    self.limit-=price
                    self.products[title] = price
                else:
                    print('You cannot buy this, you went over the budget')
        else:
            print("Item is not available only available items will be analyzed")
            pass
    

    def get_outcomes(self):
        for url in self.URLS:
            self.get_purchase_outcome(url)

    def get_outcome(self):
        return self.get_purchase_outcome(self.link)
    
    def extract_to_CSV(self):
        results = open("results.csv",'w')
        results_writer = csv.writer(results)
        results_writer.writerow(["Title","Price (US Dollars)"])
        for key,value in self.products.items():
            results_writer.writerow([key,value])

    def execute(self):
        if self.URLS:
            self.get_outcomes()
        else:
            self.get_outcome()
        
        if self.csv:
            self.extract_to_CSV()


if __name__ == "__main__":
    scraper = Scraper(args.budget,args.file,args.link,args.csv)
    scraper.execute()
