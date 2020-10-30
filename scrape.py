from bs4 import BeautifulSoup
import requests
import csv
import argparse


arguments = argparse.ArgumentParser(
    description="This script will take any item you have provided the url and parse through each of items to see which one is the best price")
arguments.add_argument("-link",help='Provide the link of your search',dest='link')
arguments.add_argument("-price",help='Provide the link of your search',dest='price')
args = arguments.parse_args()
url = args.link
limit = float(args.price)


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
response = requests.get(url,headers=HEADERS)
soup = BeautifulSoup(response.content, 'lxml')

try:
    # FIX THIS
    soup.select('#availability .a-color-state')[0].text.strip()
    stock = 0

except:
    stock = 1
   
if stock:
    title = soup.find('span',id='productTitle').text.strip()
    try:
        price = float(soup.find(id='priceblock_ourprice').text.replace('.','').replace('€', '').replace(',','.').strip())

    except:
        try:
            price = float(soup.find(id='priceblock_saleprice').text.replace('$', '').replace(',', '').strip())
        except:
            price = ''
    
    print(price)

    try:
        review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-"]')[0].get_text().split(' ')[0].replace(",", "."))
        review_count = int(soup.select('#acrCustomerReviewText')[0].text.split(' ')[0].replace(".", ""))
    except:
        try:
            review_score = float(soup.select('i[class*="a-icon a-icon-star a-star-"]')[1].get_text().split(' ')[0].replace(",", "."))
            review_count = int(soup.select('#acrCustomerReviewText')[0].get_text().split(' ')[0].replace(".", ""))
        except:
            review_score = ''
            review_count = ''
  
    print(review_score)    

    try:
        if price < limit:
            print("Found a low price for: {}".format(title))
    except:
        pass



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