from django.test import TestCase

from api.models.inspirehep import OrcidIdentity

from .assertions import assertOrcidIdentityEqual


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
