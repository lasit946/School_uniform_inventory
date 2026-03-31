# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import UniformItem
from .forms import UniformItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegisterForm
from django.contrib import messages

# ---------------------------
# Admin check function
# ---------------------------
def admin_required(user):
    return user.is_superuser
# ---------------------------
# User registration
# ---------------------------
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'inventory/register.html', {'form': form})

# ---------------------------
# List all items (public)
# ---------------------------
def product_list(request):
    query = request.GET.get('q')  # Search
    sort = request.GET.get('sort') # Sorting

    items = UniformItem.objects.all()

    if query:
        items = items.filter(name__icontains=query)
    if sort == 'name':
        items = items.order_by('name')
    elif sort == 'quantity':
        items = items.order_by('quantity')
    elif sort == 'price':
        items = items.order_by('price')

    return render(request, 'inventory/list.html', {'items': items})

# ---------------------------
# Add item (admin only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def add_product(request):
    if request.method == 'POST':
        form = UniformItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = UniformItemForm()
    return render(request, 'inventory/add.html', {'form': form})

# ---------------------------
# Edit item (admin only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def edit_product(request, pk):
    item = get_object_or_404(UniformItem, pk=pk)
    if request.method == 'POST':
        form = UniformItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = UniformItemForm(instance=item)
    return render(request, 'inventory/edit.html', {'form': form})

# ---------------------------
# Delete item (admin only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def delete_product(request, pk):
    item = get_object_or_404(UniformItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('product_list')
    return render(request, 'inventory/delete.html', {'item': item})

