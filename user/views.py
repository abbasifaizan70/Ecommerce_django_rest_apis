import json

import requests
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# api/views.py
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


@api_view(["POST"])
def signup(request):
    """
    Create a new user account and return a token upon successful registration.

    Args:
        request (HttpRequest): The HTTP request object containing user data.

    Returns:
        Response: A JSON response containing user information and a token.

    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data["password"])
        user.save()
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        token, _ = Token.objects.get_or_create(user=user)
        response = {
          "user" : {
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
          }, 
          "token": access_token,
        }
        return Response(response, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_description='Authenticate a user and return a token upon successful login.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user.'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the user.'),
        },
        required=['username', 'password']
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Successfully authenticated',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email of the user.'),
                            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name of the user.'),
                            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name of the user.'),
                            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the user.'),
                        }
                    ),
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Access token for the user.')
                }
            )
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Invalid credentials',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message.')
                }
            )
        )
    }
)
@api_view(["POST"])
def login_view(request):
    """
    Authenticate a user and return a token upon successful login.

    Args:
        request (HttpRequest): The HTTP request object containing user credentials.

    Returns:
        Response: A JSON response containing user information and a token.

    """
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        token, _ = Token.objects.get_or_create(user=user)
        response = {
            "user" : {
              "email": user.email,
              "first_name": user.first_name,
              "last_name": user.last_name,
              "username": user.username,
            },
            "token": access_token,
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@swagger_auto_schema(
    method="post",
    operation_description="Authenticate a user using a Google token and return a token upon successful authentication.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["token"],
        properties={
            "token": openapi.Schema(
                type=openapi.TYPE_STRING, description="Google token"
            ),
        },
    ),
    responses={
        200: openapi.Response(
            description="Authentication Successful",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "first_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "last_name": openapi.Schema(type=openapi.TYPE_STRING),
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    "token": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        404: "Invalid or Expired Google Token",
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Authenticate a user using a Google token and return a token upon successful authentication.

    Args:
        request (HttpRequest): The HTTP request object containing the Google token.

    Returns:
        Response: A JSON response containing user information and tokens.

    """
    payload = {"access_token": request.data.get("token")}  # validate the token
    r = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", params=payload)
    data = json.loads(r.text)
    if "error" in data:
        content = {
            "message": {"wrong google token / this google token is already expired."}
        }
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    # create user if not exist
    User = get_user_model()
    try:
        user = User.objects.get(email=data["email"])
    except:
        user = User(
            email=data["email"],
            first_name=data["given_name"],
            last_name=data["family_name"],
            password=make_password(User.objects.make_random_password()),
        )
        user.save()

    access_token = str(refresh.access_token)  
    token1 = RefreshToken.for_user(user)
    token, _ = Token.objects.get_or_create(user=user)
    response = {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "access": str(token1.access_token),
        "refresh": str(token1),
        "token": access_token,
    }
    return Response(response, status=status.HTTP_200_OK)
