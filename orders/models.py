from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


STATUS_CHOICES = (
    ('waiting', 'В ожидании'),
    ('ready', 'Готово'),
    ('paid', 'Оплачено')
    )


class Dish(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64, unique=True)
    price = models.PositiveIntegerField(verbose_name='Цена')
    def __str__(self):
        return f'{self.name}, цена - {self.price}р.'



class Order(models.Model):
    table_number = models.PositiveIntegerField(verbose_name='Номер стола')
    items = models.ManyToManyField(Dish, verbose_name='Блюда', through='OrderDish')
    status = models.CharField(
        verbose_name='Статус',
        choices=STATUS_CHOICES,
        max_length=32,
        default='waiting'
    )
    total_price = models.PositiveIntegerField(verbose_name='Общая стоимость', default=0)
    
    def __str__(self):
        return f'{self.table_number} {self.status}'
    

class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.order} {self.dish}'


@receiver(m2m_changed, sender=OrderDish)
def update_total_price(sender, instance, **kwargs):
    instance.total_price = sum(dish.price for dish in instance.items.all())
    instance.save()