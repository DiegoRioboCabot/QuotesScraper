import os
import csv
import requests

from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path 


#Fields for the quotes file (future MySQL 'quotes' table)
text = []
tags = []
author = []



#Fields for the author file (future MySQL 'authors' table)
#author = []
bio = []
country =[]
initials = []
bios_link = []
birth_date = []


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
            DECEMBER = '12'
            )


#Base URL
url_home = "http://quotes.toscrape.com"
url = url_home

#============================================
#Loop to scrape through all pages with quotes
#============================================

while True:
    altoguiso = BeautifulSoup(requests.get(url).text,"html.parser")

    text.extend(
        [item.string for item in 
        altoguiso.select(".text")]
        )

    author.extend(
        [item.string for item in 
        altoguiso.select(".author")]
        )

    bios_link.extend(
        [url_home + item.next_sibling.next_sibling.get("href") 
        for item in altoguiso.select(".author")]
        )

    #Get tags for each quote as tuples, and pass them a list elements
    for quote in altoguiso.select(".quote"):
        for temp in quote.select(".tags"):
            tags.append(
                        tuple(
                            tag.string for tag in temp.find_all("a")
                            )
                        )

    #Verify if there's a "Next" button on page
    if not altoguiso.select(".next"): break

    #Get "Next" button's link and add it to main URL
    url = url_home + altoguiso.select(".next")[0].next_element.next_element.get("href")

quotes_list = list(zip(text,author,tags))


#===========================================
#Loop to scrape through all author bio pages
#===========================================

author_set = set(zip(author,bios_link))
author = []

for item in author_set:
    url = item[1]
    altoguiso = BeautifulSoup(requests.get(url).text,"html.parser")

    birth_text = altoguiso.select(".author-born-date")[0].string.split(',') #'MMMM DD, YYYY'

    year = birth_text[-1].strip()
    day = birth_text[0].split(" ")[-1]
    month = birth_text[0].split(" ")[0]
    month = months_dict[month.upper()]

    birth_text = "-".join([year,month,day]) #'YYYY-MM-DD'

    #SOME PLACE, SOME OTHER, MAYBE STATE, ETC, <COUNTRY>
    location = altoguiso.select(".author-born-location")[0].string[3::] 

    #Selects last item from list and removes its leading spaces
    country_str = location.split(',')[-1].strip() 

    #Continues to add to temporary lists
    author.append(item[0])
    country.append(country_str)
    birth_date.append(birth_text)
    bio.append(altoguiso.select(".author-description")[0].string)


#Build quotes list, author list and delete temporary data
author_list = list(zip(author,country,birth_date,bio))


del [text, tags, bios_link, author, country, birth_date,bio]

#===================
#Saving to CSV files
#===================

#Get root folder from where Scraper.py is being run and add "\Files" to it
filesfolder = os.path.dirname(
                os.path.abspath(__file__)
                             ) + "\\Files"

#Create "Files" folder if it doesn't exist
if not Path(filesfolder).exists(): Path(filesfolder).mkdir(parents=True, exist_ok=True)


#Quotes.csv
with open(filesfolder + "\\Quotes.csv", "w", newline='',encoding='utf-16') as file:
    csv.writer(file).writerow(["quote","author","tags"])
    csv.writer(file).writerows(quotes_list)

#Authors.csv
with open(filesfolder + "\\Authors.csv", "w", newline='',encoding='utf-16') as file:
    csv.writer(file).writerow(["author","country","birth_date", "bio"])
    csv.writer(file).writerows(author_list)


#Log.csv
#Future logging, onces logging structure is defined