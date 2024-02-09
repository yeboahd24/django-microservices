import jwt
import time
import requests
from django.http import JsonResponse
from django.conf import settings


# class JWTTokenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Get the token from the Authorization header
#         token = request.headers.get("Authorization", None)

#         if not token:
#             return JsonResponse(
#                 {"error": "Authorization header is missing"}, status=401
#             )

#         try:
#             # Remove 'Bearer ' prefix from token
#             token = token.split()[1]
#             # Decode the token
#             decoded_token = jwt.decode(
#                 token, settings.JWT_DECRYPT_KEY, algorithms=["HS256"]
#             )
#             # Validate the token
#             if not self.validate_token(decoded_token):
#                 return JsonResponse({"error": "Invalid token"}, status=401)
#             # Attach user information to request object
#             request.user = self.authenticate_user(token)
#             if not request.user:
#                 return JsonResponse({"error": "User not authenticated"}, status=401)
#         except jwt.ExpiredSignatureError:
#             return JsonResponse({"error": "Token is expired"}, status=401)
#         except jwt.InvalidTokenError:
#             return JsonResponse({"error": "Invalid token"}, status=401)

#         response = self.get_response(request)
#         return response

#     def validate_token(self, decoded_token):
#         # Check expiration
#         if "exp" in decoded_token:
#             exp_timestamp = decoded_token["exp"]
#             current_timestamp = time.time()
#             if exp_timestamp < current_timestamp:
#                 return False
#         # Perform additional validation steps as needed
#         # For example: check issuer, audience, etc.
#         return True

#     def authenticate_user(self, token):
#         headers = {"Authorization": token}

#         authentication_url = (
#             settings.AUTHENTICATION_MICROSERVICE_URL + "token-verification/"
#         )
#         data = {"token": token}
#         response = requests.post(authentication_url, json=data, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return None


class JWTTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the token from the Authorization header
        token = request.headers.get("Authorization", None)
        print(token)

        if not token or len(token.split()) < 2:
            return JsonResponse({"error": "Invalid Authorization header"}, status=401)

        try:
            # Remove 'Bearer ' prefix from token
            token = token.split()[1]
            # Decode the token
            decoded_token = jwt.decode(
                token, settings.JWT_DECRYPT_KEY, algorithms=["HS256"]
            )
            # Validate the token
            if not self.validate_token(decoded_token):
                return JsonResponse({"error": "Invalid token"}, status=401)
            # Attach user information to request object
            request.user_id = self.authenticate_user(token)
            if not request.user_id:
                return JsonResponse({"error": "User not authenticated"}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token is expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)

        response = self.get_response(request)
        return response

    def validate_token(self, decoded_token):
        # Check expiration
        if "exp" in decoded_token:
            exp_timestamp = decoded_token["exp"]
            current_timestamp = time.time()
            if exp_timestamp < current_timestamp:
                return False
        # Perform additional validation steps as needed
        # For example: check issuer, audience, etc.
        return True

    def authenticate_user(self, token):
        try:
            # Remove 'Bearer ' prefix from token
            # token = token.split()
            # Decode the token
            decoded_token = jwt.decode(
                token, settings.JWT_DECRYPT_KEY, algorithms=["HS256"]
            )
            user_id = decoded_token.get("user_id")

            authentication_url = (
                settings.AUTHENTICATION_MICROSERVICE_URL + "token-verification/"
            )
            data = {"token": token}
            headers = {"Authorization": token}
            response = requests.post(authentication_url, json=data, headers=headers)

            if response.status_code == 200:
                return user_id
            else:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
