from django.contrib.auth.models import User
from django.db import models

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 star rating
    comment = models.TextField(blank=True)  # Optional comment
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Show latest ratings first
