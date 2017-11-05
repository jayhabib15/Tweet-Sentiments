#pip install textblob
#python -m textblob.download_corpora
#pip install emoji --upgrade
#pip install xlrd I don't think you need this anymore
#pip install xlwt I don't think you need this anymore
#pip install pandas
#pip install openpyxl
#remember to edit csv so that tweets are under "Tweet_Message" not "Tweet Message"
import emoji
import re
import xlrd
import xlwt
import csv
import pandas as pd
from textblob import TextBlob
import openpyxl

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

def list_of_sents(file):
    with open(file, 'r') as fin:
        tweets = (csv.reader(fin))
        data = []
        for x,y,z,w in tweets:
            data.append(full_analysis(y))
    return data

def analyze_csv(sheet):
    Results = []
    Column = []
    Data = pd.read_csv(sheet)
    Tweets = Data.Tweet_Message
    for tweet in Tweets:
        Results.append((tweet, full_analysis(tweet)))
    for x,y in Results:
        Column.append(y)
    df2 = pd.DataFrame(Column)
    with open(sheet, 'a') as f:
        df2.to_csv(f, header=False)
    # writer = pd.ExcelWriter('output.xlsx')
    # Data.to_excel(writer,'Sheet1')
    # df2.to_excel(writer,'Sheet2')
    # writer.save()
    # Data.append(df2)
    # Data.to_excel('test.xlsx')
    # with open(sheet, "w") as output:
    #      writer = csv.writer(output, lineterminator='\n')
    #      for val in Sample:
    #          writer.writerow([val])
    # csv_input = pd.read_csv(sheet)
    # csv_input['Sentiment'] = csv_input[Sample]
    # csv_input.to_csv('output.csv', index=False)

def summary(sheet):
    Positive = 0
    Neutral = 0
    Negative = 0
    for sentiment in list_of_sents(sheet):
        if sentiment == "positive":
            Positive = Positive + 1
        if sentiment == "neutral":
            Neutral = Neutral + 1
        if sentiment == "negative":
            Negative = Negative + 1
    print("Number of positive tweets: " + str(Positive))
    print("Number of neutral tweets: " + str(Neutral))
    print("Number of negative tweets: " + str(Negative))

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
