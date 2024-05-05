from django.contrib.auth.models import User
from django.db.models import Count, Avg
from django.shortcuts import render
from django.http import JsonResponse
from .models import Rating  # Import the Rating model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import datetime

@login_required
def rating(request):
    user = request.user
    existing_rating = Rating.objects.filter(user=user).first()
    context = {'existing_rating': existing_rating}
    return render(request, 'rating.html', context)

@require_POST
def rate(request):
    user = request.user
    rating_value = request.POST.get('rating')
    comment = request.POST.get('comment')  # Update to get 'comment' instead of 'comments'

    existing_rating = Rating.objects.filter(user=user).first()

    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.comment = comment
        existing_rating.save()
    else:
        new_rating = Rating(user=user, rating=rating_value, comment=comment)
        new_rating.save()

    return JsonResponse({'message': 'Rating and comment saved successfully!'})

def viewrating(request):
    ratings = Rating.objects.all()
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    total_ratings = ratings.count()
    rating_counts = [{'rating': i, 'count': ratings.filter(rating=i).count(), 'percent_of_total': (ratings.filter(rating=i).count() / total_ratings) * 100} for i in range(1, 6)]
    return render(request, 'viewrating.html', {'ratings': ratings, 'average_rating': average_rating, 'total_ratings': total_ratings, 'rating_counts': rating_counts})
