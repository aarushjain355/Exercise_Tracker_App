from rest_framework import serializers
from .models import User, GoalsProfileQuestions, NutritionProfileQuestions, Exercise, Body_Part, InspirationalVideoLink, Recipe, StravaToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:

        model = User
        fields = ["first_name", "last_name", "age", "height", "weight", "gender", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_age(self, value):
        if value < 18:

            raise serializers.ValidationError("Age must be at least 18 years old")
        

class GoalsSerializer(serializers.ModelSerializer):

    class Meta:

        model = GoalsProfileQuestions
        fields = "__all__"

class RecpieSerializer(serializers.ModelSerializer):

    class Meta:

        model = Recipe
        fields = "__all__"   

class NutritionSerializer(serializers.ModelSerializer):

    class Meta:

        model = GoalsProfileQuestions
        fields = "__all__"


class InspirationalVideoSerializer(serializers.ModelSerializer):

    class Meta:

        model = InspirationalVideoLink
        fields = "__all__"

    

class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:

        model = Exercise
        fields = "__all__"


class BodyPartSerializer(serializers.ModelSerializer):

    class Meta:

        model = Body_Part
        fields = "__all__"

    


class StravaTokenSerializer(serializers.ModelSerializer):

    class Meta:

        model = StravaToken
        fields = "__all__"