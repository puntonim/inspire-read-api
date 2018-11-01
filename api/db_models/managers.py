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

    def filter_by_pids(self, pid_values, pid_type='lit', pid_status='R'):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.objects.filter(
            pid_value__in=pid_values,
            pid_type=pid_type,
            status=pid_status).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE (pid_type = lit AND pid_value IN (769152, 1187785) AND status = R))
        return self.model.objects.filter(id__in=inner_query)


class RecordMetadataLiteratureManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered_objects.filter(pid_type=PidstorePid.TYPE_LIT).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE status = R AND pid_type = lit)
        return super().get_queryset().filter(id__in=inner_query)

    def get_by_pid(self, pid_value, pid_status='R'):
        return self.model.objects.get_by_pid(pid_value, pid_type='lit', pid_status=pid_status)

    def filter_by_pids(self, pid_values, pid_status='R'):
        return self.model.objects.filter_by_pids(pid_values, pid_type='lit', pid_status=pid_status)

    def filter_by_author(self, pid_value):
        raise NotImplementedError  # TODO


class RecordMetadataAuthorsManager(models.Manager):
    def get_queryset(self):
        from .inspirehep import PidstorePid
        inner_query = PidstorePid.registered_objects.filter(pid_type=PidstorePid.TYPE_AUT).values('object_uuid')
        # The raw query produced by Django ORM is:
        # SELECT * FROM records_metadata
        # WHERE id IN (SELECT object_uuid FROM pidstore_pid WHERE status = R AND pid_type = aut)
        return super().get_queryset().filter(id__in=inner_query)

    def get_by_pid(self, pid_value, pid_status='R'):
        return self.model.objects.get_by_pid(pid_value, pid_type='aut', pid_status=pid_status)

    def filter_by_pids(self, pid_values, pid_status='R'):
        return self.model.objects.filter_by_pids(pid_values, pid_type='aut', pid_status=pid_status)

    def filter_by_literature(self, pid_value):
        literature = self.model.literature_objects.get_by_pid(pid_value)
        recids = [aut.recid for aut in literature.json_model.authors_enclosed if aut.has_recid]
        return self.filter_by_pids(recids)


class PidstorePidRegisteredManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.STATUS_REGISTERED)


class OrcidIdentityManager(models.Manager):
    def filter_by_authored_literature(self, pid_value):
        from .inspirehep import RecordMetadata
        record = RecordMetadata.literature_objects.get_by_pid(pid_value)

        user_identities = []
        for author_enclosed in record.json_model.authors_enclosed:
            uid = None
            if author_enclosed.has_orcid_enclosed:
                # Business rule: is_curated not necessary in this case.
                uid = author_enclosed.orcid_user_identity
            elif author_enclosed.is_curated and author_enclosed.has_recid:
                author = author_enclosed.record_metadata
                if author.json_model.has_orcid_enclosed:
                    uid = author.json_model.orcid_user_identity
            if uid:
                user_identities.append(uid)

        return user_identities
