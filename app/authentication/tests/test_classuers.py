import pytest

from app.authentication.models import User
from app.core.colorful import red, yellow


# pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestCaseUsers:
    pytestmark = pytest.mark.django_db

    @classmethod
    def setup_class(cls):
        red("SETUP CLASS")

    @classmethod
    def teardown_class(cls):
        red("TEAR DOWN CLASS")

    def setup_method(self, method):
        yellow("\nSETUP METHOD")
        User.objects.create_user("test@dev.com", "test@dev.com", "123")

    def teardown_method(self, method):
        yellow("TEAR DOWN METHOD\n")

    def test_0001(self):
        users = User.objects.all()
        print(users)

    def test_0002(self, create_random_users):
        users = User.objects.all()
        print(users)

    def test_0003(self):
        users = User.objects.all()
        print(users)
