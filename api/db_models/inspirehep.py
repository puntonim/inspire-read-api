from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from . import managers
from .record_metadata_json_models.hep import HepJson
from .record_metadata_json_models.authors import AuthorJson


class PidstorePid(models.Model):
    STATUS_NEW = 'N'
    STATUS_RESERVED = 'K'
    STATUS_REGISTERED = 'R'
    STATUS_REDIRECTED = 'M'
    STATUS_DELETED = 'D'
    _STATUS_CHOICES = (
        (STATUS_NEW, 'New'),
        (STATUS_RESERVED, 'Reserved'),
        (STATUS_REGISTERED, 'Registered'),
        (STATUS_REDIRECTED, 'Redirected'),
        (STATUS_DELETED, 'Deleted'),
    )

    TYPE_LIT = 'lit'
    TYPE_AUT = 'aut'
    TYPE_JOB = 'job'
    TYPE_DAT = 'dat'
    TYPE_JOU = 'jou'
    TYPE_EXP = 'exp'
    TYPE_INS = 'ins'
    TYPE_CON = 'con'
    _TYPE_CHOICES = (
        (TYPE_LIT, 'hep.json'),
        (TYPE_AUT, 'authors.json'),
        (TYPE_JOB, 'jobs.json'),
        (TYPE_DAT, 'data.json'),
        (TYPE_JOU, 'journals.json'),
        (TYPE_EXP, 'experiments.json'),
        (TYPE_INS, 'institutions.json'),
        (TYPE_CON, 'conferences.json'),
    )
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    pid_type = models.CharField(max_length=6, choices=_TYPE_CHOICES)
    pid_value = models.CharField(max_length=255)
    pid_provider = models.CharField(max_length=8, blank=True, null=True)
    status = models.CharField(max_length=1, choices=_STATUS_CHOICES)
    object_type = models.CharField(max_length=3, blank=True, null=True)
    object_uuid = models.ForeignKey('RecordMetadata', models.DO_NOTHING, db_column='object_uuid')

    objects = models.Manager()
    registered_objects = managers.PidstorePidRegisteredManager()

    @property
    def record_metadata(self):
        return self.object_uuid

    class Meta:
        managed = False
        db_table = 'pidstore_pid'
        unique_together = (('pid_type', 'pid_value'),)


