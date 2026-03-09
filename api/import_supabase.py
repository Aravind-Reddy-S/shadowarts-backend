import requests
from datetime import datetime
from django.contrib.auth.models import User

from .models import (
    Workshop,
    Product,
    Booking,
    Profile,
    Order,
    OrderItem,
    ContactMessage,
    UserRole
)

SUPABASE_BASE = "https://kutfomkqdnwtcatfxdod.supabase.co/rest/v1"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt1dGZvbWtxZG53dGNhdGZ4ZG9kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI1MDk3MjgsImV4cCI6MjA4ODA4NTcyOH0.4JyLiQAXRQluP6HifTr0TwETsvyyhwnu8cM5WVv4Uls"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}


# -------------------------
# WORKSHOPS
# -------------------------

# -------------------------
# WORKSHOPS
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/workshops", headers=headers)

for w in res.json():

    date_value = None
    if w.get("date"):
        date_value = datetime.fromisoformat(
            w["date"].replace("Z", "+00:00")
        ).date()

    # check if already exists
    exists = Workshop.objects.filter(
        title=w.get("title"),
        city=w.get("city"),
        date=date_value
    ).exists()

    if not exists:
        Workshop.objects.create(
            title=w.get("title"),
            description=w.get("description"),
            art_type=w.get("art_type"),
            city=w.get("city"),
            venue=w.get("venue"),
            date=date_value,
            seats_available=w.get("seats_available") or 0,
            price=w.get("price") or 0,
            image_url=w.get("image_url"),
            is_active=w.get("is_active", True),
        )

print("Workshops imported successfully!")

# -------------------------
# PRODUCTS
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/products", headers=headers)

for p in res.json():

    Product.objects.get_or_create(
        name=p.get("name"),
        defaults={
            "description": p.get("description"),
            "price": p.get("price"),
            "image_url": p.get("image_url"),
            "is_active": p.get("is_active", True),
        },
    )

print("Products imported successfully!")


# -------------------------
# PROFILES
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/profiles", headers=headers)

for p in res.json():
    try:
        user = User.objects.get(id=p["user_id"])

        Profile.objects.get_or_create(
            user=user,
            defaults={
                "full_name": p.get("full_name", ""),
                "phone": p.get("phone", "")
            },
        )
    except:
        pass

print("Profiles imported successfully!")


# -------------------------
# BOOKINGS
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/bookings", headers=headers)

for b in res.json():
    try:
        user = User.objects.get(id=b["user_id"])
        workshop = Workshop.objects.get(id=b["workshop_id"])

        Booking.objects.get_or_create(
            user=user,
            workshop=workshop,
            defaults={
                "amount": b.get("amount"),
                "status": b.get("status")
            },
        )
    except:
        pass

print("Bookings imported successfully!")


# -------------------------
# ORDERS
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/orders", headers=headers)

for o in res.json():
    try:
        user = User.objects.get(id=o["user_id"])

        Order.objects.get_or_create(
            id=o.get("id"),
            defaults={
                "user": user,
                "total": o.get("total"),
                "status": o.get("status"),
            },
        )
    except:
        pass

print("Orders imported successfully!")


# -------------------------
# ORDER ITEMS
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/order_items", headers=headers)

for oi in res.json():
    try:
        order = Order.objects.get(id=oi["order_id"])
        product = Product.objects.get(id=oi["product_id"])

        OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={
                "quantity": oi.get("quantity"),
                "price": oi.get("price"),
            },
        )
    except:
        pass

print("Order items imported successfully!")


# -------------------------
# CONTACT MESSAGES
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/contact_messages", headers=headers)

for c in res.json():

    ContactMessage.objects.create(
        name=c.get("name"),
        email=c.get("email"),
        phone=c.get("phone"),
        message=c.get("message"),
    )

print("Contact messages imported successfully!")


# -------------------------
# USER ROLES
# -------------------------

res = requests.get(f"{SUPABASE_BASE}/user_roles", headers=headers)

for r in res.json():
    try:
        user = User.objects.get(id=r["user_id"])

        UserRole.objects.get_or_create(
            user=user,
            role=r.get("role")
        )
    except:
        pass

print("User roles imported successfully!")