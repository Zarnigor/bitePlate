"""
Django Admin registrations for all BitePlate models.
Access at /admin/ after creating a superuser.
"""
from django.contrib import admin


# ── Tables ────────────────────────────────────────────────────
from apps.tables.models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['number', 'capacity', 'status', 'location']
    list_filter = ['status']
    search_fields = ['number', 'location']
    ordering = ['number']


# ── Reservations ──────────────────────────────────────────────
from apps.reservations.models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'party_size', 'reserved_at', 'status', 'reminder_sent']
    list_filter = ['status', 'reminder_sent']
    search_fields = ['customer_name', 'customer_phone']
    date_hierarchy = 'reserved_at'
    ordering = ['reserved_at']


# ── Orders ────────────────────────────────────────────────────
from apps.orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['get_line_total']

    def get_line_total(self, obj):
        return f"${obj.get_line_total()}"
    get_line_total.short_description = 'Line Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_id', 'status', 'get_subtotal', 'created_at']
    list_filter = ['status']
    search_fields = ['id', 'table_id', 'staff_id']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at']

    def get_subtotal(self, obj):
        return f"${obj.get_subtotal()}"
    get_subtotal.short_description = 'Subtotal'


# ── Kitchen ───────────────────────────────────────────────────
from apps.kitchen.models import KitchenTicket

@admin.register(KitchenTicket)
class KitchenTicketAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'quantity', 'station', 'status', 'created_at']
    list_filter = ['status', 'station']
    search_fields = ['item_name', 'order_id']
    ordering = ['created_at']


# ── Menu ──────────────────────────────────────────────────────
from apps.menu.models import MenuItem, ComboMeal, Allergen

class AllergenInline(admin.TabularInline):
    model = Allergen
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'base_price', 'is_available', 'cooking_station']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'base_price']
    inlines = [AllergenInline]

@admin.register(ComboMeal)
class ComboMealAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount_pct', 'get_price', 'is_available']
    filter_horizontal = ['items']

    def get_price(self, obj):
        return f"${obj.get_price()}"
    get_price.short_description = 'Combo Price'


# ── Billing ───────────────────────────────────────────────────
from apps.billing.models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_id', 'total', 'pricing_strategy', 'is_paid', 'split_count', 'created_at']
    list_filter = ['is_paid', 'pricing_strategy']
    search_fields = ['order_id', 'table_id']
    readonly_fields = ['created_at']


# ── Staff ─────────────────────────────────────────────────────
from django.contrib.auth.admin import UserAdmin
from apps.staff.models import StaffMember

@admin.register(StaffMember)
class StaffMemberAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'role', 'email', 'is_active']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    fieldsets = UserAdmin.fieldsets + (
        ('Restaurant Role', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Restaurant Role', {'fields': ('role', 'phone')}),
    )
