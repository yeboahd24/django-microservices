from django.contrib.auth.base_user import password_validation
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from user.models import CustomUser


def generate_token(user):
    """
    Generate a token for the given user.

    Parameters:
        user (User): The user for whom the token is generated.

    Returns:
        str: The generated token.

    This function generates a token for the given user by encoding a payload containing the user's ID, admin status, staff status, and expiration time. The expiration time is set to 1 hour from the current time. The payload is then encoded using the secret key and algorithm specified in the settings module.

    Example usage:
        user = User.objects.get(id=1)
        token = generate_token(user)
    """
    # Set the expiration time to 1 hour from now
    expiration_time = datetime.utcnow() + timedelta(
        hours=settings.TOKEN_EXPIRATION_TIME
    )
    payload = {
        "user_id": str(user.id),
        "exp": expiration_time,
    }
    secret_key = settings.SECRET_KEY  # Replace with your own secret key
    algorithm = settings.HASH_ALGORITHM  # Choose the desired algorithm, such as 'HS256'
    token = jwt.encode(payload, secret_key, algorithm)
    if not token:
        return {"message": "Error generating token", "status": 500}
    return token


def get_user_from_token(token):
    # from customers.models import Customers

    """
    Decode a JWT token and retrieve the user associated with it.

    Parameters:
        - token (str): The JWT token to decode and retrieve the user from.

    Returns:
        - dict or None: If the token is valid and not expired, returns a dictionary containing the user information.
          If the token is invalid or expired, returns None.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
        user_id = payload.get("user_id")
        expiration_time = payload.get("exp")
        current_time = timezone.now().timestamp()
        if expiration_time is not None and current_time > expiration_time:
            return None
        user = CustomUser.objects.filter(pk=user_id).first()
        return user
    except jwt.exceptions.ExpiredSignatureError:
        return None
    except jwt.DecodeError:
        return None
    except CustomUser.DoesNotExist:
        return None
