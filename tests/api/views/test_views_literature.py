from django.test import TestCase

from api.models.inspirehep import RecordMetadata

from .assertions import assertRecordMetadataEqual


class TestLiteratureDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_detail_records.json',
        'tests/api/views/fixtures/test_literature_detail_pids.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/literature/'
        self.url = '{}{}/'.format(self.base_url, self.pid_value)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.literature_objects.get_by_pid(self.pid_value)
        assertRecordMetadataEqual(response.json(), rec)

    def test_get_pid_non_registered(self):
        url = '{}9999/'.format(self.base_url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_get_404(self):
        url = '{}00000/'.format(self.base_url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class TestLiteratureList(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_list_records.json',
        'tests/api/views/fixtures/test_literature_list_pids.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/literature/'

    def test_filter_by_author(self):
        aut_pid_value = 1037997
        query_params = 'author={}'.format(aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
