from django.db import models
from django.contrib.auth.models import User


class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    art_type = models.CharField(max_length=50)

    city = models.CharField(max_length=100)
    venue = models.CharField(max_length=200)

    date = models.DateField()

    seats_available = models.IntegerField()
    price = models.IntegerField()

    image_url = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)

    amount = models.IntegerField()
    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.workshop.title}"


class Product(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    image_url = models.URLField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ----------------------------
# PROFILE
# ----------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username


# ----------------------------
# ORDERS
# ----------------------------

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)


# ----------------------------
# CONTACT
# ----------------------------

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)

    email = models.EmailField()

    phone = models.CharField(max_length=20, blank=True)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    is_read = models.BooleanField(default=False)


# ----------------------------
# USER ROLES
# ----------------------------

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Testimonial(models.Model):

    name = models.CharField(max_length=100)

    role = models.CharField(max_length=100)

    message = models.TextField(blank=True)

    rating = models.IntegerField(default=5)

    video = models.FileField(upload_to="testimonials/videos/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name