from django.contrib import admin
from .models import Workshop, Booking, Product, Order, OrderItem, ContactMessage, Profile, Testimonial


# -------------------------------
# WORKSHOPS
# -------------------------------

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "art_type",
        "city",
        "date",
        "price",
        "seats_available",
        "is_active"
    )

    list_filter = (
        "city",
        "art_type",
        "is_active",
        "date"
    )

    search_fields = (
        "title",
        "city",
        "venue"
    )

    ordering = ("-date",)


# -------------------------------
# BOOKINGS
# -------------------------------

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "workshop",
        "amount",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
        "created_at"
    )

    search_fields = (
        "user__username",
        "workshop__title"
    )

    ordering = ("-created_at",)


# -------------------------------
# PRODUCTS
# -------------------------------

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "is_active"
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
    )


# -------------------------------
# ORDERS
# -------------------------------

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "total",
        "status",
        "created_at"
    )

    list_filter = (
        "status",
        "created_at"
    )

    search_fields = (
        "user__username",
    )

    inlines = [OrderItemInline]

    ordering = ("-created_at",)


# -------------------------------
# CONTACT MESSAGES
# -------------------------------

@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "phone",
        "created_at",
        "is_read"
    )

    list_filter = (
        "is_read",
        "created_at"
    )

    search_fields = (
        "name",
        "email"
    )


# -------------------------------
# USER PROFILES
# -------------------------------

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "phone",
    )

    search_fields = (
        "user__username",
        "phone"
    )

# -------------------------------
# TESTIMONIALS
# -------------------------------

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "role",
        "rating",
        "is_active",
        "created_at"
    )

    list_filter = (
        "is_active",
        "rating",
        "created_at"
    )

    search_fields = (
        "name",
        "role"
    )

    ordering = ("-created_at",)    