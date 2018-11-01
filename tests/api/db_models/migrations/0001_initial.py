# Generated by Django 2.1.2 on 2018-11-01 16:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrcidIdentity',
            fields=[
                ('orcid_value', models.CharField(max_length=255, unique=True)),
                ('useridentity_user_id', models.IntegerField(unique=True)),
                ('client_id', models.CharField(max_length=255)),
                ('extra_data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('id', models.IntegerField(db_column='remoteaccount_id', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'oauthclient_orcid_identity',
            },
        ),
        migrations.CreateModel(
            name='RecordMetadata',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('json', django.contrib.postgres.fields.jsonb.JSONField()),
                ('version_id', models.IntegerField()),
            ],
            options={
                'db_table': 'records_metadata',
            },
        ),
        migrations.CreateModel(
            name='PidstorePid',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('pid_type', models.CharField(choices=[('lit', 'hep.json'), ('aut', 'authors.json'), ('job', 'jobs.json'), ('dat', 'data.json'), ('jou', 'journals.json'), ('exp', 'experiments.json'), ('ins', 'institutions.json'), ('con', 'conferences.json')], max_length=6)),
                ('pid_value', models.CharField(max_length=255)),
                ('pid_provider', models.CharField(blank=True, max_length=8, null=True)),
                ('status', models.CharField(choices=[('N', 'New'), ('K', 'Reserved'), ('R', 'Registered'), ('M', 'Redirected'), ('D', 'Deleted')], max_length=1)),
                ('object_type', models.CharField(blank=True, max_length=3, null=True)),
                ('object_uuid', models.ForeignKey(on_delete=models.DO_NOTHING, to='api.RecordMetadata', db_column='object_uuid')),
            ],
            options={
                'db_table': 'pidstore_pid',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('active', models.BooleanField(blank=True, null=True)),
                ('confirmed_at', models.DateTimeField(blank=True, null=True)),
                ('last_login_at', models.DateTimeField(blank=True, null=True)),
                ('current_login_at', models.DateTimeField(blank=True, null=True)),
                ('last_login_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('current_login_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('login_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'accounts_user',
            },
        ),
        migrations.CreateModel(
            name='RemoteToken',
            fields=[
                ('orcid_identity', models.OneToOneField(db_column='id_remote_account', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='api.OrcidIdentity')),
                ('token_type', models.CharField(max_length=40)),
                ('access_token', models.BinaryField()),
                ('secret', models.TextField()),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField()),
            ],
            options={
                'db_table': 'oauthclient_remotetoken',
            },
        ),
    ]