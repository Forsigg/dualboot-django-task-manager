import django_filters
from rest_framework import viewsets

from main.models import User, Task, Tag
from main.serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(field_name="state", lookup_expr="icontains")
    author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")
    executor = django_filters.CharFilter(field_name="executor", lookup_expr="icontains")
    tags = django_filters.MultipleChoiceFilter(field_name="tags", lookup_expr="in")

    class Meta:
        model = Task
        fields = ("state", "author", "executor", "tags")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related("tags").order_by("id")
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
