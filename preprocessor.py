import pandas as pd
import numpy as np
import datetime
#import matplotlib.pyplot as plt
import re
def process_data(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-z]{1,2}\s-\s'
    #f = open('gali-L-block.txt','r', encoding='UTF-8')
    #data = f.read()
    message = re.split(pattern, data)[1:]
    date = re.findall(pattern, data)
    date  = [s.replace('\u202f',' ') for s in date]
    date  = [s.replace(' - ','') for s in date]
    df = pd.DataFrame({'user_text':message,'text_date':date})
    df['date'] = pd.to_datetime(df['text_date'],format='%d/%m/%Y, %I:%M %p')
    df = df.drop(columns=['text_date'])
    #get user and message as new columns
    users = []
    messages = []
    for message in df['user_text']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('grouop_notification')
            messages.append(entry[0])

    df['username'] = users
    df['message'] = messages

    #create additionalcolumns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day'] = df['date'].dt.day_name()
    df['hours'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['date_new'] = df['date'].dt.date
    df = df.drop(columns=['user_text'])
    #create period datafram to bucketize time
    period = []
    for hours in df[['day','hours']]['hours']:
        if hours==23:
            period.append(str(hours)+'-'+str('00'))
        elif hours==0:
            period.append(str('00')+'-'+str(hours+1))
        else:
            period.append(str(hours)+'-'+str(hours+1))
                
    df['period'] =   period 
    
    return df[1:]


