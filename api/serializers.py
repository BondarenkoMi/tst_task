from rest_framework import serializers
from orders.models import Dish, Order, STATUS_CHOICES
from rest_framework.validators import ValidationError

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name', 'price')
        read_only_fields = ('id',)

    def create(self, validated_data):
        dish, _ = Dish.objects.get_or_create(name=validated_data['name'], defaults={'price': validated_data['price']})
        return dish


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ('id', 'table_number', 'status', 'total_price', 'items')
        read_only_fields = ('id', 'total_price')

    def create(self, validated_data):
        if 'items' not in validated_data or not validated_data['items']:
            raise ValidationError({"items": ["В заказе должно быть хотя бы одно блюдо."]})

        items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        order.items.set(items)
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)

        if 'items' in validated_data:
            instance.items.set(validated_data['items'])

        instance.save()
        return instance
    
    # def validate(self, attrs):
    #     items = attrs.get('items', [])
    #     if not items:
    #         raise ValidationError({"items": ["В заказе должно быть хотя бы одно блюдо."]})
    #     return super().validate(attrs)
