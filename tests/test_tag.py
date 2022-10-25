import factory

from main.models import Tag
from tests.base import TestViewSetBase
from tests.factories import TagFactory


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = factory.build(dict, FACTORY_CLASS=TagFactory)

    @staticmethod
    def expected_details(entity: dict, attributes: dict) -> dict:
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, tag)
        assert tag == expected_response

    def test_list(self):
        tags = [factory.build(dict, FACTORY_CLASS=TagFactory) for _ in range(2)]
        expected_responses = []
        for tag_dict in tags:
            tag = self.create(tag_dict)
            tag_expected_response = self.expected_details(tag, attributes=tag)
            expected_responses.append(tag_expected_response)
        list_tasks = self.list_()
        assert list_tasks == expected_responses

    def test_retrieve(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, tag)
        tag_data = self.retrieve(expected_response["id"])
        assert expected_response == tag_data

    def test_update(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, tag)
        tag_updated = self.update(self.tag_attributes, expected_response["id"])
        updated_expected_response = self.expected_details(tag_updated, tag)
        assert tag_updated == updated_expected_response

    def test_delete(self):
        tag = self.create(self.tag_attributes)
        tags_count = len(self.list_())
        assert 1 == tags_count
        self.delete(tag["id"])
        tags_count = len(self.list_())
        assert 0 == tags_count
