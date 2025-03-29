from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Expense URLs
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_add, name='expense_add'),
    path('expenses/<int:pk>/edit/', views.expense_edit, name='expense_edit'),
    path('expenses/<int:pk>/delete/', views.expense_delete, name='expense_delete'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Group Expense URLs
    path('group-expenses/', views.group_expense_list, name='group_expense_list'),
    path('group-expenses/add/', views.group_expense_add, name='group_expense_add'),
    path('group-expenses/<int:pk>/', views.group_expense_detail, name='group_expense_detail'),
    path('shares/<int:pk>/mark-paid/', views.mark_share_paid, name='mark_share_paid'),
]