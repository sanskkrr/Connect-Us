import os
import django

# 🔥 SET SETTINGS FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectFolder.settings')

# 🔥 INITIALIZE DJANGO BEFORE ANY IMPORT
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})