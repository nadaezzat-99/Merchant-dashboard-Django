import calendar

from django.utils.timezone import now
from datetime import datetime, timedelta, time, date

from analytics.models import Transactions


class FilterServices:
    @staticmethod
    def filter_on_date(request, queryset):
        print('filter_on_date')
        if request.GET.get('dateFrom') and request.GET.get('dateTo'):
            if request.GET.get('dateFrom') > request.GET.get('dateTo'):
                queryset = Transactions.objects.none()
            else:
                queryset = queryset.filter(date__range=[request.GET.get('dateFrom'), datetime.strptime(request.GET.get('dateTo'), '%Y-%m-%d') + timedelta(days=1)])
        elif request.GET.get('TimeFrameId'):
            time_frame = request.GET.get('TimeFrameId')
            if time_frame == 'today':
                start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = start_date + timedelta(hours=24)
            elif time_frame == 'yesterday':
                today = datetime.now().date()
                yesterday = today + timedelta(-1)
                start_date = datetime.combine(yesterday, time())
                end_date = datetime.combine(today, time())
            elif time_frame == 'current-week':
                today = datetime.today()
                weekday = (today.weekday() - 5) % 7
                start_date = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=weekday)
                end_date = start_date + timedelta(days=7)
            elif time_frame == 'last-week':
                today = datetime.today()
                weekday = (today.weekday() - 5) % 7
                start_date = date.today() - timedelta(days=weekday) - timedelta(days=7)
                end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
                # print("###10", start_date, "##", end_date)
            elif time_frame == 'current-month':
                start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                days = calendar.monthrange(start_date.year, start_date.month)[1]
                end_date = start_date + timedelta(days=days)
            elif time_frame == 'last-month':
                now = datetime.now()
                days = calendar.monthrange(now.year, now.month)[1]
                start_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days)
                end_date = start_date + timedelta(days=days)
            elif time_frame == 'last-quarter':
                lastQuarter = (int((datetime.today().month - 1) // 3) - 1) % 4 + 1
                # print("points:", lastQuarter)
                start_date = datetime(datetime.today().year, (3 * lastQuarter - 2) % 12, 1)
                end_date = datetime(datetime.today().year, (3 * lastQuarter + 1) % 12, 1) + timedelta(microseconds=-1)
                # print(lastQuarter, start_date, end_date, sep=" ## ")
            else:
                start_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
                end_date = datetime.now()
            # print("filter_on_date: ", start_date, "##", end_date)
            queryset = queryset.filter(date__range=[start_date, end_date])
        return queryset

    @staticmethod
    def filter_on_status(request, queryset):
        print('filter_on_status')
        if request.GET.get('f-status'):
            status = request.GET.get('f-status')
            status = status.split(',')
            status = [state.replace('-', ' ') for state in status]
            queryset = queryset.filter(mapping_status__in=status)
        return queryset

    @staticmethod
    def filter_on_type(request, queryset):
        print('filter_on_type')
        if request.GET.get('f-type'):
            types = request.GET.get('f-type')
            types = types.split(',')
            types = [type.replace('-', ' ') for type in types]
            queryset = queryset.filter(mapping_type__in=types)
        return queryset

    @staticmethod
    def filter_on_pos(request, queryset):
        print('filter_on_pos')
        if request.GET.get('POS'):
            queryset = queryset.filter(terminal_id=request.GET.get('POS'))
        return queryset

    @staticmethod
    def filter_on_transaction_id(request, queryset):
        print('filter_on_transaction_id')
        if request.GET.get('transaction_id'):
            queryset = queryset.filter(stan__icontains=request.GET.get('transaction_id'))
        return queryset

    @staticmethod
    def filter_on_amount(request, queryset):
        print('filter_on_amount')
        if request.GET.get('f-Value-from-to'):
            value = request.GET.get('f-Value-from-to')
            first_value = value.split('-')[0]
            second_value = value.split('-')[1]
            queryset = queryset.filter(amount__range=[first_value, second_value])
        return queryset



