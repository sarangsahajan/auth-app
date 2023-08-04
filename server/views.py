import json
import bcrypt
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .decorators import authenticate_token
from django.conf import settings


# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["faceswap"]


@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Check if user already exists
            if db.users.find_one({"email": email}):
                return JsonResponse({"error": "User already exists."}, status=400)

            # Hash the password
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())

            # Create the user
            user = {
                "email": email,
                # Decode the bytes to store as string
                "password": hashed_password.decode('utf-8'),
            }
            db.users.insert_one(user)

            # Generate JWT token
            jwt_token = jwt.encode(
                {"email": email}, settings.SECRET_KEY, algorithm="HS256")

            return JsonResponse({"message": "User created successfully.", "token": jwt_token})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Check if user exists
            user = db.users.find_one({"email": email})
            if not user:
                return JsonResponse({"error": "User does not exist."}, status=404)

            # Verify password
            hashed_password = user.get('password').encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                # Password is correct, generate JWT token
                jwt_token = jwt.encode(
                    {"email": email}, settings.SECRET_KEY, algorithm="HS256")
                return JsonResponse({"message": "Login successful.", "token": jwt_token})
            else:
                return JsonResponse({"error": "Invalid credentials."}, status=401)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
@authenticate_token
def protected_view(request):
    user = request.user
    # Convert ObjectId to string for serialization
    user['_id'] = str(user['_id'])
    return JsonResponse({"user": user})
