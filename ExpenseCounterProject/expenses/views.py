from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Expense, Category, GroupExpense, ExpenseShare
from .filters import ExpenseFilter, GroupExpenseFilter
from .forms import ExpenseForm, CategoryForm, GroupExpenseForm


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    user_shares = ExpenseShare.objects.filter(user=request.user)
    total_shares = user_shares.aggregate(Sum('share_amount'))['share_amount__sum'] or 0

    categories = Category.objects.filter(user=request.user)
    category_expenses = []
    for category in categories:
        amount = expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0
        category_expenses.append({
            'name': category.name,
            'amount': amount
        })

    context = {
        'total_expenses': total_expenses,
        'total_shares': total_shares,
        'category_expenses': category_expenses,
    }
    return render(request, 'expenses/dashboard.html', context)


# Individual Expense Views
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    expense_filter = ExpenseFilter(request.GET, queryset=expenses, user=request.user)

    context = {
        'filter': expense_filter,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_add(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(user=request.user)

    return render(request, 'expenses/expense_form.html', {'form': form})


@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense, user=request.user)

    return render(request, 'expenses/expense_form.html', {'form': form, 'expense': expense})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('expense_list')

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


# Category Views
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenses/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'expenses/category_form.html', {'form': form})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'expenses/category_form.html', {'form': form, 'category': category})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')

    return render(request, 'expenses/category_confirm_delete.html', {'category': category})


# Group Expense Views
@login_required
def group_expense_list(request):
    user_group_expenses = GroupExpense.objects.filter(users=request.user).order_by('-date')
    expense_filter = GroupExpenseFilter(request.GET, queryset=user_group_expenses, user=request.user)

    context = {
        'filter': expense_filter,
    }
    return render(request, 'expenses/group_expense_list.html', context)


@login_required
def group_expense_add(request):
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            group_expense = form.save(commit=False)
            group_expense.created_by = request.user
            group_expense.save()

            # Get the selected users and add the creator
            selected_users = form.cleaned_data['users']
            if request.user not in selected_users:
                selected_users = list(selected_users)
                selected_users.append(request.user)

            # Save users to the many-to-many relationship
            group_expense.users.set(selected_users)

            # Calculate equal shares for each user
            share_amount = group_expense.amount / len(selected_users)

            # Create ExpenseShare objects for each user
            for user in selected_users:
                ExpenseShare.objects.create(
                    user=user,
                    group_expense=group_expense,
                    share_amount=share_amount,
                    paid=(user == request.user)  # Mark as paid for the creator
                )

            messages.success(request, 'Group expense added successfully!')
            return redirect('group_expense_list')
    else:
        form = GroupExpenseForm(user=request.user)

    return render(request, 'expenses/group_expense_form.html', {'form': form})


@login_required
def group_expense_detail(request, pk):
    group_expense = get_object_or_404(GroupExpense, pk=pk, users=request.user)
    shares = ExpenseShare.objects.filter(group_expense=group_expense)

    context = {
        'expense': group_expense,
        'shares': shares,
    }
    return render(request, 'expenses/group_expense_detail.html', context)


@login_required
def mark_share_paid(request, pk):
    share = get_object_or_404(ExpenseShare, pk=pk, user=request.user)

    if request.method == 'POST':
        share.paid = True
        share.save()
        messages.success(request, 'Share marked as paid!')
        return redirect('group_expense_detail', pk=share.group_expense.pk)

    return render(request, 'expenses/share_confirm_payment.html', {'share': share})