# TODO handle deleted records, json['deleted'] = True
class RecordMetadata(models.Model):
    SCHEMA_AUTHORS = 'authors.json'
    SCHEMA_CONFERENCES = 'conferences.json'
    SCHEMA_DATA = 'data.json'
    SCHEMA_EXPERIMENTS = 'experiments.json'
    SCHEMA_HEP = 'hep.json'  # Literature.
    SCHEMA_INSTITUTIONS = 'institutions.json'
    SCHEMA_JOBS = 'jobs.json'
    SCHEMA_JOURNALS = 'journals.json'
    SCHEMAS = (SCHEMA_AUTHORS, SCHEMA_CONFERENCES, SCHEMA_DATA, SCHEMA_EXPERIMENTS,
               SCHEMA_HEP, SCHEMA_INSTITUTIONS, SCHEMA_JOBS, SCHEMA_JOURNALS)

    id = models.UUIDField(primary_key=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    json = JSONField()
    version_id = models.IntegerField()

    objects = managers.RecordMetadataManager()
    literature_objects = managers.RecordMetadataLiteratureManager()
    author_objects = managers.RecordMetadataAuthorsManager()

    @property
    def control_number(self):
        return self.json.get('control_number')

    @property
    def pid(self):
        return self.pidstorepid_set.get(status=PidstorePid.STATUS_REGISTERED)

    @property
    def json_model(self):
        if self.is_hep():
            return HepJson(self.json)
        elif self.is_author():
            return AuthorJson(self.json)
        raise NotImplementedError

    @property
    def schema_type(self):
        for schema_type in self.SCHEMAS:
            if schema_type in self.json.get('$schema'):
                break
        if not schema_type:
            raise Exception('Unknown schema type: {}'.format(self.json.get('$schema')))
        if not self.pid.pid_type == SCHEMAS_PIDTYPES[schema_type]:
            raise Exception('$schema does not match the pid_type')  ###### BETTER
        return schema_type

    def is_author(self):
        return self.schema_type == self.SCHEMA_AUTHORS

    def is_conference(self):
        return self.schema_type == self.SCHEMA_CONFERENCES

    def is_data(self):
        return self.schema_type == self.SCHEMA_DATA

    def is_experiment(self):
        return self.schema_type == self.SCHEMA_EXPERIMENTS

    def is_hep(self):
        return self.schema_type == self.SCHEMA_HEP

    def is_institution(self):
        return self.schema_type == self.SCHEMA_INSTITUTIONS

    def is_job(self):
        return self.schema_type == self.SCHEMA_JOBS

    def is_journal(self):
        return self.schema_type == self.SCHEMA_JOURNALS

    class Meta:
        managed = False
        db_table = 'records_metadata'


SCHEMAS_PIDTYPES = {
    RecordMetadata.SCHEMA_AUTHORS: PidstorePid.TYPE_AUT,
    RecordMetadata.SCHEMA_CONFERENCES: PidstorePid.TYPE_CON,
    RecordMetadata.SCHEMA_DATA: PidstorePid.TYPE_DAT,
    RecordMetadata.SCHEMA_EXPERIMENTS: PidstorePid.TYPE_EXP,
    RecordMetadata.SCHEMA_HEP: PidstorePid.TYPE_LIT,
    RecordMetadata.SCHEMA_INSTITUTIONS: PidstorePid.TYPE_INS,
    RecordMetadata.SCHEMA_JOBS: PidstorePid.TYPE_JOB,
    RecordMetadata.SCHEMA_JOURNALS: PidstorePid.TYPE_JOU,
}


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    current_login_at = models.DateTimeField(blank=True, null=True)
    last_login_ip = models.CharField(max_length=50, blank=True, null=True)
    current_login_ip = models.CharField(max_length=50, blank=True, null=True)
    login_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts_user'

    @property
    def orcid_remote_account(self):
        return self.remoteaccount_set.get(client_id=settings.ORCID_APP_CONSUMER_KEY)





# class UserIdentity(models.Model):
#     id = models.CharField(primary_key=True, max_length=255)
#     method = models.CharField(max_length=255)
#     user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
#     created = models.DateTimeField()
#     updated = models.DateTimeField()
#
#     objects = models.Manager()
#     orcid_objects = managers.UserIdentityOrcidsManager()
#
#     class Meta:
#         managed = False
#         db_table = 'oauthclient_useridentity'
#         # Primary key = (id, method)
#         unique_together = (('id', 'method'), ('user', 'method'),)
#
#     @property
#     def orcid_remote_account(self):
#         return self.user.orcid_remote_account


# class RemoteAccount(models.Model):
#     id = models.CharField(primary_key=True, max_length=255)
#     user = models.ForeignKey('User', models.DO_NOTHING)
#     client_id = models.CharField(max_length=255)  # Inspire APP's ORCID.
#     extra_data = JSONField()  # It is actually a JSON (no JSONB).
#     created = models.DateTimeField()
#     updated = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'oauthclient_remoteaccount'
#         unique_together = (('user', 'client_id'),)


class RemoteToken(models.Model):
    orcid_identity = models.OneToOneField('OrcidIdentity', models.DO_NOTHING, db_column='id_remote_account', primary_key=True)
    token_type = models.CharField(max_length=40)
    # TODO decode with password
    access_token = models.BinaryField()
    secret = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'oauthclient_remotetoken'
        # Primary key: (id_remote_account, token_type)
        unique_together = (('remote_account', 'token_type'),)


class OrcidIdentity(models.Model):
    orcid_value = models.CharField(unique=True, max_length=255)
    remoteaccount_user_id = models.IntegerField(unique=True)
    useridentity_user_id = models.IntegerField(unique=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='remoteaccount_user_id')
    client_id = models.CharField(max_length=255)  # Inspire APP's ORCID.
    extra_data = JSONField()  # It is actually a JSON (no JSONB).
    id = models.IntegerField(primary_key=True, db_column='remoteaccount_id')  # Originally: remoteaccount.id.

    class Meta:
        managed = False
        db_table = 'oauthclient_orcid_identity'
        # # Primary key: (id_remote_account, token_type)
        # unique_together = (('remote_account', 'token_type'),)
