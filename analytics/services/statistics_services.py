import calendar
import datetime
from datetime import date, timedelta

from django.db.models import Sum
from django.utils.timezone import now

from analytics.services.utils import HelperFunction


class StatisticsServices:

    @staticmethod
    def get_statistics(queryset):
        # print("get_statistics", queryset)
        # daily transaction
        start_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_transactions = queryset.filter(date__range=[start_date, start_date + timedelta(hours=24)])
        # print("daily_transactions", daily_transactions.values_list('id', flat=True))
        # print("daily: ", start_date, " ## ", start_date + timedelta(hours=24))
        # print("#####1", daily_transactions.filter(response_code='00'))
        plus = daily_transactions.filter(response_code='00', type='sale').aggregate(Sum('amount'))['amount__sum'] or 0
        minus = daily_transactions.filter(response_code='00', is_void=True).aggregate(Sum('amount'))['amount__sum'] or 0
        # print(daily_transactions.filter(response_code='00', type='sale'), daily_transactions.filter(response_code='00', is_void=True))
        daily_transactions = plus - minus

        # weekly transactions
        today = datetime.datetime.today()
        weekday = (today.weekday() - 5) % 7
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=weekday)
        # print("PEEEEP1", start_date)
        weekly_transactions = queryset.filter(date__range=[start_date, datetime.datetime.now()])
        plus = weekly_transactions.filter(response_code='00', type__in=['sale', 'installment']).aggregate(Sum('amount'))['amount__sum'] or 0
        minus = weekly_transactions.filter(response_code='00', is_void=True).aggregate(Sum('amount'))['amount__sum'] or 0
        weekly_transactions = plus - minus
        # print("weekly: ", start_date, " ## ", datetime.datetime.now())

        # monthly transactions
        start_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        days = calendar.monthrange(start_date.year, start_date.month)[1]
        end_date = start_date + timedelta(days=days)
        monthly_transactions = queryset.filter(date__range=[start_date, end_date])
        plus = monthly_transactions.filter(response_code='00', type__in=['sale', 'installment']).aggregate(Sum('amount'))['amount__sum'] or 0
        minus = monthly_transactions.filter(response_code='00', is_void=True).aggregate(Sum('amount'))['amount__sum'] or 0
        # print( plus , " ## ",minus)
        monthly_transactions = plus - minus
        # print("monthly: ", start_date, " ## ", end_date)

        # last-month transactions
        now = datetime.datetime.now()
        days = calendar.monthrange(now.year, now.month)[1]
        start_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
        end_date = start_date + timedelta(days=days)
        last_month = queryset.filter(date__range=[start_date, end_date])
        plus = last_month.filter(response_code='00', type__in=['sale', 'installment']).aggregate(Sum('amount'))['amount__sum'] or 0
        minus = last_month.filter(response_code='00', is_void=True).aggregate(Sum('amount'))['amount__sum'] or 0
        last_month = plus - minus
        # print("monthly: ", start_date, " ## ", end_date)


        # last-quarter transactions
        current_date = datetime.datetime.now()
        lastQuarter = HelperFunction.get_last_quarter_start()
        # print("lastQuarter", HelperFunction.get_last_quarter_start())
        dtFirstDay = datetime.datetime(current_date.year, lastQuarter, 1)
        dtLastDay = datetime.datetime(current_date.year, (lastQuarter + 3)%12, 1)
        # print("lastQuarter: ", dtFirstDay, " ## ", dtLastDay)
        # print("lasstQuarter", queryset)
        quarter_transactions = queryset.filter(date__range=[dtFirstDay, dtLastDay])
        # print("lasstQuarter", quarter_transactions)
        plus = quarter_transactions.filter(response_code='00', type__in=['sale', 'installment']).aggregate(Sum('amount'))['amount__sum'] or 0
        minus = quarter_transactions.filter(response_code='00', is_void=True).aggregate(Sum('amount'))['amount__sum'] or 0
        quarter_transactions = plus - minus
        # print("last-quarter: ", dtFirstDay, " ## ", dtLastDay)


        statistics = {
            "today": daily_transactions,
            "current-week": weekly_transactions,
            "current-month": monthly_transactions,
            "last-month": last_month,
            "last-quarter": quarter_transactions,
        }
        return statistics
