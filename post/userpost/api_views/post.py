from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from userpost.models import Post
from django.conf import settings
from django.db.utils import IntegrityError
import json
from django.core.exceptions import ValidationError


@csrf_exempt
@require_POST
def post(request):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        content = data.get("content")

        # Validate required parameters
        if any([not title, not content]):
            return JsonResponse(
                {
                    "message": "Missing parameters in request",
                    "status": 400,
                },
                status=400,
            )

        # Get or create the user
        post = Post.objects.create(
            title=title, content=content, author_id=request.user_id
        )

        post.save()
        message = "Post completed."

        response_data = {
            "message": message,
            "status": 200,
            "data": {
                "title": post.title,
                "content": post.content,
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
