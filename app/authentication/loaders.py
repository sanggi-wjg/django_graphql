from promise import Promise
from promise.dataloader import DataLoader

from app.authentication.models import User
from app.core.colorful import cyan


class UserLoader(DataLoader):

    def batch_load_fn(self, keys):
        cyan("UserLoader!", keys)
        users = User.objects.all().in_bulk(keys)
        # users = list(users)
        return Promise.resolve([
            users.get(id=user_id) for user_id in keys
        ])
