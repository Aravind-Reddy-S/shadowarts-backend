from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import os
import json

from .models import (
    Workshop,
    Booking,
    Product,
    ContactMessage,
    Testimonial
)

from .serializers import (
    WorkshopSerializer,
    ProductSerializer,
    TestimonialSerializer
)


# ---------------------------------
# WORKSHOPS
# ---------------------------------

class WorkshopListAPIView(generics.ListAPIView):
    queryset = Workshop.objects.filter(is_active=True).order_by("date")
    serializer_class = WorkshopSerializer


# ---------------------------------
# BOOK WORKSHOP
# ---------------------------------

@csrf_exempt
@api_view(["POST"])
def book_workshop(request):

    user_id = request.data.get("user_id")
    workshop_id = request.data.get("workshop_id")

    try:
        workshop = Workshop.objects.get(id=workshop_id)
    except Workshop.DoesNotExist:
        return Response({"error": "Workshop not found"}, status=404)

    if workshop.seats_available <= 0:
        return Response({"error": "No seats available"}, status=400)

    user = User.objects.get(id=user_id)

    Booking.objects.create(
        user=user,
        workshop=workshop,
        amount=workshop.price,
        status="confirmed",
    )

    workshop.seats_available -= 1
    workshop.save()

    return Response(
        {"message": "Workshop booked successfully"},
        status=status.HTTP_201_CREATED,
    )


# ---------------------------------
# REGISTER USER
# ---------------------------------

@csrf_exempt
@api_view(["POST"])
def register_user(request):

    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields required"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    return Response({
        "message": "User registered successfully",
        "user_id": user.id
    })


# ---------------------------------
# LOGIN USER
# ---------------------------------

@csrf_exempt
@api_view(["POST"])
def login_user(request):

    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"error": "Email and password required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=400)

    user = authenticate(username=user.username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    return Response({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    })


# ---------------------------------
# USER BOOKINGS
# ---------------------------------

@api_view(["GET"])
def user_bookings(request, user_id):

    bookings = Booking.objects.filter(user_id=user_id)

    data = []

    for b in bookings:
        w = b.workshop

        data.append({
            "id": b.id,
            "amount": b.amount,
            "status": b.status,
            "workshop_title": w.title,
            "city": w.city,
            "venue": w.venue,
            "date": w.date
        })

    return Response(data)


# ---------------------------------
# PRODUCTS
# ---------------------------------

@api_view(["GET"])
def products_list(request):

    products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


# ---------------------------------
# CONTACT FORM
# ---------------------------------

@csrf_exempt
@api_view(["POST"])
def contact_message(request):

    name = request.data.get("name")
    email = request.data.get("email")
    phone = request.data.get("phone")
    message = request.data.get("message")

    if not name or not email or not message:
        return Response({"error": "Missing fields"}, status=400)

    ContactMessage.objects.create(
        name=name,
        email=email,
        phone=phone,
        message=message
    )

    return Response({"message": "Message sent successfully"})


# ---------------------------------
# TESTIMONIALS
# ---------------------------------

@api_view(["GET"])
def testimonials_list(request):

    testimonials = Testimonial.objects.filter(is_active=True).order_by("-created_at")

    serializer = TestimonialSerializer(testimonials, many=True)

    return Response(serializer.data)


# ---------------------------------
# RESET PASSWORD
# ---------------------------------

@csrf_exempt
@api_view(["POST"])
def reset_password(request):

    password = request.data.get("password")

    if not password:
        return Response({"error": "Password required"}, status=400)

    user = request.user
    user.set_password(password)
    user.save()

    return Response({"message": "Password updated"})


# ---------------------------------
# CHATBOT
# ---------------------------------

@csrf_exempt
def chat(request):

    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return JsonResponse({
            "reply": "The AI assistant is currently being set up. Please try again later."
        })

    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    data = json.loads(request.body)
    messages = data.get("messages", [])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content

    return JsonResponse({"reply": reply})