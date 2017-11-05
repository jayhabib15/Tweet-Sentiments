#pip install textblob
#python -m textblob.download_corpora
#pip install emoji --upgrade
#pip install xlrd
#pip install xlwt
import emoji
import re
import xlrd
import xlwt
import csv
from textblob import TextBlob

POSITIVE = 'Positive'
NEGATIVE = 'Negative'
NEUTRAL = 'Neutral'
CONFUSED = 'Confused'

emojis = {
    POSITIVE: '😀|😃|😄|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😝|💪|💪🏻|💪🏼|💪🏽|💪🏾|💪🏿|✌|✌🏻|✌🏼|✌🏽|✌🏾|✌🏿|👌|👌🏻|👌🏼|👌🏽|👌🏾|👌🏿|👍|👍🏻|👍🏼|👍🏽|👍🏾|👍🏿|👊|👊🏻|👊🏼|👊🏽|👊🏾|👊🏿|👏|👏🏻|👏🏼|👏🏽|👏🏾|👏🏿|',
    NEGATIVE: '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😰|😱|😜|👎|👎🏻|👎🏼|👎🏽|👎🏾|👎🏿',
    NEUTRAL: '😐|😑|😳|😮|😯|😶|😴|😵|😲|🖕|😅|😂|😆|😁',
    CONFUSED: '😕'
}

def new_sheet(file):
    with open(file, 'r') as fin:
        tweets = (csv.reader(fin))
        data = []
        for x,y,z,w in tweets:
            data.append(full_analysis(y))
    return data

def summary(sheet):
    Positive = 0
    Neutral = 0
    Negative = 0
    for sentiment in new_sheet(sheet):
        if sentiment == "positive":
            Positive = Positive + 1
        if sentiment == "neutral":
            Neutral = Neutral + 1
        if sentiment == "negative":
            Negative = Negative + 1
    print("Number of positive tweets: " + str(Positive))
    print(Neutral)
    print(Negative)

def full_analysis(tweet):
    sent_list = []
    for sent, icons in emojis.items():
        matched = re.findall(icons, tweet)
        if len(matched) > 0:
            sent_list.append(sent)
            return(sent_list)
        else:
            return text_analysis(tweet)
    if POSITIVE in sent_list and NEGATIVE in sent_list:
        sent = CONFUSED
    elif POSITIVE in sent_list:
        sent = POSITIVE
    elif NEGATIVE in sent_list:
        sent = NEGATIVE
    return sent

def text_analysis(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
