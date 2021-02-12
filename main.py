from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
import re
import nltk
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup

# Treba da se popravi ovaj word_is_important tako da uzima i EUR/USD i slicno
def word_is_important(word):
    IMPORTANT_WORDS = {
        "UK",
        "US",
        "dollar",
        "pound",
        "Pound",
        "GBP",
        "NZD",
        "Dollar",
        "New",
        "Zeland",
        "Japan",
        "Japanese",
        "JPY",
        "Euro",
        "EUR",
        "EU",
        "Europian",
        "Australia",
        "Australian",
        "AU",
        "AUD",
        "Switzerland",
        "Swiss",
        "CHF",
        "frank",
        "Canada",
        "Canadian",
        "CAD"
    }
    if word in IMPORTANT_WORDS:
        return 1
    return 0
def switch_currency(curr_argument):
    switcher = {
        1: "NZD",
        2: "GBP",
        3: "EUR",
        4: "AUD",
        5: "CHF",
        6: "CAD",
        7: "JPY",
        8: "USD"
    }
    return switcher.get(curr_argument)

def regex_search(pattern,word_stack):
    for word in word_stack:
        if(re.search(pattern,word)):
            return 1
        return 0

url = "https://www.investing.com/news/forex-news"
req = Request(url = url,headers={'user-agent':'my_app'})
response = urlopen(req)
html = BeautifulSoup(response,features='html.parser')
#print(html)
news_table = html.findAll("div", {"class": "textDiv"})
cnt = 0
for news in news_table:
    if cnt<7:
        cnt+=1
        continue
    sentence = news.find("a",{"class":"title"})['title']
    print(sentence)
    vader = SentimentIntensityAnalyzer()
    polarity = vader.polarity_scores(sentence)['compound']
    words = word_tokenize(sentence)
    # print(words)
    counter = 0
    for word in words:
        word_polarity = vader.polarity_scores(word)['compound']
        # print(word + " " + str(word_polarity))
        if polarity==0:
            break
        elif polarity<0:
            if(counter==0 and word_polarity<0):
                most_polar_word = word
                most_polar_word_polarity = word_polarity
                counter = 1
            elif(counter!=0 and word_polarity<most_polar_word_polarity):
                # Ovde treba razmotriti slucaj kada je word_polarity=important_word_polarity
                most_polar_word = word
                most_polar_word_polarity = word_polarity
        elif polarity>0:
            if(counter==0 and word_polarity>0):
                most_polar_word = word
                most_polar_word_polarity = word_polarity
                counter = 1
            elif(counter!=0 and word_polarity>most_polar_word_polarity):
                # Ovde treba razmotriti slucaj kada je word_polarity=important_word_polarity
                most_polar_word = word
                most_polar_word_polarity = word_polarity

    words_before = []
    for word in words:
        try:
            if(word==most_polar_word):
                break
            words_before.append(word)
        except:
            print("All of the words are natural")
            break
    # print(words_before)
    counter = 0
    word_stack = []
    for i in range(0,len(words_before)):
        word = words_before.pop()
        if word_is_important(word)==0 and counter==1:
            break
        if word_is_important(word)==1:
            word_stack.append(word)
            counter=1

    # currency_identifier value table
    # 1 - NZD
    # 2 - GBP
    # 3 - EUR
    # 4 - AUD
    # 5 - CHF
    # 6 - CAD
    # 7 - JPY
    # 8 - USD
    if(len(word_stack)==0):
        print("News are not affecting any of the 8 major pairs")
        print(" ")
        continue
    if ("New" in word_stack and "Zeland" in word_stack) or ("NZD" in word_stack) or (regex_search(r"NZD/",word_stack)):
        currency_identifier = 1
    elif regex_search(r"/NZD",word_stack):
        currency_identifier = 1
        polarity = -polarity
    elif("Pound" in word_stack) or ("pound" in word_stack) or ("GBP" in word_stack) or (regex_search(r"GBP/",word_stack)):
        currency_identifier = 2
    elif regex_search(r"/GBP",word_stack):
        currency_identifier = 2
        polarity = -polarity
    elif("Euro" in word_stack) or ("EU" in word_stack) or ("EUR" in word_stack) or ("Europian" in word_stack) or (regex_search(r"EUR/",word_stack)):
        currency_identifier = 3
    elif regex_search(r"/EUR",word_stack):
        currency_identifier = 3
        polarity = -polarity
    elif("Australia" in word_stack) or ("Australian" in word_stack) or ("AUD" in word_stack) or (regex_search(r"AUD/",word_stack)):
        currency_identifier = 4
    elif regex_search(r"/AUD",word_stack):
        currency_identifier = 4
        polarity = -polarity
    elif("Switzerland" in word_stack) or ("CHF" in word_stack) or ("Swiss" in word_stack) or ("frank" in word_stack) or (regex_search(r"CHF/",word_stack)):
        currency_identifier = 5
    elif regex_search(r"/CHF",word_stack):
        currency_identifier = 5
        polarity = -polarity
    elif("Canada" in word_stack) or ("Canadian" in word_stack) or ("CAD" in word_stack) or (regex_search(r"CAD/",word_stack)):
        currency_identifier = 6
    elif regex_search(r"/CAD",word_stack):
        currency_identifier = 6
        polarity = -polarity
    elif("Japan" in word_stack) or ("Japanese" in word_stack) or ("JPY" in word_stack) or (regex_search(r"JPY/",word_stack)):
        currency_identifier = 7
    elif regex_search(r"/JPY",word_stack):
        currency_identifier = 7
        polarity = -polarity
    elif("dollar" in word_stack) or ("Dollar" in word_stack) or ("US" in word_stack) or (regex_search(r"USD/",word_stack)):
        currency_identifier = 8
    elif regex_search(r"/USD",word_stack):
        currency_identifier = 8
        polarity = -polarity

    if polarity>0:
        text = "Positive"
    elif polarity<0:
        text = "Negative"
    else:
        text = "Neutral news"

    if polarity==0:
        print(text)
    else:
        print("Affected currency: " + str(switch_currency(currency_identifier)))
        print("Effect: " + text)
    print(" ")


