import factory

from main.models import Task
from tests.base import TestViewSetBase
from tests.factories import TaskFactory


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    task_attributes = factory.build(dict, FACTORY_CLASS=TaskFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, task)
        assert task == expected_response

    def test_list(self):
        tasks = [factory.build(dict, FACTORY_CLASS=TaskFactory) for _ in range(2)]
        expected_responses = []
        for task_dict in tasks:
            task = self.create(task_dict)
            task_expected_response = self.expected_details(task, attributes=task)
            expected_responses.append(task_expected_response)
        list_tasks = self.list_()
        assert list_tasks == expected_responses

    def test_retrieve(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, task)
        task_data = self.retrieve(expected_response["id"])
        assert expected_response == task_data

    def test_update(self):
        task = self.create(self.task_attributes)
        expected_response = self.expected_details(task, task)
        task_updated = self.update(self.task_attributes, expected_response["id"])
        updated_expected_response = self.expected_details(task_updated, task)
        assert task_updated == updated_expected_response

    def test_delete(self):
        task = self.create(self.task_attributes)
        tasks_count = Task.objects.count()
        assert 1 == tasks_count
        self.delete(task["id"])
        tasks_count = Task.objects.count()
        assert 0 == tasks_count
