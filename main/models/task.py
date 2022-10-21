from django.db import models
from django.utils import timezone

from .tag import Tag
from .user import User


class Task(models.Model):
    class States(models.TextChoices):
        NEW = "new_task"
        DEVELOPMENT = "in_development"
        QA = "in_qa"
        CODE_REVIEW = "in_code_review"
        READY_FOR_RELEASE = "ready_for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    edited_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True)
    priority = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="author")
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="executor"
    )
    tags = models.ManyToManyField(Tag)
    state = models.CharField(max_length=255, default=States.NEW, choices=States.choices)

    def __str__(self):
        return f"{str(self.state).upper()} | {self.title}"
