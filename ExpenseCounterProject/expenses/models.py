from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.description[:20]}"


class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    users = models.ManyToManyField(User, through='ExpenseShare')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_expenses', default=None)

    def __str__(self):
        return f"{self.name} - {self.amount}"

    def split_expense(self):
        num_users = self.users.count()
        if num_users > 0:
            return self.amount / num_users
        return self.amount


class ExpenseShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_expense = models.ForeignKey(GroupExpense, on_delete=models.CASCADE)
    share_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s share of {self.group_expense.name}"



