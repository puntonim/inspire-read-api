from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase

from api.models.inspirehep import RecordMetadata, OrcidIdentity

from datetime import datetime
import uuid


class TestGenericFieldsInclude(TestCase):
    def test_all_existent_fields(self):

        data = {
            'countries': [
                {
                    'france': {
                        'people': [
                            {'name': 'paolo'},
                            {'name': 'frenghy'},
                            {'name': 'gigi'},
                        ]
                    },
                },
                {
                    'switzerland': {
                        'people': [
                            {'name': 'louis'},
                            {'name': 'jack'},
                        ],
                        'size': 3,
                    }
                }
            ],
        }
        data = {
            "authors": [
                {
                    "ids": 'one',
                    "value": '1',
                },
                {
                    "ids": 'two',
                    "value": '2',
                }
            ]
        }

        rec = RecordMetadata.objects.create(
            id=uuid.uuid4(),
            created=datetime.now(),
            updated=datetime.now(),
            json=data,
            version_id=0,
        )
        raw = "SELECT * FROM records_metadata"\
              "WHERE jsonb_array_elements(json->'authors') @> '{\"ids\": \"one\"}'"
        import ipdb; ipdb.set_trace()
        """
        SELECT * FROM records_metadata
        WHERE json->'authors' @> '[{"record": {"$ref": "http://labs.inspirehep.net/api/authors/1036652"}}]'::jsonb        
        """


        """
        create or replace function referenced_records(json jsonb) returns text[] as  $$
        select
            array_agg(
                references_arr->'record'->>'$ref'
            )  as result
         from
            jsonb_array_elements(json->'references') as references_arr; $$
        language sql immutable
        """



        print('END')
