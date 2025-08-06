import redis
from rest_framework.response import Response
from rest_framework.exceptions import Throttled

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Throttle view
def rate_limited(max_requests:int,time_window : int):
    def decorator(view_func):
        def wrapper(self , request, *args, **kwargs):
            client_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            endpoint = request.path
            redis_key = f"{client_id}:{endpoint}"
            current_requests = redis_client.get(redis_key)
            if current_requests is None:
                redis_client.set(redis_key, 1,ex=time_window)
            elif int(current_requests) < max_requests:
                redis_client.incr(redis_key)
            else:
                raise Throttled(detail="You have exceeded the rate limit.")
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator
    

        
        