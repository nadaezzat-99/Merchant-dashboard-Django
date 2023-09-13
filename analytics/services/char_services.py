import datetime
from datetime import timedelta
import calendar
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.timezone import now

from analytics.models import Transactions, Terminal

MONTH = 8


class ChartServices:
    @staticmethod
    def get_points_util(queryset, interval, start_date, end_date=datetime.datetime.now(), operation="count"):
        # print("#################20")
        # print("start_date", start_date)
        # print("end_date", end_date)
        # print(interval)
        points = []
        # print(queryset)
        # print("##@@##1", start_date, "##", end_date)
        curr = start_date
        # print('######2', end_date, "###", interval)
        # for trx in queryset:
            # print("#####3", trx['transactionDate'], trx['transactionDate'])
        while curr < end_date:
            # print("@@@@2", queryset.values_list('date', flat=True))
            start_time = curr
            end_time = start_time + timedelta(days=interval)
            # print("##", start_time, "##", end_time)
            if end_time >= end_date:
                end_time = end_date
            curr = end_time
            # print("########4", curr)
            # start_time = datetime.datetime.timestamp(start_time)
            # end_time = datetime.datetime.timestamp(end_time)
            # print("##", start_time, "##", end_time)
            # temp = queryset.filter(date__range=[start_time, end_time])
            temp = [i for i in queryset if start_time <= datetime.datetime.strptime(i['transactionDate'], '%Y-%m-%dT%H:%M:%S') <= end_time]
            # print("#### len temp", len(temp))
            # print("temp", temp)
            if operation == "avg":
                # print("@@@3", temp)
                count = len(temp)
                # plus = temp.filter(response_code='00', type__in=['sale', 'installment'])
                # sum = plus.aggregate(Avg('amount'))['amount__avg'] or 0
                # minus = temp.filter(response_code='00', type__in=['void', 'refund'])
                # sum -= minus.aggregate(Avg('amount'))['amount__avg'] or 0
                amount_sum = sum([i['amount'] for i in temp])
                if count:
                    avg = amount_sum / count
                else:
                    avg = 0
                point = avg
            elif operation == "sum":
                # plus = temp.filter(response_code='00', type__in=['sale', 'installment']).aggregate(Sum('amount'))[
                #            'amount__sum'] or 0
                # minus = temp.filter(response_code='00', type__in=['void', 'refund']).aggregate(Sum('amount'))[
                #             'amount__sum'] or 0
                point = sum([i['amount'] for i in temp])
                # point = plus - minus
            else:
                point = len(temp) or 0
            points.append({'time': end_time, 'value': point})
        return points

    @staticmethod
    def calculate_ratio_util(queryset, operation):
        if operation == "avg":
            return queryset.aggregate(Avg('amount'))['amount__avg'] or 0
        elif operation == "sum":
            return queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        else:
            return queryset.count()

    @staticmethod
    def generate_points(queryset, time_frame, date_from, date_to, operation):
        points = []
        interval = 0.1666666667
        if time_frame == 'yesterday':
            start_date = (datetime.datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                                 microsecond=0)
            end_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            interval = 0.1666666667
        elif time_frame == 'current-week':
            today = datetime.datetime.today()
            weekday = (today.weekday() - 5) % 7
            start_date = (today - timedelta(days=weekday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=7)
            interval = 1
        elif time_frame == 'last-week':
            today = datetime.datetime.today()
            weekday = (today.weekday() - 5) % 7
            start_date = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=weekday) - timedelta(
                days=7)
            end_date = start_date + timedelta(7)
            interval = 1
        elif time_frame == 'current-month':
            start_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            days = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = start_date + timedelta(days=days)
            interval = 5
        elif time_frame == 'last-month':
            now = datetime.datetime.now()
            days = calendar.monthrange(now.year, now.month)[1]
            start_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0,
                                                           microsecond=0) - timedelta(days=days)
            end_date = start_date + timedelta(days=days)
            interval = 5
        elif time_frame == 'last-quarter':
            lastQuarter = (int((datetime.date.today().month - 1) // 3) - 1) % 4 + 1
            # print("points:", lastQuarter)
            start_date = datetime.datetime(datetime.date.today().year, (3 * lastQuarter - 2) % 12, 1)
            end_date = datetime.datetime(datetime.date.today().year, (3 * lastQuarter + 1) % 12, 1)
            interval = 21
            # print(start_date, end_date, sep="###")
        elif time_frame == 'today':
            start_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            interval = 0.1666666667
        elif date_from and date_to:
            # time_frame = time_frame[6:]
            start_date = datetime.datetime.strptime(date_from, '%d-%m-%Y')
            end_date = datetime.datetime.strptime(date_to, '%d-%m-%Y') + timedelta(hours=23, minutes=59, seconds=59)
            delta = end_date - start_date
            interval = (delta.days + 1) / 7
            # print("#### interval ####", interval)
            if start_date > end_date:
                return []
        else:
            start_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + timedelta(days=1)
            interval = 0.1666666667
        # print("Generate Points:", start_date, " ## ", end_date)
        points = ChartServices.get_points_util(queryset, interval, start_date, end_date, operation)
        return points

    # @staticmethod
    # def calculate_ratio(request, current, operation):
    #     time_frame = request.GET.get('TimeFrameId')
    #     POSs = Terminal.objects.filter(user_id=request.user, deactivated=False)
    #     queryset = Transactions.objects.filter(terminal_id__in=POSs, response_code='00')
    #     if time_frame == 'yesterday':
    #         start_date = (datetime.datetime.today() - timedelta(days=2)).replace(hour=0, minute=0, second=0,
    #                                                                              microsecond=0)
    #         end_date = (datetime.datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0,
    #                                                                            microsecond=0)
    #     elif time_frame == 'current-week':
    #         today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    #         weekday = (today.weekday() - 5) % 7
    #         start_date = today - timedelta(days=weekday) - timedelta(days=7)
    #         end_date = start_date + timedelta(days=7)
    #     elif time_frame == 'last-week':
    #         today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    #         weekday = (today.weekday() - 5) % 7
    #         start_date = (today - timedelta(days=weekday + 14)).replace(hour=0, minute=0, second=0, microsecond=0)
    #         end_date = start_date + timedelta(days=7)
    #     elif time_frame == 'current-month':
    #         now = datetime.datetime.now()
    #         days = calendar.monthrange(now.year, now.month)[1]
    #         start_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0,
    #                                                        microsecond=0) - timedelta(days=days)
    #         end_date = datetime.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    #     elif time_frame == 'last-month':
    #         today = datetime.datetime.today()
    #         month_before = datetime.datetime(today.year, today.month - 2, 1)
    #         days = calendar.monthrange(month_before.year, month_before.month)[1]
    #         start_date = month_before
    #         end_date = start_date + timedelta(days=days)
    #     elif time_frame == 'last-quarter':
    #         prevQuarter = (int((datetime.date.today().month - 1) // 3) - 2) % 4 + 1
    #         # print("ratio:", prevQuarter)
    #         start_date = datetime.datetime(datetime.date.today().year, (3 * prevQuarter - 2) % 12, 1)
    #         end_date = datetime.datetime(datetime.date.today().year, (3 * prevQuarter + 1) % 12, 1) + timedelta(
    #             microseconds=-1)
    #         # print(start_date, end_date, sep="###")
    #     elif time_frame == 'today':
    #         start_date = (datetime.datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0,
    #                                                                              microsecond=0)
    #         end_date = start_date + timedelta(days=1)
    #     elif date_from and date_to:
    #         # time_frame = time_frame[6:]
    #         start_date = datetime.datetime.strptime(date_from, '%d-%m-%Y')
    #         end_date = datetime.datetime.strptime(date_to, '%d-%m-%Y') + timedelta(hours=23, minutes=59, seconds=59)
    #         delta = end_date - start_date
    #         interval = (delta.days + 1) / 7
    #         print("#### interval ####", interval)
    #         if start_date > end_date:
    #             return []
    #         # print("#####9", type(start_date), end_date)
    #     else:
    #         start_date = (datetime.datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0,
    #                                                                              microsecond=0)
    #         end_date = start_date + timedelta(days=1)
    #     queryset = queryset.filter(date__range=[start_date, end_date])
    #     # print("######2", queryset.values_list('date', flat=True))
    #     temp = ChartServices.calculate_ratio_util(queryset, operation)
    #     # print("######1", start_date, " ## ", end_date)
    #     # print(queryset)
    #     # print("####temp###", temp)
    #     # print("####current###", current)
    #     if temp > 0:
    #         res = (current - temp) / abs(temp) * 100
    #     else:
    #         return 0
    #     return res
