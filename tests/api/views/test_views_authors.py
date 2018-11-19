from django.test import TestCase

from api.models.inspirehep import RecordMetadata

from .assertions import assertRecordMetadataEqual


class TestAuthorDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_author_detail_records.json',
        'tests/api/views/fixtures/test_author_detail_pids.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/authors/'
        self.url = '{}{}/'.format(self.base_url, self.pid_value)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.author_objects.get_by_pid(self.pid_value)
        assertRecordMetadataEqual(response.json(), rec)

    def test_get_pid_not_registered(self):
        url = '{}9999/'.format(self.base_url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_get_404(self):
        url = '{}00000/'.format(self.base_url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)


class TestAuthorsList(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_authors_list_records_lit.json',
        'tests/api/views/fixtures/test_authors_list_records_aut.json',
        'tests/api/views/fixtures/test_authors_list_pids.json',
    )

    def setUp(self, **kwargs):
        self.base_url = '/api/authors/'

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 2)
        recs = RecordMetadata.author_objects.all().order_by('id')
        for i, rec in enumerate(recs):
            assertRecordMetadataEqual(response.json()['results'][i], rec)

    def test_filter_by_literature(self):
        lit_pid_value = 6666
        query_params = 'literature={}'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 2)
        recs = RecordMetadata.author_objects.filter_by_pids([7777, 7778]).order_by('id')
        for i, rec in enumerate(recs):
            assertRecordMetadataEqual(response.json()['results'][i], rec)

    def test_filter_by_literature_nonexistent(self):
        lit_pid_value = 1
        query_params = 'literature={}'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_literature_pid_not_registered(self):
        lit_pid_value = 6668
        query_params = 'literature={}'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_orcid(self):
        orcid_value = '0000-0001-5498-9174'
        query_params = 'orcid={}'.format(orcid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
        aut = RecordMetadata.author_objects.get_by_pid(7777)
        assertRecordMetadataEqual(response.json()['results'][0], aut)

    def test_filter_by_orcid_nonexistent(self):
        orcid_value = '0000-0001-5498-XXXX'
        query_params = 'orcid={}'.format(orcid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_orcid_pid_not_registered(self):
        orcid_value = '0000-0001-5498-YYYY'
        query_params = 'orcid={}'.format(orcid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])
