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
            raise Exception  # TODOOOOOOOO specific exception

        return pid.record_metadata


class RecordMetadataLiteratureManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered.filter(pid_type=PidstorePid.TYPE_LIT).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE status = R AND pid_type = lit)
        return super().get_queryset().filter(id__in=inner_query)

    def get_by_pid(self, pid_value, pid_status='R'):
        return self.model.objects.get_by_pid(pid_value, pid_type='lit', pid_status=pid_status)

    def filter_by_author_orcid(self, orcid):
        pass


class RecordMetadataAuthorsManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered.filter(pid_type=PidstorePid.TYPE_AUT).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE status = R AND pid_type = aut)
        return super().get_queryset().filter(id__in=inner_query)

    def get_by_pid(self, pid_value, pid_status='R'):
        return self.model.objects.get_by_pid(pid_value, pid_type='aut', pid_status=pid_status)

    def filter_by_literature(self, recid):
        pass


class PidstorePidRegisteredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.STATUS_REGISTERED)


class UserIdentityOrcidsManager(models.Manager):
    def filter_by_authored_record(self, pid_value):
        from .inspirehep import RecordMetadata
        record = RecordMetadata.objects.get_by_pid(pid_value)

        authors_orcids = []
        for author in record.json_model.authors:
            if author.has_orcid:
                authors_orcids.append(author.orcid)
            elif author.is_curated and author.has_recid:
                # author_record = RecordMetadata.objects.get_by_pid(author.record, 'aut')
                author_record = author.record_metadata
                if author_record.json_model.has_orcid:
                    authors_orcids.append(author_record.json_model.orcid)

        return authors_orcids
