import datetime


def last_known_start_date(session):
    if 'quick_history' not in session or len(session['quick_history']) == 0:
        return formatted_now()
    else:
        oldest_known_item = session['quick_history'][0]
        return {
            "month": oldest_known_item["from_month"],
            "year": oldest_known_item["from_year"]
        }


def formatted_now():
    today = datetime.datetime.now()
    now = {
        "month": today.month,
        "year": today.year,
    }
    return now
