from django import forms
from .models import Order, Dish
from django.core.exceptions import ValidationError
from django.db import transaction
class DishForm(forms.ModelForm):

    class Meta:
        model = Dish
        fields = ('name', 'price')

class OrderForm(forms.ModelForm):
    new_dish_name = forms.CharField(
        max_length=64,
        label='Новое блюдо',
        required=False
    )
    new_dish_price = forms.IntegerField(
        min_value=0,
        label='Цена нового блюда',
        required=False
    )
    items = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Блюда:'
    )

    class Meta:
        model = Order
        fields = ('table_number', 'items')

    def clean(self):
        cleaned_data = super().clean()
        new_name = cleaned_data.get('new_dish_name')
        new_price = cleaned_data.get('new_dish_price')
        items = cleaned_data.get('items')

        if not items and not new_name:
            self.add_error('items', "В заказе должно быть хотябы 1 блюдо.")

        return cleaned_data

    def save(self, commit=True):
        order = super().save(commit=False)

        new_name = self.cleaned_data.get('new_dish_name')
        new_price = self.cleaned_data.get('new_dish_price')
        items = self.cleaned_data.get('items')

        if not items and not new_name:
            raise ValidationError('В заказе должно быть хотябы 1 блюдо.')
        
        with transaction.atomic():
            order.save()

            if new_name and new_price is not None and new_price >= 0:
                dish = Dish.objects.create(name=new_name, price=new_price)
                order.items.add(dish)

            if items:
                order.items.add(*items)

            order.save()

        return order
