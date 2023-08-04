from django.http import JsonResponse
import jwt
from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017/")
db = client["faceswap"]


def authenticate_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', None)

        if not auth_header:
            return JsonResponse({"error": "Authorization header missing."}, status=401)

        try:
            _, token = auth_header.split(' ')
            payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
            print(payload)
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
