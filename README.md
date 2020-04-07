# QuotesScraper
Saves quotes and author details to a MySQL local DB + a small Python Game



## 2020.04.07 - Erste Notizen und Ideen

The application should be based on several files, in order to compartimentalize, thus making it easier to learn and practise:

### Scraper.py      
    --> Logs into quotes.toscrape.com and downloads the content into csv files
        1) Quotes details --> Files\Quotes.csv
        2) Author details --> Files\Authors.csv
        3) Activity       --> Files\Log.csv

    
### DB_Handler.py   
    --> All the code related to updating and deleting the data inside the DB is going to be here
        * If schema doesn't exist, it should be created
        * If tables don't exist, they should be created
        * Maybe create a "Log" Table? to practise datetime values

        * If tables are empty, directly try to import all available information
        * If tables aren't empty, default action is to insert only new quotes and author details
        * Before trying to do anything, check if files exist. 
            * If no file exists, log event and do nothing.
            * If some file exists, log status and continue with existing file.
            
        * Update/Load whatever information is available after user interaction.
        * Move and rename parsed files to Files\Processed\yyyymmdd_hhmm_name.csv
        * Update Log.csv

        * Give the user the ability to delete all, in order to start over

### DB_ReadOnly.py
    --> This file will only be used to create a Class, which will be importad by GessingGame.py
        * Connect to the database
        * Randomly select a quote
        * Maybe optional filters could be applied to narrow possibilities down (Say... quotes from People from the UK... idk)
        * Find the author related to the chosen quote, and get it's info.
        * Return a quote object and an author object, each one with all available attributes from the website. + an attribute saying if its the quote-author or not (True/Flase)
        
        * If multiple choice is enabled, then 3 adittional author objects should be returned (all different from each other, of course)


### GuessingGame.py
    --> Interacts with the user to make a guessing game

        * Check if DB hasn't been updated for more than X days. If it is, ask for update check
        * Ask for game mode: Wise Mode or Multiple Choice
            * Wise Mode: Player has to fully guess author               (But has 4 chances)
                ° IF they miss, game engine hives one hint
                ° .... two hints
                ° .... thress hints
                ° that's it, you suck.
            * Multiple Choice: Player has to choose between 4 options   (But has only 1 chance)
        * Play again? Y / N
        
