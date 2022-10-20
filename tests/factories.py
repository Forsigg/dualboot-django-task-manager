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
    created_at = factory.LazyAttribute(lambda _: datetime.datetime.now())
    edited_at = factory.LazyAttribute(lambda _: datetime.datetime.now())
    priority = factory.LazyAttribute(lambda _: faker.random_element(elements=(1, 2, 3)))
    author = factory.SubFactory(UserFactory)
    executor = factory.SubFactory(UserFactory)
    state = factory.fuzzy.FuzzyChoice(Task.States)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
