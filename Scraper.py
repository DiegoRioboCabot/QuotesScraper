import os
import csv
import requests

from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path 

# Lists that will contain dictionaries  | Fields :
list_quotes = []                        # quote, author, tags, link to author' bio
list_authors = []                       # author, country, birth date, bio
set_authors = set()

months_dict = dict(
            JANUARY = '01',
            FEBRUARY = '02',
            MARCH = '03',
            APRIL = '04',
            MAY = '05',
            JUNE = '06',
            JULY = '07',
            AUGUST = '08',
            SEPTEMBER = '09',
            OCTOBER = '10',
            NOVEMBER = '11',
            DECEMBER = '12')

#Base URL
url = ''
url_home = 'http://quotes.toscrape.com'

#============================================
#Loop to scrape through all pages with quotes
#============================================
while True:
    print(f'Scraping {url_home}{url}')
    altoguiso = BeautifulSoup(requests.get(url_home + url).text,'html.parser')

    for quote in altoguiso.select(".quote"):

        author = quote.find(class_='author').get_text()
        link = url_home + quote.find('a')['href']

        #Builds a set of tuples (author,link-to-bio)
        set_authors.add((author,link))

        #List of dictionaries {quote,author,tags,link}
        #Tags for each quote delimited with "_"
        list_quotes.append({
            'quote':quote.find(class_='text').get_text(),
            'author':author,
            'tags':"_".join([tag.get_text() for tag in quote.select('.tag')]),
            'link':link
            })

    next_btn = altoguiso.find(class_='next')                #Looks for for the 'next button'. If not returns None
    if not next_btn: break
    url = next_btn.find('a')['href'] if next_btn else ''    #Get "Next" button's url

#===========================================
#Loop to scrape through all author bio pages
#===========================================
for item in set_authors:

    print(f"Scraping {item[1]}")
    altoguiso = BeautifulSoup(requests.get(item[1]).text,'html.parser')

    #Get birth date in 'YYYY-MM-DD' string format
    txt_birth = altoguiso.find(class_='author-born-date').get_text()  #String 'MMMM DD, YYYYY'
    txt_birth = txt_birth.split(',')                            #List ['MMMM DD',' YYYY']
    txt_birth[1] = txt_birth[1].strip()                      #List ['MMMM DD','YYYY'] 
    txt_birth.extend(txt_birth[0].split(" "))                   #List ['MMMM DD','YYYY', 'MMMM', 'DD']
    txt_birth[2] = months_dict[txt_birth[2].upper()]            #List ['MMMM DD','YYYY', 'MM', 'DD']
    txt_birth = "-".join(txt_birth[1:])                         #String 'YYYY-MM-DD'

    #Get country
    location = altoguiso.find(class_='author-born-location').get_text()   # Gets raw location text
    location = location[3::]                                        # Removes "in_" from the string
    location = location.split(',')                                  # ['SOME PLACE', 'SOME OTHER', 'MAYBE STATE', '...', '<COUNTRY>']
    location = location[-1].strip()                                 # Removes leading and/or trailing spaces from the country item

    #Adds author dictionary to authors list
    list_authors.append({
        'author':item[0],
        'country':location,
        'bdate':txt_birth,
        'bio':altoguiso.find(class_='author-description').get_text().strip()
        })

del [altoguiso, url, url_home, txt_birth, location]

#========================================
#Initialize Files folder, and other stuff
#========================================
#Get root folder from where Scraper.py is being run and add "\Files" to it
filesfolder = os.path.dirname(
                os.path.abspath(__file__)
                             ) + '\\Files'

#Create "Files" folder if it doesn't exist
if not Path(filesfolder).exists(): Path(filesfolder).mkdir(parents=True, exist_ok=True)

file_quotes = filesfolder + '\\Quotes.csv'
file_authors = filesfolder + "\\Authors.csv"

fields_quotes = ['quote','author','tags', 'link']   #Header names must match dictionary keys
fields_authors =['author','country','bdate','bio']

tasks_thingy = [
    [file_quotes,fields_quotes,list_quotes],
    [file_authors,fields_authors,list_authors]
    ]

del (filesfolder, 
    file_quotes, file_authors, 
    fields_quotes, fields_authors,
    list_quotes, list_authors)

#===================
#Saving to CSV files
#===================
for item in tasks_thingy:
    print(f'Printing to file: {item[0]}\nHeaders are: {item[1]}')
    with open(item[0], 'w',newline ='', encoding='utf-16') as file:
        WriterObj = csv.DictWriter(file, fieldnames=item[1])
        WriterObj.writeheader()
        WriterObj.writerows(item[2])

#Log.csv
#Future logging, onces logging structure is defined
#