from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Dish, STATUS_CHOICES
from .forms import OrderForm, DishForm

class OrderListView(generic.ListView):
    model = Order
    template_name = 'orders/list.html'

    def get_queryset(self):
        query = self.request.GET.get('search', '').strip()

        if query:
            status = next((db for db, real in STATUS_CHOICES if real.lower() == query.lower()), None)

            if status:
                return Order.objects.filter(status=status)
            elif query.isdigit():
                return Order.objects.filter(table_number=query)
            else:
                return None

        return Order.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices'] = STATUS_CHOICES
        return context


class OrderCreateView(generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create.html'
    success_url = reverse_lazy('orders:list')


class DishCreateView(generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'orders/create_dish.html'
    success_url = reverse_lazy('orders:list')

def get_revenue(request):
    queryset = Order.objects.filter(status='paid')
    revenue = sum(order.total_price for order in queryset)
    template_name = 'orders/revenue.html'
    return render(request, template_name, {'revenue': revenue})

def delete_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    order.delete()
    success_url = reverse_lazy('orders:list')
    return redirect(success_url)

def update_order_status(request, pk):
    order = get_object_or_404(Order, id=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status:
            order.status = new_status
            order.save()

    return redirect('orders:list')