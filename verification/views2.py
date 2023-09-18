from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, GoalsSerializer, NutritionSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from .models import StravaToken
from .serializers import StravaTokenSerializer
import requests
from .algorithms import calculate_calories, get_macronutrient_ratios
from bs4 import BeautifulSoup


CLIENT_ID = "112353"
CLIENT_SECRET = "f7eb8f2c8e3d1763bb5c29bbfe3a57db5311ed54"
TOKEN_URL = "https://www.strava.com/oauth/token"

class RetrieveToken(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = StravaToken.objects.all()
    serializer = StravaTokenSerializer

class retrieve_tokens(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        auth_code = request.data.get("code")
        payload = {

            "client_id" : CLIENT_ID,
            "client_secret" : CLIENT_SECRET,
            "code" : auth_code,
            "grant_type" : "authorization_code"
        }

        response = requests.post(TOKEN_URL, data=payload)
        data = response.json()

    
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')

        user_tokens = StravaToken(user=user,access_token=access_token, refresh_token=refresh_token)
        user_tokens.save()


class refresh_access_token(APIView):

    def get(self, request):
        user = request.user
        token_model = StravaToken(user=user)
        refresh_token = token_model.refresh_token
        payload = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        response = requests.post(TOKEN_URL, data=payload)
        data = response.json()

        new_access_token = data.get('access_token')
        token_model.access_token = new_access_token
        token_model.save()

