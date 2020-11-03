'''
TODO: Scrape through each of the items whether hourly or in minutes
    Define the logic for looping through this URL will help:
    https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
    Update the lowest price found if another one is found that's lower than the limit
    Update the command line interface for better functionality

    UPDATE:
    Add file to sift through and see which items are available to purchase
    Budget argument is the whole bugdet for someone
'''


from bs4 import BeautifulSoup
import requests
import csv
import argparse


arguments = argparse.ArgumentParser(
    description="This script will take any item you have provided the url and parse through each of items to see which one is the best price")
arguments.add_argument("-link",help='Provide the link of your search',dest='link',required=True)
arguments.add_argument("-budget",help="Provide the price you're looking for",dest='budget')
arguments.add_argument("-file",help='Provide the file of items you would like to go through',dest='file')
args = arguments.parse_args()



def purchase_outcome(available,limit):
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
    
        if limit > 0:
            if price < limit:
                print("Found a low price for: {}".format(title))
                limit-=price
            else:
                print('You cannot buy this')
    else:
        print("Item is not available only available items will be analyzed")


'''
episodes = soup.find_all('div', class_='info')
def remove_str(votes):
    for r in ((',', ''), ('(', ''), (')', '')):
        votes = votes.replace(*r)
    return votes


for episode in episodes:
    try:
        title = episode.a['title']
        content = episode.meta['content']
        date = episode.find('div', class_='airdate').text.strip()

        rating = episode.find(
            'span', class_='ipl-rating-star__rating').text.strip()
        votes = episode.find(
            'span', class_='ipl-rating-star__total-votes').text.strip()
        votes = remove_str(votes)
        info = episode.find('div', class_='item_description').text.strip()

    except Exception as e:
        raise(e)
    csv_writer.writerow([title, content, date, rating, votes, info])

csv_file.close()
'''


if __name__ == "__main__":

    try:
        url = args.link
        limit = float(args.budget)
    except:
        url = args.link
        limit = None

    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url,headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')


    try:
        soup.select('#availability .a-color-state')[0].text.strip()
        stock = 0
    except:
        # checking if there is "Out of stock" on a second possible position
        try:
            soup.select('#availability .a-color-price')[0].text.strip()
            stock = 0
        except:
            stock = 1
    purchase_outcome(stock,limit)
