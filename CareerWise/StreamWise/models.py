from django.contrib.auth.models import User
from django.db import models

class UserResponse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    recommended_stream = models.CharField(max_length=100)
    math_score = models.IntegerField(default=0)
    physics_score = models.IntegerField(default=0)
    chemistry_score = models.IntegerField(default=0)
    biology_score = models.IntegerField(default=0)
    computer_science_score = models.IntegerField(default=0)
    accountancy_score = models.IntegerField(default=0)
    business_studies_score = models.IntegerField(default=0)
    economics_score = models.IntegerField(default=0)
    history_score = models.IntegerField(default=0)
    geography_score = models.IntegerField(default=0)
    political_science_score = models.IntegerField(default=0)
    psychology_score = models.IntegerField(default=0)
    sociology_score = models.IntegerField(default=0)
    philosophy_score = models.IntegerField(default=0)
    languages_score = models.IntegerField(default=0)
