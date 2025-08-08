from apps.transcribe.middleware import JWTAuthMiddleware
from channels.auth import AuthMiddlewareStack

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))