import datetime
from http import HTTPStatus
from typing import Type, Container

from django.db import models
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Task, Tag, User


class TestAdmin(APITestCase):
    client: APIClient
    admin: User

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.admin = User.objects.create_superuser(
            "test@test.ru", email=None, password=None
        )
        cls.client = APIClient()
        cls.client.force_login(cls.admin)

    @classmethod
    def assert_forms(
        cls, model: Type[models.Model], key: int, check_actions: Container = ()
    ) -> None:
        app_label = model._meta.app_label
        model_name = model._meta.model_name

        actions = {"changelist": [], "add": [], "change": (key,)}
        if check_actions:
            actions = {key: val for key, val in actions.items() if key in check_actions}

        for action, args in actions.items():
            url = reverse(f"admin:{app_label}_{model_name}_{action}", args=args)
            response = cls.client.get(url)
            assert response.status_code == HTTPStatus.OK, response.content

    def test_user(self) -> None:
        self.assert_forms(User, self.admin.id)

    def test_tag(self) -> None:
        tag = Tag.objects.create()
        self.assert_forms(tag, tag.id)

    def test_task(self) -> None:
        task = Task.objects.create(author=self.admin, executor=self.admin)
        self.assert_forms(task, task.id)
