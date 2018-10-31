from django.contrib import admin
from django.contrib.postgres.fields import JSONField

from jsoneditor.forms import JSONEditor

from .db_models import inspirehep


class RecordMetadataAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditor}
    }


# TODO add search and links from model to model
# TODO read only forms

admin.site.register(inspirehep.RecordMetadata, RecordMetadataAdmin)
admin.site.register(inspirehep.PidstorePid)
admin.site.register(inspirehep.User)
admin.site.register(inspirehep.OrcidIdentity)
admin.site.register(inspirehep.RemoteToken)
