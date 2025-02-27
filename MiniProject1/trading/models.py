from django.db import models


class Order(models.Model):
    ORDER_TYPES = [('buy', 'Buy'), ('sell', 'Sell')]
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type.upper()} #{self.id} - {self.product.name} x {self.quantity}"

    