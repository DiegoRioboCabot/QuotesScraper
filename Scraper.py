import os
import csv
import requests

from bs4 import BeautifulSoup
from time import sleep
from pathlib import Path 


url_home = "http://quotes.toscrape.com"
url = url_home

text = []
author = []
bios_link = []
tags = []
quotes_list = ["quote","author","tags"]
author_list = ["author", "url", "birth_date", "bio"]

#####################################################

#Loop to scrape through all pages with quotes

#####################################################
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
                        "-".join(
                            [tag.string for tag in temp.find_all("a")]
                            )
                        )

    #Verify if there's a "Next" button on page
    if not altoguiso.select(".next"): break

    #Get "Next" button's link and add it to main URL
    url = url_home + altoguiso.select(".next")[0].next_element.next_element.get("href")

#####################################################

#Loop to scrape through all author bio pages

#####################################################




#####################################################

#Saving to CSV files

#####################################################

filesfolder = os.path.dirname(os.path.abspath(__file__)) + "\\Files"

#Create "Files" folder if it doesn't exist
if not Path(filesfolder).exists(): Path(filesfolder).mkdir(parents=True, exist_ok=True)

#author_list = author_header + zip(author, bios_link)

with open(filesfolder + "\\Quotes.csv", "w", newline='') as file:
    csv.writer(file).writerow(["quote","author","tags"])
    csv.writer(file).writerows(list(zip(text,author,tags)))

#El programa está arrojando error al intentar procesar la última cita de la página 8, de Mark Twain. Ya que empieza con 'Clasic' entre signos de comillas simples