from DB_ReaderOnly import DB_Reader
import os


clear = lambda: os.system('cls') #Clears Screen for Windows Systems


class Hinter:

    def __init__(self):
        pass

    def get(self,lives, quote):

        if lives == 3:    print(f"\nWrong! Let me give you a hint:\nAuthor was born in {quote['a_country']}")
        elif lives == 2:    print(f"\nWrong! Let me give you another hint:\nAuthor was born on {quote['a_bdate']}")
        elif lives == 1:    print(f"\nWrong! Let me give the last hint:\nAuthor's initials are {quote['a_initials']}")

        return None

def get_answer(options):
    txt = "[ " + " / ".join(options) +" ]"
    error_msg= f"You must type a valid answer {txt}.\nPlease try again:"
    output = dict(Y = True, N = False)

    while True:
        answer = input()
        try:
            answer.upper()
        except:
            print(error_msg)
            continue
        
        if answer.upper() in options: 
            return output[answer.upper()]

        print(error_msg)

def check_answer(lives,author, answer):
    try:
        answer.upper()
    except:
        return False
    
    if answer.upper() == author.upper():
        return (lives,True)

    lives -= 1
    return (lives,False)


#=========================
#   I N I T I A L I Z E 
#=========================
print("Welcome to Quote Guessing!\nWould you like to update the DB? [ Y / N ]:")

if get_answer(['Y','N']):
    import Scraper
    import DB_Handler

Hints = Hinter()


#=============================
#   Game Engine Starts Here
#=============================
# DB_Reader().catch() 
# Returns dict with keys: [quote,tags,author,a_initials,a_country,a_bdate,a_bio]

while True:
    clear()
    lives = 4
    quote = DB_Reader().catch()
    print(quote['quote']+"\n\n\n")
    print("Who do you think said this?")

    while lives>0:

        Hints.get(lives,quote)
        lives, result = check_answer(lives,quote['author'],input())
        if result:
            print("Yay!! You won! :D")
            break
        elif lives == 0: print(f"\nOh no! You lost :'(\nIt was {quote['author']}")


    print(f"\nDo you want to play again? [ Y / N ]")

    if not get_answer(['Y','N']): break

print("\nBye Bye!")