from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase


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