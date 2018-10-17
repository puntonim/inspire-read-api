"""
Managers encapsulate queries on models.
"""
from django.db import models


class RecordMetadataManager(models.Manager):
    def get_by_pid(self, pid_value, pid_type='lit', pid_status='R'):
        from .inspirehep import PidstorePid
        try:
            pid = PidstorePid.objects.get(
                pid_value=pid_value,
                pid_type=pid_type,
                status=pid_status)
        except PidstorePid.DoesNotExist as exc:
            raise self.model.DoesNotExist from exc

        if not pid.record_metadata:
            raise self.model.DoesNotExist

        if not int(pid.record_metadata.control_number) == int(pid_value):
            import ipdb; ipdb.set_trace()
            raise Exception  # TODOOOOOOOO specific exception

        return pid.record_metadata

    def filter_by_author_orcid(self, orcid):
        pass


class UserIdentityOrcidsManager(models.Manager):
    def filter_by_authored_record(self, pid_value):
        from .inspirehep import RecordMetadata
        record = RecordMetadata.objects.get_by_pid(pid_value)

        authors_orcids = []
        for author in record.json_model.authors:
            if author.has_orcid:
                authors_orcids.append(author.orcid)
            elif author.is_curated and author.has_record:
                # author_record = RecordMetadata.objects.get_by_pid(author.record, 'aut')
                author_record = author.record_metadata
                if author_record.json_model.has_orcid:
                    authors_orcids.append(author_record.json_model.orcid)

        return authors_orcids
