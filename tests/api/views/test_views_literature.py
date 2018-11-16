from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase

from api.models.inspirehep import RecordMetadata, OrcidIdentity

from .assertions import assertRecordMetadataEqual


class TestLiteratureDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_detail_records.json',
        'tests/api/views/fixtures/test_literature_detail_pids.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/literature/{}/'.format(self.pid_value)

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.literature_objects.get_by_pid(self.pid_value)
        assertRecordMetadataEqual(response.json(), rec)

    def test_get_pid_non_registered(self):
        base_url = '/api/literature/9999/'
        response = self.client.get(base_url)
        self.assertEquals(response.status_code, 404)

    def test_get_404(self):
        response = self.client.get('/api/literature/00000/')
        self.assertEquals(response.status_code, 404)
