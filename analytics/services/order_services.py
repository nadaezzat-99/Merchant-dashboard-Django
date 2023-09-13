

class OrderServices:

    @staticmethod
    def order_query(request, queryset):
        print('order by date')
        order = []
        if request.GET.get('s-history') == 'new-first':
            order.append('-date')
        elif request.GET.get('s-history') == 'old-first':
            order.append('date')
        if request.GET.get('s-value') == 'largest-first':
            order.append('-amount')
        elif request.GET.get('s-value') == 'smallest-first':
            order.append('amount')
        if order:
            queryset = queryset.order_by(*order)
        return queryset


