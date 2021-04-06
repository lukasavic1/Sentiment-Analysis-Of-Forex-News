# Financial News Sentiment Analysis Using NLTK

This repository contains a script implementing nltk in order to predict future price movements on a foreign currency exchange using news from Investing.com website.

## Table of Contents
- **Scraping the website**
- **Finding the most polar word**
- **Identifying which currency is impacted and how**

### Scraping the website
This is the easiest part, but will be different for every website you choose to do sentiment analysis on. Simply open the url, parse the html and find a news table.
```
from urllib.request import urlopen,Request
from bs4 import BeautifulSoup

url = "https://www.investing.com/news/forex-news"
req = Request(url = url,headers={'user-agent':'my_app'})
response = urlopen(req)
html = BeautifulSoup(response,features='html.parser')
#print(html)
news_table = html.findAll("div", {"class": "textDiv"})
```
Later we will find exact sentences using
```
sentence = news.find("a",{"class":"title"})['title']
```
since sentences are written as links to their own pages.
Using nltk's SentimentIntensityAnalyzer we can find the polarity of the whole sentence.
```
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize

polarity = vader.polarity_scores(sentence)['compound']
```
Using this polarity, we will try to find the strongest word in the sentence, that points to the same direction as the overall polarity!

```
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
```
This part of the code does it. ```most_polar_word``` is the result.
Then we take all the words before the ```most_polar_word``` and save them to one list if they are important. Important words are the ones contaning import names like Pound,Dollar,U.S. etc.
This part should be improved so it can better identify the words, since Canada,Canadian and Canada's all point to the same currency. This is something I will work on to improving, and making the script even better.
If there are no important words before the most polar one, then news are not affecting any currencies.
At the end, with a lot of if statements(for all major pairs), I'm checking to see is the polarity direction normal or inverse and for which currency.
```
    if ("New" in word_stack and "Zeland" in word_stack) or ("NZD" in word_stack) or (regex_search(r"NZD/",word_stack)):
        currency_identifier = 1
    elif regex_search(r"/NZD",word_stack):
        currency_identifier = 1
        polarity = -polarity
    elif("Pound" in word_stack) or ("pound" in word_stack) or ("GBP" in word_stack) or (regex_search(r"GBP/",word_stack)):
        currency_identifier = 2
```
Here a simple regex function is used.

And that's it. The results were very good. For the 7 most recent news releases that the script identified some clear meaning, it made a mistake on 1 of those and 6 were correct, which is great in my opinion, for such simple script like this, that can be improved so much more.

### Connect with me
This wraps up my explanation of this project, I hope that I was clear and if you want to connect with me:
- Send me an email (lukasavic18@gmail.com) 📚
- Follow me on [LinkedIn](https://www.linkedin.com/in/luka-savic-a73504206/) 💡
