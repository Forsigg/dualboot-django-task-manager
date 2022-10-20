from http import HTTPStatus
from typing import Union

from django.urls import reverse

from rest_framework.test import APITestCase, APIClient

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
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, args: list[Union[int, str]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def retrieve(self, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(args))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def list_filter(self, args: Union[int, str], q: str) -> dict:
        self.client.force_login(self.user)
        url = self.list_url()[:-1] + f"?{q}={args}"
        response = self.client.get(url, follow=True)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def update(self, data: dict, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(args), data=data)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def delete(self, args: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(args))
        assert response.status_code == HTTPStatus.NO_CONTENT
        return response
