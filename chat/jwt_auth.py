from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    try:
        access = AccessToken(token)
        user = User.objects.get(id=access['user_id'])
        return user
    except (TokenError, User.DoesNotExist, KeyError):
        return None

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query = parse_qs(scope['query_string'].decode())
        token = query.get('token', [None])[0]

        if token:
            user = await get_user_from_token(token)
            if user:
                scope['user'] = user

        return await self.inner(scope, receive, send)
