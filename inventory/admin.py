from django.contrib import admin
from .models import UniformItem, Sale

# 1. Design for the Uniform Inventory Table
@admin.register(UniformItem)
class UniformItemAdmin(admin.ModelAdmin):
    # This adds actual columns so you don't just see the name
    list_display = ('name', 'size', 'quantity', 'price')
    
    # This adds a filter sidebar on the right (Great for Cebu Eastern College's many sizes!)
    list_filter = ('size',)
    
    # This adds a search bar at the top
    search_fields = ('name',)
    
    # This makes the quantity and price editable directly in the list
    list_editable = ('quantity', 'price')

# 2. Design for the Sales Records
@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity_sold', 'sale_date', 'sold_by')
    list_filter = ('sale_date', 'sold_by')
    date_hierarchy = 'sale_date' # Adds a "timeline" at the top