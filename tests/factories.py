import datetime
import factory.fuzzy
from .faker import faker

from main.models import User, Task, Tag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    title = factory.LazyAttribute(lambda _: faker.word())


class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.LazyAttribute(lambda _: faker.name())
    description = factory.LazyAttribute(lambda _: faker.sentence())
    created_at = factory.LazyAttribute(
        lambda _: faker.past_datetime().strftime("%Y-%m-%dT%XZ")
    )
    edited_at = factory.LazyAttribute(
        lambda _: faker.past_datetime().strftime("%Y-%m-%dT%XZ")
    )
    deadline = factory.LazyAttribute(
        lambda _: faker.past_datetime().strftime("%Y-%m-%dT%XZ")
    )
    priority = factory.LazyAttribute(lambda _: faker.random_element(elements=(1, 2, 3)))
    author = factory.LazyAttribute(lambda _: 2)
    executor = factory.LazyAttribute(lambda _: 2)
    state = factory.LazyAttribute(
        lambda _: faker.word(
            ext_word_list=[
                "new_task",
                "in_development",
                "in_qa",
                "in_code_review",
                "ready_for_release",
                "released",
                "archived",
            ]
        )
    )
