from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, GoalsSerializer, NutritionSerializer, ExerciseSerializer, BodyPartSerializer, InspirationalVideoSerializer, RecpieSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import GoalsProfileQuestions, NutritionProfileQuestions, Body_Part, Exercise, InspirationalVideoLink, Recipe
import requests
from .algorithms import calculate_calories, get_macronutrient_ratios
from bs4 import BeautifulSoup

# Create your views here.

EXERCISE_API_KEY = "DQkj6i8AxB/G72a+bC7mLw==fM8MQJZua9k44Lz9"
NUTRITION_API_KEY = "84d12c98deeb46cbabcc842ea5b0af67"
YOUTUBE_API_KEY = "AIzaSyCpbsfCRnsgdzjN5-uEslF66YqWbo7AtsE"

class UserRegistrationView2(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except serializer.ValidationError as e:
            return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class UserGoalsFormCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = GoalsProfileQuestions.objects.all()
    serializer = GoalsSerializer

class UserGoalsFormCreate(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = GoalsProfileQuestions.objects.all()
    serializer = GoalsSerializer

class RecipeCRUD(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Recipe.objects.all()
    serializer = RecpieSerializer

class UserNutritionFormCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = NutritionProfileQuestions.objects.all()
    serializer = NutritionSerializer

class UserNutritionFormCreate(CreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = NutritionProfileQuestions.objects.all()
    serializer = NutritionSerializer

class BodyPartCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = NutritionProfileQuestions.objects.all()
    serializer = NutritionSerializer

class ExerciseCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Exercise.objects.all()
    serializer = ExerciseSerializer

class InspirationalVideoCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = InspirationalVideoLink.objects.all()
    serializer = InspirationalVideoSerializer

class BodyPartCRUD(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Body_Part.objects.all()
    serializer = BodyPartSerializer


class FitnessAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        exercises_list = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        user = request.user
        goals = GoalsProfileQuestions.objects.filter(user=user)

        if goals.exist():
            level = goals.first().fitness_level
            type = goals.first().fitness_goal
            exercise_data = []
            for body_part in exercises_list:
                muscle = body_part
                api_url = 'https://api.api-ninjas.com/v1/exercises?muscle={}&type={}&difficulty={}'.format(
                        muscle, type, level
                )

                body_part = Body_Part(name=muscle)
                response = requests.get(api_url, headers={'X-Api-Key': EXERCISE_API_KEY})

                for exercise in response:
                    exercise_name = exercise.get('name')
                    exercise_type = exercise.get('type')
                    exercise_muscle = exercise.get('muscle')
                    exercise_equipment = exercise.get('equipment')
                    exercise_difficulty = exercise.get('difficulty')
                    exercise_instructions = exercise.get('instructions')
                
                    exercise = Exercise(name=exercise_name, type=exercise_type, 
                                        muscle=exercise_muscle, equipment=exercise_equipment,
                                        difficulty=exercise_difficulty, instructions=exercise_instructions)

                    exercise.save()
                if response.status_code == requests.codes.ok:
                # Return the response content as the API response
                    return Response(response.json(), status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Error fetching data from the API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NutritionAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        nutrition_profile = NutritionProfileQuestions.objects.get(user=user)
        goals_profile = GoalsProfileQuestions.objects.get(user=user)

        calories = calculate_calories(user.age, user.gender, user.weight, user.height, goals_profile.body_type,
                                      goals_profile.body_fat_percentage_goal, goals_profile.activity_level)
        
        ratios_list = get_macronutrient_ratios(goals_profile.primary_goal, nutrition_profile.num_of_meals,
                                               user.gender)
        
        min_protein_grams = ratios_list[0] * calories / 4 / nutrition_profile.num_of_meals
        max_protein_grams = ratios_list[1] * calories / 4 / nutrition_profile.num_of_meals
        min_carb_grams = ratios_list[2] * calories / 4 / nutrition_profile.num_of_meals
        max_carb_grams = ratios_list[3] * calories / 4 / nutrition_profile.num_of_meals
        min_fat_grams = ratios_list[4] * calories / 9 / nutrition_profile.num_of_meals
        max_fat_grams = ratios_list[5] * calories / 9 / nutrition_profile.num_of_meals

        api_url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
                
                "apiKey" : NUTRITION_API_KEY,
                "number" : 5,
                "minCarbs" : min_carb_grams,
                "maxCarbs" : max_carb_grams,
                "minProtein" : min_protein_grams,
                "maxProtein" : max_protein_grams,
                "minCalories" : calories - 100,
                "maxCalories" : calories + 100,
                "minFat" : min_fat_grams,
                "maxFat" : max_fat_grams,
                "minVitaminA" : ratios_list[6],
                "maxVitaminA" : ratios_list[6],
                "minFiber" : ratios_list[7],
                "maxFiber" : ratios_list[8]

        }
        response = requests.get(f'{api_url}', params=params)
        if response.status_code == 200:
            data = response.json()
    # Process the response data (data contains the API response)
        else:
            print('Error:', response.status_code)
            
        for result in data.get("results", []):
            recipe_id = result.get("id")
            title = result.get("title")
            image = result.get("image")
            image_type = result.get("imageType")

            # Create a new Recipe instance
            recipe = Recipe.objects.create(
                recipe_id=recipe_id,
                title=title,
                image=image,
                image_type=image_type
            )

            # You can perform additional processing or save the instance to the database
            recipe.save()



class inspirational_videos_youtube_api(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        try:
            user = request.user
            profile = GoalsProfileQuestions.objects.get(user=user)
            inspirations = profile.inspirations
            for person_name in inspirations:
                search_query = person_name

# URL for the YouTube Data API search endpoint
                search_url = f"https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&part=snippet&type=video&q={search_query}"

                # Send GET request to the API endpoint
                response = requests.get(search_url)
                data = response.json()

                # Extract video IDs from the search results
                video_ids = [item["id"]["videoId"] for item in data["items"]]

                # Construct video URLs using the video IDs
                video_urls = [f"https://www.youtube.com/watch?v={video_id}" for video_id in video_ids[:5]]

                for url in video_urls:

                    video = InspirationalVideoLink(user=user, video_link=url)
                    video.save()
                return Response({'message': 'Web scraping completed successfully'}, status=status.HTTP_200_OK)
        except GoalsProfileQuestions.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
