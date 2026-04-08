from django.shortcuts import render, redirect, get_object_or_404
from .models import UniformItem, Sale
from .forms import UniformItemForm, UserRegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum # Added Sum here
from django.utils import timezone # Added timezone here

# ---------------------------
# SECURITY: Admin check function
# ---------------------------
def admin_required(user):
    """Checks if the logged-in user is a Superuser/Admin."""
    return user.is_superuser

# ---------------------------
# FUNCTION 1: User Registration
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
@login_required
def product_list(request):
    query = request.GET.get('q')  
    sort = request.GET.get('sort') 

    items = UniformItem.objects.all()

    if query:
        items = items.filter(name__icontains=query)
    
    if sort in ['name', 'quantity', 'price']:
        items = items.order_by(sort)
    else:
        items = items.order_by('name') # Default sorting

    # --- NEW: Calculate Today's Total Sold ---
    today = timezone.now().date()
    # Sums quantity_sold for all Sale records created today
    total_sold_today = Sale.objects.filter(sale_date__date=today).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0

    return render(request, 'inventory/list.html', {
        'items': items,
        'total_sold_today': total_sold_today # Pass this to your HTML
    })
# ---------------------------
# FUNCTION 3: Sell
# ---------------------------
@login_required
@user_passes_test(admin_required)
def sell_item(request, pk):
    item = get_object_or_404(UniformItem, pk=pk)
    
    if request.method == 'POST':
        # Get the quantity from the input field, default to 1
        qty_to_sell = int(request.POST.get('sell_qty', 1))
        
        if item.quantity >= qty_to_sell:
            item.quantity -= qty_to_sell
            item.save()
            
            # Record the sale with the specific quantity
            Sale.objects.create(
                item=item, 
                quantity_sold=qty_to_sell, 
                sold_by=request.user
            )
            messages.success(request, f"Successfully sold {qty_to_sell} units of {item.name}!")
        else:
            messages.error(request, f"Not enough stock! Only {item.quantity} left.")
            
    return redirect('product_list')
# ---------------------------
# FUNCTION 4: Sales Report (In-Demand Analytics)
# ---------------------------
@login_required
def sales_report(request):
    """Shows history and calculates demand based on your handwritten notes."""
    sales_history = Sale.objects.all().order_by('-sale_date')
    
    # Analytics: Which sizes are selling the fastest?
    # This fulfills the "In Demand" tracking for reordering.
    demand_stats = Sale.objects.values('item__size').annotate(total_sold=Count('id')).order_by('-total_sold')

    return render(request, 'inventory/sales_report.html', {
        'sales_history': sales_history,
        'demand_stats': demand_stats
    })

# ---------------------------
# FUNCTION 5: Add New Item (Admin Only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def add_product(request):
    if request.method == 'POST':
        form = UniformItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New item added successfully!")
            return redirect('product_list')
    else:
        form = UniformItemForm()
    return render(request, 'inventory/add.html', {'form': form})

# ---------------------------
# FUNCTION 6: Edit Item (Admin Only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def edit_product(request, pk):
    item = get_object_or_404(UniformItem, pk=pk)
    if request.method == 'POST':
        # Get the 'add_amount' from the form
        try:
            add_amount = int(request.POST.get('add_stock', 0))
            if add_amount < 0:
                messages.error(request, "You cannot add a negative amount!")
            else:
                item.quantity += add_amount # This adds to the existing stock
                item.save()
                messages.success(request, f"Successfully added {add_amount} units to {item.name}.")
                return redirect('product_list')
        except ValueError:
            messages.error(request, "Please enter a valid number.")
            
    return render(request, 'inventory/edit.html', {'item': item})
# ---------------------------
# FUNCTION 7: Delete Item (Admin Only)
# ---------------------------
@login_required
@user_passes_test(admin_required)
def delete_product(request, pk):
    item = get_object_or_404(UniformItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.warning(request, "Item removed from system.")
        return redirect('product_list')
    return render(request, 'inventory/delete.html', {'item': item})
