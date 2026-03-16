from django.views.generic import TemplateView

from .models import Order


class DashboardView(TemplateView):

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.all().recent()

        total_profit = sum(order.profit() for order in orders)

        context["total_orders"] = orders.count()
        context["pending_orders"] = Order.objects.pending().count()
        context["completed_orders"] = Order.objects.completed().count()
        context["orders"] = orders

        context["total_revenue"] = Order.objects.total_revenue()
        context["total_distance"] = Order.objects.total_distance()
        context["total_profit"] = total_profit

        return context
