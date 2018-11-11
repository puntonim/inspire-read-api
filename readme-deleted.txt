** DELETED RECORDS **


PID STATUS VS JSON['deleted']
=============================
Deleted record should have PidstorePid.status = 'D'.
And also RecordMetadata.json['deleted'] = True.
Unfortunately there are some inconsistency, like for RecordMetadata.id
  84f8960b-db32-4dee-b8ed-291da1f7fc3a
  4f2d48a0-e81e-49c5-8296-63af4e093f89
  981bc8cc-b7b8-48ce-917d-fd8c4b628969
But we should consider PidstorePid.status to be our oracle.

If PidstorePid.status to be our oracle then all queries like:
  >>> RecordMetadata.objects.get_by_pid()
  >>> RecordMetadata.objects.filter_by_pids()
  >>> RecordMetadata.literature_objects.*
  >>> RecordMetadata.author_objects.*
are safe because they return only registered records (PidstorePid.status = 'R').

The only queries that might return records in any state (so also deleted) is:
  >>> RecordMetadata.objects.get()
  >>> RecordMetadata.objects.all()
which should be indeed rarely used, as the ones mentioned above are more handy.


INDEX TYPE
==========
Anyway, if we need to create an index on RecordMetadata.json['deleted'], follow these guidelines.

- For booleans it's often better to use partial indexes on other columns:
https://stackoverflow.com/a/12026593/1969672
But this is not our case, as it would mean doing the proper queries (always selecting for deleted=False or NULL)

- We have 3 viable options: B-tree, Hash, GIN
https://www.postgresql.org/docs/9.6/indexes-types.html
Hash would be a great fit, but it is discouraged by the doc itself (it is safe from PostgreSQL 10 onwards).
GIN is not being used in actual queries (run an EXPLAIN and see that it is not being used).
So the only usable one is B-Tree: on a table with 1.6M records it takes only 39Mbyte.

  CREATE INDEX ix_records_metadata_json_deleted
  ON public.records_metadata
  USING btree ((json -> 'deleted'))


QUERIES
=======
Anyway, if we need to query RecordMetadata.json['deleted'], follow these guidelines.

Note: the index mentioned above is being used in all queries.

- All deleted:
  >>> RecordMetadata.objects.filter(json__deleted=True)
This query is very efficient (measured with EXPLAIN ANALYZE).
The index mentioned above improves the performance by 10x.

- All not deleted:
  >>> RecordMetadata.objects.filter(Q(json__deleted__isnull=True)|Q(json__deleted=False))
This query is NOT efficient (measured with EXPLAIN ANALYZE), despite using the index.

  >>> deleted_ids = RecordMetadata.objects.filter(json__deleted=True).values('id')
  >>> RecordMetadata.objects.exclude(id__in=deleted_ids)
This query instead is very efficient (measured with EXPLAIN ANALYZE).
