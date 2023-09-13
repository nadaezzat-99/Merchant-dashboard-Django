from django.db.models.functions import datetime


class HelperFunction:

    @staticmethod
    def get_last_quarter_start():
        now = datetime.datetime.now()
        quarter = (now.month - 1) // 3 + 1
        if quarter == 1:
            # Last quarter of the previous year
            year = now.year - 1
            month = 10
        else:
            year = now.year
            month = (quarter - 2) * 3 + 1
        return datetime.datetime(year, month, 1).month