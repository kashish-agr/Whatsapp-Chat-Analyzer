import re
import pandas as pd

def preprocess (data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    msg = re.split(pattern, data)
    date = re.findall(pattern, data)
    date = pd.to_datetime(date , format = '%m%d%y, %H:%M - ')

    data = pd.DataFrame({'Message' : msg , 'date': date})
    data['day'] = data['date'].dt.day
    data['month'] = data['date'].dt.month_name()
    data['year'] = data['date'].dt.year
    data['hour'] = data['date'].dt.hour
    data['minute'] = data['date'].dt.minute
    pattern = '([\w\W]+?):\s'
    users = []
    message = []
    for msg in data['message']:
        entry = re.split(pattern, msg)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
    else:
        users.append('group_notification')
        message.append(entry[0])
    msg = [m.replace('\n', "") for m in message]
    data['Users'] = users
    data['message'] = msg

    return data