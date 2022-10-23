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
        tag1 = self.create(tags[0])
        tag1_exp_resp = self.expected_details(tag1, attributes=tag1)
        tag2 = self.create(tags[1])
        tag2_exp_resp = self.expected_details(tag2, attributes=tag2)
        list_tasks = self.list_()
        assert list_tasks == [tag1_exp_resp, tag2_exp_resp]

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
        tags_count = Tag.objects.count()
        assert 1 == tags_count
        self.delete(tag["id"])
        tags_count = Tag.objects.count()
        assert 0 == tags_count