"""
Managers encapsulate queries on models.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class RecordMetadataQuerySet(models.QuerySet):
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

    def filter_by_pids(self, pid_values, pid_type='lit', pid_status='R'):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.objects.filter(
            pid_value__in=pid_values,
            pid_type=pid_type,
            status=pid_status).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE (pid_type = lit AND pid_value IN (769152, 1187785) AND status = R))
        return self.filter(id__in=inner_query)


class RecordMetadataLiteratureQuerySet(RecordMetadataQuerySet):
    def get_by_pid(self, pid_value, pid_status='R'):
        return super().get_by_pid(pid_value, pid_type='lit', pid_status=pid_status)

    def filter_by_pids(self, pid_values, pid_status='R'):
        return super().filter_by_pids(pid_values, pid_type='lit', pid_status=pid_status)

    def filter_by_author(self, pid_value):
        raise NotImplementedError  # TODO


class _RecordMetadataLiteratureManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered_objects.filter(pid_type=PidstorePid.TYPE_LIT).values('object_uuid')
        return super().get_queryset().filter(id__in=inner_query)
RecordMetadataLiteratureManager = _RecordMetadataLiteratureManager.from_queryset(RecordMetadataLiteratureQuerySet)


class RecordMetadataAuthorsQuerySet(RecordMetadataQuerySet):
    def get_by_pid(self, pid_value, pid_status='R'):
        return super().get_by_pid(pid_value, pid_type='aut', pid_status=pid_status)

    def filter_by_pids(self, pid_values, pid_status='R'):
        return super().filter_by_pids(pid_values, pid_type='aut', pid_status=pid_status)

    def filter_by_literature(self, pid_value):
        try:
            literature = self.model.literature_objects.get_by_pid(pid_value)
        except ObjectDoesNotExist:
            return self.filter_by_pids([])
        recids = [aut.recid for aut in literature.json_model.authors_embedded if aut.recid]
        return self.filter_by_pids(recids)


class _RecordMetadataAuthorsManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered_objects.filter(pid_type=PidstorePid.TYPE_AUT).values('object_uuid')
        return super().get_queryset().filter(id__in=inner_query)
RecordMetadataAuthorsManager = _RecordMetadataAuthorsManager.from_queryset(RecordMetadataAuthorsQuerySet)


class PidstorePidRegisteredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.STATUS_REGISTERED)


class OrcidIdentityQuerySet(models.QuerySet):
    def filter_by_authored_literature(self, pid_value):
        from .inspirehep import RecordMetadata
        try:
            literature = RecordMetadata.literature_objects.get_by_pid(pid_value)
        except RecordMetadata.DoesNotExist:
            return self.filter(id__in=[])
        orcid_identities_ids = []
        for author_embedded in literature.json_model.authors_embedded:
            if author_embedded.orcid_identity:
                orcid_identities_ids.append(
                    author_embedded.orcid_identity.id)
        return self.filter(id__in=orcid_identities_ids)

    def get_by_author(self, pid_value):
        from .inspirehep import RecordMetadata
        author = RecordMetadata.author_objects.get_by_pid(pid_value)
        orcid_identity = getattr(author.json_model.orcid_embedded, 'orcid_identity', None)
        if not orcid_identity:
            raise self.model.DoesNotExist
        return orcid_identity

    def filter_by_allow_push(self, do_push):
        # extra_data['allow_push'] is always present and always 'true' or 'false'.
        return self.filter(extra_data__allow_push=do_push)
