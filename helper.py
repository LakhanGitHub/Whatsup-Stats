from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def featch_states(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
        
    num_mess = df.shape[0]
    words = []
    for txt in df['message'].fillna(''):
        words.extend(txt.split())
    
    num_media = df[df['message']=='<Media omitted>\n'].shape[0]
    links = []
    for message in df['message'].fillna(''):
        links.extend(extract.find_urls(message))

    return num_mess,len(words),num_media, len(links)
    
def most_busy_user(df):
    df = df[df['username']!='grouop_notification']
    x = df['username'].value_counts().head(10)
    df = round((df['username'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'username': 'Person','count': 'Percentage%'})
    return x,df

def create_word_cloud(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    df = df[df['username']!='grouop_notification']
    df['message'] = df['message'].replace('<Media omitted>','')
    def remove_stop_word(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=200, min_font_size=8, background_color='white')
    df['message'] = df['message'].apply(remove_stop_word)
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc

def most_common_word(selected_user,df):
    f = open('stop_hinglish.txt','r')
    stop_word = f.read()
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    df = df[df['username']!='grouop_notification']
    df['message'] = df['message'].replace('<Media omitted>','')
    words = []
    for message in df['message'].fillna(''):
        for word in message.lower().split():
            if word not in stop_word:
                words.append(word.title())
    temp_df = pd.DataFrame(Counter(words).most_common(20))
    if not temp_df.empty:
        temp_df = temp_df[~temp_df[0].str.contains(r"[&}{.,#_✅🔹•·?*]", regex=True, na=False)]
    
    return temp_df

#emojis
def get_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    
    emojis = []
    for message in df['message'].dropna():
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    df_emoji = pd.DataFrame(Counter(emojis).most_common())
    if not df_emoji.empty:
        df_emoji = df_emoji[~df_emoji[0].isin(['✅', '🔹', '✔'])]

    df_emoji = df_emoji.reset_index(drop=True)
    return df_emoji

#Monthly trend analysis
def monthly_timeline(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    timeline = df.groupby(['year','month'])['message'].count().reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))

    timeline['time'] = time
    return timeline
#Daily Trend
def daily_timeline(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    timeline_daily = df.groupby('date_new')['message'].count().reset_index()
    return timeline_daily
#day trend
def dayname_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    dailytime_days = df.groupby('day')['message'].count().reset_index().sort_values(by='message',ascending=False)
    mapping = {'Friday':5, 'Wednesday':3, 'Thursday':4, 'Monday':1, 'Tuesday':2, 'Sunday':7, 'Saturday':6}
    dailytime_days['order'] = dailytime_days['day'].map(mapping)
    dailytime_days=dailytime_days.sort_values(by='order')
    return dailytime_days
#user activity heatmap
def user_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['username'] == selected_user]
    user_heatap = df.pivot_table(index='day',columns='period', values='message',aggfunc='count').fillna(0)
    return user_heatap