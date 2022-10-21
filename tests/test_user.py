import factory

from main.models import User
from .base import TestViewSetBase
from .factories import UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_list(self):
        users = [factory.build(dict, FACTORY_CLASS=UserFactory) for _ in range(2)]

        user1 = self.create(users[0])
        user1_exp_resp = self.expected_details(user1, attributes=user1)
        user2 = self.create(users[1])
        user2_exp_resp = self.expected_details(user2, attributes=user2)
        default_api_user = self.retrieve(self.user.id)
        api_user_exp_resp = self.expected_details(
            default_api_user, attributes=default_api_user
        )
        list_users = self.list_()
        assert list_users == [api_user_exp_resp, user1_exp_resp, user2_exp_resp]

    def test_retrieve(self):
        user = self.create(self.user_attributes)
        user_exp_resp = self.expected_details(user, self.user_attributes)
        user_data = self.retrieve(user_exp_resp["id"])
        assert user_exp_resp == user_data

    def test_update(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        user_updated = self.update(self.user_attributes, expected_response["id"])
        updated_expected_response = self.expected_details(
            user_updated, self.user_attributes
        )
        assert user_updated == updated_expected_response

    def test_delete(self):
        user = self.create(self.user_attributes)
        users_count = User.objects.count()
        assert 2 == users_count
        self.delete(user["id"])
        users_count = User.objects.count()
        assert 1 == users_count

    def test_filter(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        username_trunc = expected_response["username"][:2]
        user_filter = self.list_filter(args=username_trunc, q="username")
        assert user_filter == [expected_response]
