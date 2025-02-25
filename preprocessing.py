import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    msg = re.split(pattern, data)
    date = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'date': date, 'message': msg[1:]})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M - ', errors='coerce')



    # Extract users and messages
    user_pattern = r'([\w\W]+?):\s'
    users = []
    messages = []

    for m in df['message']:
        entry = re.split(user_pattern, m)
        if len(entry) > 2:
            users.append(entry[1])  # Username
            messages.append(entry[2])  # Message
        else:
            users.append('group_notification')  # System messages
            messages.append(entry[0])  # Message content

    # Clean messages and add to DataFrame
    messages = [m.replace('\n', "") for m in messages]
    df['Users'] = users
    df['message'] = messages

    # Extract date components
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['Date'] = df['date'].dt.date
    df['Day_name'] = df['date'].dt.day_name()
    period = []
    for h in df[['Day_name', 'hour']]['hour']:
        if h == 23:
            period.append(str(h) + '-' + str('00'))
        elif h == 0:
            period.append(str('00') + '-' + str(h + 1))
        else:
            period.append(str(h) + '-' + str(h + 1))

    df['period'] = period

    return df
