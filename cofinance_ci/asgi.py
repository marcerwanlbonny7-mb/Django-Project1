import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack
import chat.routing
from chat.jwt_auth import JWTAuthMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cofinance_ci.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': SessionMiddlewareStack(
        AuthMiddlewareStack(
            JWTAuthMiddleware(
                URLRouter(
                    chat.routing.websocket_urlpatterns
                )
            )
        )
    ),
})
