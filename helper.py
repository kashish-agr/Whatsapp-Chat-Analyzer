from urlextract import URLExtract
import emoji
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

def fetch_stats( user , data):
    if user != 'Overall':
        data = data[data['Users'] == user]

    # 1.  Fetch number of messages
    num_message = data.shape[0]

    # 2. Fetch number of words
    word=[]
    for m in data['message']:
        if m != '<Media omitted>':
            word.extend(m.split())
    num_words = len(word)

    # Media Shared
    media_shared = len(data[data['message'] == '<Media omitted>'])

    # Link shared
    extracter = URLExtract()
    links = []
    for m in data['message']:
        links.extend(extracter.find_urls(m))

    links_shared = len(links)

    # number of emojis
    emojis_shared = 0
    for m in data['message']:
        emojis_shared += emoji.emoji_count(m)

    return num_message , num_words , media_shared , links_shared , emojis_shared


def fetch_most_busy_user( data):
    count =  data['Users'].value_counts().head()
    df = round(data['Users'].value_counts()/data.shape[0]*100,2).reset_index().rename(columns= {'index':'Name' , 'user':'Percent'})
    return count , df

def create_wordcloud(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]
    temp = data[data['Users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    # Read stopwords and convert to a list
    with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().split()  # Splitting creates a list of stopwords
    wc = WordCloud(width=500, height=200, background_color='white', min_font_size=4)
    wimage = wc.generate(temp['message'].str.cat(sep=" "))
    return wimage


def top20(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]
    temp = data[data['Users'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    # Read stopwords and convert to a list
    with open(r'E:\Ml_Learning\Whatsapp-chat-Analyzer\Chat Anayser\stop_hinglish.txt', 'r', encoding='utf-8') as f:
        stop_words = f.read().split()  # Splitting creates a list of stopwords

    words = []
    for m in temp['message']:
        for word in m.lower().split():
            if word not in stop_words:
                words.append(word)

    # Get top 20 words and create a DataFrame with proper column names
    top20_words = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return top20_words
def Emo_Analysis(data , selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]
    emojis = []
    for m in data['message']:
        emojis.extend([c for c in m if c in emoji.EMOJI_DATA])
    Emoji_List = pd.DataFrame(Counter(emojis).most_common(20), columns=['Emojis', 'count'])
    return Emoji_List


def monthly_analysis(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]


    timeline = data.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_analysis(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]


    daily_timeline = data.groupby(data['Date']).count()['message'].reset_index()

    return daily_timeline


def busy_day(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]


    day_timeline = data.groupby(data['Day_name']).count()['message'].reset_index()
    return day_timeline

def busy_month(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]

    month_count = data.groupby(data['month']).count()['message'].reset_index()
    return month_count
def daily_activity_map(data, selected_user):
    if selected_user != 'Overall':
        data = data[data['Users'] == selected_user]


    pt = data.pivot_table(index='Day_name',columns='period',values='message',aggfunc='count')
    return pt





