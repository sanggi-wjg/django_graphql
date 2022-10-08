from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin
from redis.client import Redis

NOT_ALLOWED_ABUSING_PATHS = (
    '/graphql',
    '/users'
)

NOT_ALLOWED_ABUSING_OPERATION_NAMES = (
    'create_order',
    'something_mutation'
)

redis: Redis = caches['default'].client.get_client()


class ProtectAbusingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # TODO 특정 request 요청만을 목적으로 block 처리 한다고 하면 middleware보다는 decorator로 감싸주는게 좋아봄임
        full_path = request.get_full_path()

        if request.method == "POST":
            if full_path in NOT_ALLOWED_ABUSING_PATHS:
                protector = SomethingProtector(user_id=10)
                protector.protect()


class SomethingProtector:

    def __init__(self, user_id: int = 10):
        # TODO 휘발성 정보지만 사용자 정보를 저장하고 따로 로그나 sentry나 등등 사용하고 싶다면 user_id만 저장하는 것 보다는
        # hash로 유저 객체정보를 저장하는 것도 좋아보임
        self.protect_redis_key = f"order:user:start-ordering:{user_id}"
        self.user_id = user_id

    def protect(self):
        if MyLovelyRedisRepo.get_bit_by_key_and_offset(self.protect_redis_key) == 1:
            raise Exception(
                f"@@ Protect an abusing request. (Time of rest : {MyLovelyRedisRepo.get_ttl_by_key(self.protect_redis_key)})")
        else:
            MyLovelyRedisRepo.set_bit_by_key_and_offset(self.protect_redis_key)


class MyLovelyRedisRepo:

    @classmethod
    def get_ttl_by_key(cls, key: str) -> int:
        return redis.ttl(key)

    @classmethod
    def get_bit_by_key_and_offset(cls, key: str, offset: int = 0) -> int:
        return redis.getbit(key, offset)

    @classmethod
    def set_bit_by_key_and_offset(cls, key: str, offset: int = 0, expire_second: int = 10) -> bool:
        redis.setbit(key, offset, 1)
        return redis.expire(key, expire_second)
