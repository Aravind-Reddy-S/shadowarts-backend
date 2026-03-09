from django.urls import path
from .views import WorkshopListAPIView, book_workshop, login_user, register_user, user_bookings, products_list,chat, reset_password,contact_message
from .views import testimonials_list

urlpatterns = [
    path("workshops/", WorkshopListAPIView.as_view()),
    path("book-workshop/", book_workshop),
    path("login/", login_user),
    path("register/", register_user),
    path("user-bookings/<int:user_id>/", user_bookings),
    path("products/", products_list),
    path("chat/", chat),
    path("reset-password/", reset_password),
    path("contact/", contact_message),
    path("testimonials/", testimonials_list),
]