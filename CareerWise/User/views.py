from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.db import IntegrityError
from Ratings.models import Rating
import logging


logger = logging.getLogger(__name__)

def index(request):
    ratings = Rating.objects.all()
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    total_ratings = ratings.count()
    rating_counts = [{'rating': i, 'count': ratings.filter(rating=i).count(), 'percent_of_total': (ratings.filter(rating=i).count() / total_ratings) * 100} for i in range(1, 6)]

    # Pass ratings data to the template
    return render(request, 'index.html', {'average_rating': average_rating, 'total_ratings': total_ratings, 'rating_counts': rating_counts})

def home(request):
    return render(request, 'home.html')
def user_logout(request):
    auth_logout(request)  # Use the auth_logout function to log the user out
    logger.info("User logged out successfully")
    return redirect('index')

def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            logger.info("User %s logged in successfully", user)
            return redirect('home')
        else:
            context['error'] = "Invalid username or password."

    return render(request, 'login.html', context)

def signup(request):
    context = {}  # Initialize context dictionary
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Create user using create_user method
            user = User.objects.create_user(username=username, email=email, password=password)
            logger.info("User %s created successfully", user)
            return redirect('login')
        except IntegrityError as e:
            # Handle unique constraint violation (e.g., username or email already exists)
            error_message = str(e)
            if 'username' in error_message:
                context['error'] = "Username already exists. Please choose a different one."
            elif 'email' in error_message:
                context['error'] = "Email already exists. Please use a different one."
            else:
                context['error'] = "An error occurred. Please try again."
            return render(request, 'signup.html', context)

    return render(request, 'signup.html')
def viewratings(request):
    ratings = Rating.objects.all()
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    total_ratings = ratings.count()
    rating_counts = [{'rating': i, 'count': ratings.filter(rating=i).count(), 'percent_of_total': (ratings.filter(rating=i).count() / total_ratings) * 100} for i in range(1, 6)]
    return render(request, 'index.html', {'ratings': ratings, 'average_rating': average_rating, 'total_ratings': total_ratings, 'rating_counts': rating_counts})
