from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from myapp.accounts.models import User

class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom JWT Authentication Middleware for Django Channels.

    Purpose:
    - Extracts JWT token from WebSocket connection URL query string (?token=...).
    - Validates token using SimpleJWT.
    - If valid: attaches authenticated user to scope.
    - If invalid or missing: attaches AnonymousUser to scope.

    Works like Django's authentication middleware, but adapted for WebSocket connections.
    """

    async def __call__(self, scope, receive, send):
        # Parse query string from scope (bytes → string → dict)
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        # Extract token from ?token=... in query params (first value if multiple)
        token = query_params.get("token", [None])[0]
        print(token)
        
        

        if token:
            try:
                # Decode and validate JWT access token
                access_token = AccessToken(token)

                # Extract user_id claim from token payload
                user_id = access_token["user_id"]

                # Fetch user asynchronously from database
                user = await User.objects.aget(id=user_id)

                # Attach authenticated user to scope
                scope["user"] = user
            except Exception:
                scope["user"] = AnonymousUser()
        else:
            # No token was provided in query params
            scope["user"] = AnonymousUser()

        # Continue processing the connection with updated scope
        return await super().__call__(scope, receive, send)
