RECORDS GRANDI
==============
PROD DUMP DEL 2018.04
---------------------
Il record col json piu grande (2.5 MB) e':
select id, length(json::text)
from public.records_metadata
where length(json::text) = (
	select max(length(json::text)) from public.records_metadata
) group by id;

       d1be3315-9567-4df7-9989-a5355fc66e18
uuid = d1be3315-9567-4df7-9989-a5355fc66e18
length = 2537584  (2.5 MB)
json['control_number'] = 335153
https://labs.inspirehep.net/api/literature/335153

PROD IL 2018.10.14
------------------
Still the same as in the dump:
uuid = d1be3315-9567-4df7-9989-a5355fc66e18
length = 2526662
json['control_number'] = 335153
https://labs.inspirehep.net/api/literature/335153

Lit + grande: 335153
Lit small: 335152 w/ 3 authors Dugan(1011268), Mitchell(1008115), Chivukula(1013679)
Auth: 1607170

Un autore grande (ATLAS) su orcid:
https://orcid.org/0000-0002-0400-7555


SELECT *, SELECT FEW
====================
Per fare una query con SELECT id FROM:
MyModel.objects.get().values('id')  # ritorna dict
MyModel.objects.get().values_list('id', named=True)  # ritorna named tuple

Per fare la stessa cosa dentro un record json:
https://stackoverflow.com/a/45369944/1969672



MULTIPLE AND LEGACY DATABASE
============================
https://docs.djangoproject.com/en/2.1/topics/db/multi-db/#database-routers
https://docs.djangoproject.com/en/2.1/howto/legacy-databases/


RECORD, AUTORI, TOKENS
======================
- Senza token:
Record 250460
Has author 994322 (2nd author)
With orcid 0000-0002-3132-4417
Senza UserIdentity e token

- Con token:
Record 1126991
Has author 1039812 (1st author)
With orcid 0000-0001-9835-7128
Con UserIdentity e User 52921


OPERAZIONI SU DB ISNPIRE
=========================
- Garantire permessi in lettura:
# no need -- GRANT CONNECT ON DATABASE "inspirehep-prod-dump" TO "inspire-read-api";
# no need -- GRANT USAGE ON SCHEMA public TO "inspire-read-api";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "inspire-read-api";

- RemoteAccount.extra_data to JSONB:
ALTER TABLE public.oauthclient_remoteaccount
    ALTER COLUMN extra_data SET DATA TYPE jsonb;

- Creazione della view:
Postgresql 9.6.2
https://www.postgresql.org/docs/9.6/static/sql-createview.html

CREATE VIEW oauthclient_orcid_identity
AS
    SELECT oauthclient_useridentity.id as orcid_value,
           oauthclient_remoteaccount.user_id as remoteaccount_user_id,
           oauthclient_useridentity.id_user as useridentity_user_id,
           oauthclient_remoteaccount.client_id,
           oauthclient_remoteaccount.extra_data,
           oauthclient_remoteaccount.id as remoteaccount_id
    FROM public.oauthclient_useridentity
    FULL OUTER JOIN public.oauthclient_remoteaccount
    ON oauthclient_useridentity.id_user = oauthclient_remoteaccount.user_id
    WHERE oauthclient_useridentity.method = 'orcid'
    OR oauthclient_useridentity.method is NULL;

Nota che alcuni hanno dati inconsistenti:
remoteaccount_id=5888 non ha useridentity e non ha token
ce ne sono 9 cosi

Poi aggiungere ancora i permessi di select:
GRANT SELECT ON ALL TABLES IN SCHEMA public TO "inspire-read-api";

