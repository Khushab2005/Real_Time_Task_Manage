"""
ASGI config for backend project.
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django

django.setup()

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from django.core.asgi import get_asgi_application

from  myapp.notifications import routing
from myapp import notifications
from myapp.notifications.middleware import JWTAuthMiddleware
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from myapp.chats.routing import websocket_urlpatterns
from myapp import chats
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns + chats.routing.websocket_urlpatterns   
        )
    ),
})
