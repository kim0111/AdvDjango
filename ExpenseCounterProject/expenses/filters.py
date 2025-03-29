import django_filters
from django import forms

from expenses.models import Expense, Category, GroupExpense


class ExpenseFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte',
                                          widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte',
                                        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseFilter, self).__init__(*args, **kwargs)
        if user:
            self.filters['category'].queryset = Category.objects.filter(user=user)


class GroupExpenseFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte',
                                          widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte',
                                        widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = GroupExpense
        fields = ['category']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(GroupExpenseFilter, self).__init__(*args, **kwargs)
        if user:
            self.filters['category'].queryset = Category.objects.filter(user=user)
