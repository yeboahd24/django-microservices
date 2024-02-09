from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from user.models import CustomUser
from django.conf import settings
from django.db.utils import IntegrityError
import json
from django.core.exceptions import ValidationError


@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        password = data.get("password")

        # Validate required parameters
        if any([not email, not password, not first_name, not last_name]):
            return JsonResponse(
                {
                    "message": "Missing parameters in request",
                    "status": 400,
                },
                status=400,
            )

        # Get or create the user
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        if not created:
            return JsonResponse(
                {"message": "User not created / already exists", "status": 400},
                status=400,
            )

        # Set user password
        user.set_password(password)
        user.save()
        message = "Registrations completed."

        response_data = {
            "message": message,
            "status": 200,
            "data": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        }

        return JsonResponse(response_data, content_type="application/json")

    except json.JSONDecodeError:
        return JsonResponse(
            {
                "message": "JSONDecodeError, You might have forgotten to provide your data/field(s) in JSON format.",
                "status": 400,
            },
            status=400,
        )
    except ValidationError as e:
        return JsonResponse(
            {"message": str(e), "status": 400},
            status=400,
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An error occurred: " + str(e), "status": 500},
            status=500,
        )
