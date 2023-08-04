import re
from django.http import JsonResponse
import jwt
from pymongo import MongoClient
from django.conf import settings
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["faceswap"]


def authenticate_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return JsonResponse({"error": "Authorization header missing."}, status=401)

        try:
            _, token = auth_header.split(' ')

            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256")
            email = payload.get('email')
            user = db.users.find_one({"email": email})
            if not user:
                return JsonResponse({"error": "User not found."}, status=404)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token."}, status=401)

        request.user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def strong_password(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)

        if not password:
            return JsonResponse({"error": "Password field is empty."}, status=400)

        if len(password) < 8:
            return JsonResponse({"error": "Password should have at least 8 characters."}, status=400)

        if not re.search(r'[a-z]', password):
            return JsonResponse({"error": "Password should have at least one letter."}, status=400)

        if not re.search(r'\d', password):
            return JsonResponse({"error": "Password should contain at least one digit."}, status=400)

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return JsonResponse({"error": "Password should contain at least one special character."}, status=400)

        return view_func(request, *args, **kwargs)

    return wrapped_view


def valid_email(view_func):
    def wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format in the request body."}, status=400)

        if not email:
            return JsonResponse({"error": "Email field is empty."}, status=400)

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            return JsonResponse({"error": "Invalid email format."}, status=400)

        return view_func(request, *args, **kwargs)

    return wrapped_view
