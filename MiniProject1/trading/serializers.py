from rest_framework import serializers
from .models import Order
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'product_id', 'order_type', 'quantity', 'price', 'timestamp']
        read_only_fields = ['user', 'timestamp']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)