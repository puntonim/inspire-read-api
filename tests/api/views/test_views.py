from django.test import TestCase

from api.models.inspirehep import RecordMetadata


class TestGenericFieldsInclude(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_detail_record.json',
        'tests/api/views/fixtures/test_literature_detail_pid.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/literature/{}/'.format(self.pid_value)

    def _get_filtered_json_data(self, fields_include):
        record = RecordMetadata.literature_objects.get_by_pid(self.pid_value)
        record_json_keys = list(record.json.keys())
        if not fields_include:
            return record.json
        for key in record_json_keys:
            if key not in fields_include:
                del record.json[key]
        return record.json

    def test_all_existent_fields(self):
        fields = ['dois', 'authors', 'titles', 'abstracts']
        query_params = 'fields-include={}'.format(','.join(fields))
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.json()['json'], self._get_filtered_json_data(fields))

    def test_empty(self):
        query_params = 'fields-include='
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.json()['json'], self._get_filtered_json_data(None))

    def test_all_nonexistent_fields(self):
        fields = ['doesnotexist1', 'doesnotexist2']
        query_params = 'fields-include={}'.format(','.join(fields))
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.json()['json'], self._get_filtered_json_data(fields))

    def test_mix_existent_and_nonexistent_fields(self):
        fields = ['doesnotexist1', 'dois', 'doesnotexist2', 'authors']
        query_params = 'fields-include={}'.format(','.join(fields))
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.json()['json'], self._get_filtered_json_data(fields))


class TestLiteratureDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_detail_record.json',
        'tests/api/views/fixtures/test_literature_detail_pid.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/literature/{}/'.format(self.pid_value)

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.literature_objects.get_by_pid(self.pid_value)
        self.assertDictEqual(response.json()['json'], rec.json)

    def test_get_404(self):
        response = self.client.get('/api/literature/00000/')
        self.assertEquals(response.status_code, 404)


class TestAuthorDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_author_detail_record.json',
        'tests/api/views/fixtures/test_author_detail_pid.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/authors/{}/'.format(self.pid_value)

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.author_objects.get_by_pid(self.pid_value)
        self.assertDictEqual(response.json()['json'], rec.json)

    def test_get_404(self):
        response = self.client.get('/api/literature/00000/')
        self.assertEquals(response.status_code, 404)
