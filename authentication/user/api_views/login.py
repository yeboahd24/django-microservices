from django.contrib.auth import authenticate
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from user.utils import (
    generate_token,
)
from user.models import CustomUser


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        """
        Handles the POST request for the API endpoint.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            JsonResponse: The JSON response containing the result of the request.

        Raises:
            None.
        """

        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

        except json.JSONDecodeError:
            return JsonResponse(
                {
                    "message": "JSONDecodeError, You might have forgotten to provide your data / field(s) in json format.",
                    "status": 400,
                },
                status=400,
            )
        # check if user does not exist
        if not CustomUser.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "User does not exist", "status": 400}, status=400
            )

        user = authenticate(request, email=email, password=password)

        if not user:
            return JsonResponse(
                {"message": "Invalid credentials", "status": 401}, status=401
            )

        if not user.is_active:
            return JsonResponse(
                {"message": "User is not active", "status": 401}, status=401
            )

        token = generate_token(user)
        # user = CustomUser.objects.get(email=user.email)

        message = f"Login completed."
        response_data = {
            "message": message,
            "status": 200,
            "data": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "token": token,
            },
        }
        return JsonResponse(response_data, content_type="application/json")
