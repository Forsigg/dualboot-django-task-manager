from http import HTTPStatus
from typing import Union

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import User
from tests.factories import UserFactory


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user()
        cls.client = APIClient()
        token = cls.get_token()
        cls.token = {"HTTP_AUTHORIZATION": f"Bearer {token.access_token}"}

    @classmethod
    def get_token(cls):
        token = RefreshToken.for_user(cls.user)
        return token

    @staticmethod
    def create_api_user():
        user_attributes = UserFactory.build()
        return User.objects.create(
            username=user_attributes.username,
            email=user_attributes.email,
            role=user_attributes.role,
        )

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: list[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: list[Union[int, str]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data, **self.token)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list_(self, args: list[Union[int, str]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args), **self.token)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(args), **self.token)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list_filter(self, query_data: dict) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(), follow=True, data=query_data,
                                   **self.token)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(args), data=data, **self.token)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(args), **self.token)
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response

    def unauthorized_get(self, args: list[Union[str, int]]) -> dict:
        self.client.logout()
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.FORBIDDEN
        return response.data
