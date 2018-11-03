from django.test import TestCase

from api.models.inspirehep import RecordMetadata


class TestLiteratureDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/record_metadata_hep.json',
        'tests/api/views/fixtures/pidstore_pid.json',
    )

    def setUp(self, **kwargs):
        self.recid = 7777
        self.base_url = '/api/literature/{}/'.format(self.recid)

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.literature_objects.get_by_pid(self.recid)
        self.assertDictEqual(response.json()['json'], rec.json)

    def test_get_404(self):
        response = self.client.get('/api/literature/00000/')
        self.assertEquals(response.status_code, 404)

    def test_get_fields_include(self):
        fields = ['dois', 'authors', 'titles', 'abstracts']
        query_params = 'fields-include={}'.format(','.join(fields))
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.literature_objects.get_by_pid(self.recid)
        data = {}
        for field in fields:
            data[field] = rec.json[field]
        self.assertDictEqual(response.json()['json'], data)
