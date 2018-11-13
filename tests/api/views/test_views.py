from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase

from api.models.inspirehep import RecordMetadata, OrcidIdentity


def assertRecordMetadataEqual(serialized, record_metadata_instance):
    t = TestCase()
    t.assertDictEqual(serialized['json'], record_metadata_instance.json)
    t.assertEquals(serialized['id'], str(record_metadata_instance.id))
    t.assertEquals(serialized['created'].split('Z')[0],
                   record_metadata_instance.created.isoformat().split('+')[0])
    t.assertEquals(serialized['updated'].split('Z')[0],
                   record_metadata_instance.updated.isoformat().split('+')[0])
    t.assertEquals(serialized['version_id'], record_metadata_instance.version_id)


def assertOrcidIdentityEqual(serialized, orcid_identity_instance, has_token=False):
    t = TestCase()
    t.assertEquals(serialized['id'], orcid_identity_instance.id)
    t.assertEquals(serialized['orcid_value'], str(orcid_identity_instance.orcid_value))
    t.assertEquals(serialized['useridentity_user_id'], orcid_identity_instance.useridentity_user_id)
    t.assertEquals(serialized['client_id'], str(orcid_identity_instance.client_id))
    t.assertDictEqual(serialized['extra_data'], orcid_identity_instance.extra_data)
    t.assertEquals(serialized['user'], orcid_identity_instance.user.id)
    if has_token:
        try:
            plain = orcid_identity_instance.remote_token.access_token_plain
        except ObjectDoesNotExist:
            plain = None
        t.assertEquals(serialized['token'], plain)


class TestGenericFieldsInclude(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_literature_detail_records.json',
        'tests/api/views/fixtures/test_literature_detail_pids.json',
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


class TestAuthorDetail(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_author_detail_records.json',
        'tests/api/views/fixtures/test_author_detail_pids.json',
    )

    def setUp(self, **kwargs):
        self.pid_value = 7777
        self.base_url = '/api/authors/{}/'.format(self.pid_value)

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        rec = RecordMetadata.author_objects.get_by_pid(self.pid_value)
        assertRecordMetadataEqual(response.json(), rec)

    def test_get_pid_not_registered(self):
        base_url = '/api/authors/9999/'
        response = self.client.get(base_url)
        self.assertEquals(response.status_code, 404)

    def test_get_404(self):
        response = self.client.get('/api/literature/00000/')
        self.assertEquals(response.status_code, 404)


class TestGenericPagination(TestCase):
    # TODO
    # test that more than 100 results make up 2 pages with proper next param
    pass


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


class TestOrcidIdentitiesList(TestCase):
    fixtures = (
        'tests/api/views/fixtures/test_orcid_identities_list_records_lit.json',
        'tests/api/views/fixtures/test_orcid_identities_list_records_aut.json',
        'tests/api/views/fixtures/test_orcid_identities_list_pids.json',
        'tests/api/views/fixtures/test_orcid_identities_list_orcids.json',
        'tests/api/views/fixtures/test_orcid_identities_list_users.json',
        'tests/api/views/fixtures/test_orcid_identities_list_tokens.json',
    )

    def setUp(self, **kwargs):
        self.base_url = '/api/identities/orcid/'

    def test_get(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 6)
        orcids = OrcidIdentity.objects.all().order_by('id')
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

    def test_filter_by_literature(self):
        lit_pid_value = 6666
        query_params = 'literature={}'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 2)
        orcids = OrcidIdentity.objects.filter(orcid_value__in=[
            '0000-0001-5498-9174', '0000-0002-4133-1234'])
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

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

    def test_filter_by_push_true(self):
        query_params = 'push=true'
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 4)
        orcids = OrcidIdentity.objects.filter(extra_data__allow_push=True)
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

    def test_filter_by_push_false(self):
        query_params = 'push=false'
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 2)
        orcids = OrcidIdentity.objects.filter(extra_data__allow_push=False)
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

    def test_filter_by_push_and_literature(self):
        lit_pid_value = 6666
        query_params = 'literature={}&push=true'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
        orcids = OrcidIdentity.objects\
            .filter(orcid_value__in=['0000-0001-5498-9174', '0000-0002-4133-1234']) \
            .filter(extra_data__allow_push=True)
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

    def test_filter_by_push_and_literature_nonexistent(self):
        lit_pid_value = 1
        query_params = 'literature={}&push=true'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_push_and_literature_pid_not_registered(self):
        lit_pid_value = 6668
        query_params = 'literature={}&push=true'.format(lit_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author(self):
        aut_pid_value = 7777
        query_params = 'author={}'.format(aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
        orcid = OrcidIdentity.objects.get(pk=1)
        assertOrcidIdentityEqual(response.json()['results'][0], orcid)

    def test_filter_by_author_nonexistent(self):
        aut_pid_value = 1
        query_params = 'author={}'.format(aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author_pid_not_registered(self):
        aut_pid_value = 7782
        query_params = 'author={}'.format(aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author_and_push_and_literature(self):
        lit_pid_value = 6666
        aut_pid_value = 7777
        query_params = 'literature={}&author={}&push=false'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
        orcids = OrcidIdentity.objects\
            .filter(orcid_value__in=['0000-0001-5498-9174', '0000-0002-4133-1234']) \
            .filter(extra_data__allow_push=False)
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid)

    def test_filter_by_author_nonexistent_and_push_and_literature(self):
        lit_pid_value = 6666
        aut_pid_value = 1
        query_params = 'literature={}&author={}&push=false'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author_pid_not_registered_and_push_and_literature(self):
        lit_pid_value = 6666
        aut_pid_value = 7782
        query_params = 'literature={}&author={}&push=false'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author_and_push_and_literature_nonexistent(self):
        lit_pid_value = 1
        aut_pid_value = 7777
        query_params = 'literature={}&author={}&push=false'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_filter_by_author_and_push_and_literature_pid_not_registered(self):
        lit_pid_value = 6668
        aut_pid_value = 7777
        query_params = 'literature={}&author={}&push=false'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 0)
        self.assertListEqual(response.json()['results'], [])

    def test_get_with_tokens(self):
        query_params = 'fields-extra=token'
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 6)
        orcids = OrcidIdentity.objects.all().order_by('id')
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid, has_token=True)

    def test_filter_by_author_and_push_and_literature_with_tokens(self):
        lit_pid_value = 6666
        aut_pid_value = 7777
        query_params = 'literature={}&author={}&push=false&fields-extra=token'.format(
            lit_pid_value, aut_pid_value)
        response = self.client.get('{}?{}'.format(self.base_url, query_params))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()['count'], 1)
        orcids = OrcidIdentity.objects\
            .filter(orcid_value__in=['0000-0001-5498-9174', '0000-0002-4133-1234']) \
            .filter(extra_data__allow_push=False)
        for i, orcid in enumerate(orcids):
            assertOrcidIdentityEqual(response.json()['results'][i], orcid, has_token=True)
