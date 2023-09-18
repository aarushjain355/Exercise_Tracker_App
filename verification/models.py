from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MinLengthValidator

class User(AbstractUser):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    height = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    weight = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    username = None
    birth_month = models.CharField(max_length=244)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class GoalsProfileQuestions(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body_type = models.CharField(max_length=135)
    fitness_goal = models.CharField(max_length=135)
    fitness_level = models.CharField(max_length=135)
    primary_goal = models.CharField(max_length=135)
    body_fat_percentage_goal = models.PositiveIntegerField(default=10, validators=[MinValueValidator(0)])
    activity_level = models.CharField(max_length=135)
    motivation = models.CharField(max_length=135)
    inspirations = ArrayField(models.CharField(max_length=135), size=3)

class NutritionProfileQuestions(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dietary_restrictions = models.CharField(max_length=135)
    num_of_meals = models.CharField(max_length=135)
    meal_size = models.CharField(max_length=135)
    macronutrient_goals = models.CharField(max_length=135)
    target_daily_calorie_intake = models.PositiveIntegerField(default=2000)
    meals_per_day = models.CharField(max_length=135)
    allergies = ArrayField(models.CharField(max_length=135), size=3)
    suplements_taken = ArrayField(models.CharField(max_length=135), size=3)
    health_conditions = ArrayField(models.CharField(max_length=135), size=3)


class Body_Part(models.Model):

    name = models.CharField(max_length=135)
    exercises = models.ManyToManyField("Exercise")
    
class Exercise(models.Model):

    name = models.CharField(max_length=135)
    type = models.CharField(max_length=135)
    muscle = models.ForeignKey(Body_Part, on_delete=models.CASCADE)
    equipment = models.CharField(max_length=135)
    difficulty = models.CharField(max_length=135)
    instructions = models.TextField(validators=[MinLengthValidator(15)])


class InspirationalVideoLink(models.Model):
    user = models.ManyToManyField("User")
    video_link = models.URLField()

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.PositiveIntegerField(unique = True)
    title = models.CharField(max_length=255)
    image = models.URLField()
    image_type = models.CharField(max_length=10)
    

class StravaToken(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    
# Create your models here.
