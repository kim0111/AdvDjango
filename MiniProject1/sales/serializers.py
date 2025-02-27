from rest_framework import serializers
from .models import SalesOrder, Invoice, SalesOrderItem
from products.models import Product  # Import Product model


class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ["id", "product_id", "quantity", "price", "subtotal"]


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, write_only=True)
    discount_percent = serializers.DecimalField(
        max_digits=5, decimal_places=2, required=False
    )

    class Meta:
        model = SalesOrder
        fields = [
            "id",
            "user",
            "status",
            "discount_percent",
            "created_at",
            "items",
            "total",
        ]
        read_only_fields = ["user", "total", "status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        sales_order = SalesOrder.objects.create(**validated_data)
        for item_data in items_data:
            SalesOrderItem.objects.create(
                sales_order=sales_order,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                price=item_data["price"],
            )
        return sales_order


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "sales_order", "generated_at"]
        read_only_fields = ["generated_at"]