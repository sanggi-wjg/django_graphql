from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin
from redis.client import Redis

redis: Redis = caches['default'].client.get_client()
NOT_ALLOWED_ABUSING_PATHS = (
    '/graphql', '/users'
)

NOT_ALLOWED_ABUSING_OPERATION_NAMES = (
    'create_order'
)


class ProtectAbusingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        full_path = request.get_full_path()

        if request.method == "POST":
            if full_path in NOT_ALLOWED_ABUSING_PATHS:
                something_redis = SomethingProtector(user_id=10)
                something_redis.protect()


class SomethingProtector:

    def __init__(self, user_id: int = 10):
        self.something_key = f"create-order:user:{user_id}"
        self.user_id = user_id

    def protect(self):
        if self.get_bit_by_user_id() == 1:
            raise Exception(f"@@ ERROR : protect_abusing. rest_time : {self.get_ttl_by_user_id()}")
        else:
            self.set_bit_by_user_id()

    def get_ttl_by_user_id(self) -> int:
        return redis.ttl(self.something_key)

    def get_bit_by_user_id(self) -> int:
        return redis.getbit(self.something_key, 0)

    def set_bit_by_user_id(self, expire_second: int = 10) -> bool:
        redis.setbit(self.something_key, 0, 1)
        return redis.expire(self.something_key, expire_second)
