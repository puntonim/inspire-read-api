import sys
import warnings


# Ignore warnings like:
# ...db/models/fields/__init__.py:1421: RuntimeWarning: DateTimeField
# RecordMetadata.created received a naive datetime (2010-01-12 00:00:00) while
# time zone support is active.
if not sys.warnoptions:
    msg = r'DateTimeField .* received a naive datetime.*'
    warnings.filterwarnings('ignore', message=msg, module='.*models.*')
