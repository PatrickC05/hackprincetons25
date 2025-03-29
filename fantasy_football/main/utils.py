import datetime

def recent_monday():
    today = datetime.date.today()
    days_to_subtract = (today.weekday() - 0) % 7  # 0 represents Monday
    most_recent_monday = today - datetime.timedelta(days=days_to_subtract)
    return most_recent_monday