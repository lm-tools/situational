import datetime

from . import forms


def format_circumstance(circumstance):
    circumstance_dict = dict(forms.HistoryDetailsForm.CIRCUMSTANCE_CHOICES)
    return circumstance_dict.get(circumstance, circumstance)


def same_date(month_1, year_1, month_2, year_2):
    return (month_1 == month_2) and (year_1 == year_2)


def intervals_for_item(history_item, timeline_beginning, timeline_end):
    number_active_months = number_of_months_in_item(history_item)
    total_months = number_of_months(
        timeline_beginning["month"],
        timeline_beginning["year"],
        timeline_end["month"],
        timeline_end["year"]
    )
    if same_date(
        timeline_beginning["month"],
        timeline_beginning["year"],
        history_item["from_month"],
        history_item["from_year"]
    ):
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval = {
            "active": False,
            "width": 100 - active_interval["width"]
        }
        return [active_interval, inactive_interval]
    elif same_date(
        timeline_end["month"],
        timeline_end["year"],
        history_item["to_month"],
        history_item["to_year"]
    ):
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval = {
            "active": False,
            "width": 100 - active_interval["width"]
        }
        return [inactive_interval, active_interval]
    else:
        inactive_initial_months = number_of_months(
            timeline_beginning["month"],
            timeline_beginning["year"],
            history_item["from_month"],
            history_item["from_year"]
        )
        inactive_interval_1 = {
            "active": False,
            "width": inactive_initial_months / total_months * 100
        }
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval_2 = {
            "active": False,
            "width": 100 - active_interval["width"] - inactive_interval_1["width"]
        }
        return [inactive_interval_1, active_interval, inactive_interval_2]


def year_timeline(timeline_beginning, timeline_end):
    years = []
    total_months = number_of_months(
        timeline_beginning["month"],
        timeline_beginning["year"],
        timeline_end["month"],
        timeline_end["year"],
    )
    years += [{
        "width": (12 - timeline_beginning["month"]) / total_months * 100,
        "label": timeline_beginning["year"]
    }]
    for year in range(timeline_beginning["year"] + 1, timeline_end["year"]):
        years += [{
            "width": 12 / total_months * 100,
            "label": year
        }]
    years += [{
        "width": timeline_end["month"] / total_months * 100,
        "label": timeline_end["year"]
    }]
    return years


def number_of_months_in_item(history_item):
    return number_of_months(
        history_item["from_month"],
        history_item["from_year"],
        history_item["to_month"],
        history_item["to_year"],
    )


def number_of_months(start_month, start_year, end_month, end_year):
    if start_month == end_month and start_year == end_year:
        return 1
    else:
        return (end_year - start_year) * 12 + (end_month - start_month)


def formatted_now():
    today = datetime.datetime.now()
    now = {
        "month": today.month,
        "year": today.year,
    }
    return now
