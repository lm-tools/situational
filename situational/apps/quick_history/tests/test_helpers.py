from situational.testing import BaseCase
from quick_history import helpers


class TestHelpers(BaseCase):

    timeline_beginning = {
        "month": 9,
        "year": 2013
    }
    timeline_end = {
        "month": 9,
        "year": 2015
    }
    history_item_at_start = {
        "from_month": timeline_beginning["month"],
        "from_year": timeline_beginning["year"],
        "to_month": timeline_beginning["month"] + 6,
        "to_year": timeline_beginning["year"]
    }
    history_item_at_end = {
        "from_month": timeline_end["month"] - 6,
        "from_year": timeline_end["year"],
        "to_month": timeline_end["month"],
        "to_year": timeline_end["year"]
    }
    history_item_within_timeline = {
        "from_month": timeline_beginning["month"] + 6,
        "from_year": timeline_beginning["year"],
        "to_month": timeline_end["month"] - 6,
        "to_year": timeline_end["year"]
    }

    def test_intervals_for_item_at_start(self):
        intervals = helpers.intervals_for_item(
            self.history_item_at_start,
            self.timeline_beginning,
            self.timeline_end
        )
        self.assertEquals(intervals, [
            {
                "active": True,
                "width": 25,
            },
            {
                "active": False,
                "width": 75,
            }
        ])

    def test_intervals_for_item_at_end(self):
        intervals = helpers.intervals_for_item(
            self.history_item_at_end,
            self.timeline_beginning,
            self.timeline_end
        )
        self.assertEquals(intervals, [
            {
                "active": False,
                "width": 75,
            },
            {
                "active": True,
                "width": 25,
            }
        ])

    def test_intervals_for_item_within_timeline(self):
        intervals = helpers.intervals_for_item(
            self.history_item_within_timeline,
            self.timeline_beginning,
            self.timeline_end
        )
        self.assertEquals(intervals, [
            {
                "active": False,
                "width": 25,
            },
            {
                "active": True,
                "width": 50,
            },
            {
                "active": False,
                "width": 25,
            }
        ])

    def test_year_timeline(self):
        years = helpers.year_timeline(
            self.timeline_beginning,
            self.timeline_end
        )
        self.assertEquals(years, [
            {
                "label": 2013,
                "width": 12.5,
            },
            {
                "label": 2014,
                "width": 50,
            },
            {
                "label": 2015,
                "width": 37.5
            }
        ])

    def test_number_of_months_same_months(self):
        months = helpers.number_of_months(11, 2014, 11, 2014)
        self.assertEquals(months, 1)

    def test_number_of_months_different_months(self):
        months = helpers.number_of_months(11, 2012, 3, 2015)
        self.assertEquals(months, 28)
