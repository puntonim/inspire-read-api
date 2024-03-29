import re


SPLIT_KEY_PATTERN = re.compile(r'\.|\[')


def smartget(data, key, default=None):
    # Inspired by: https://github.com/inspirehep/inspire-utils/blob/master/inspire_utils/record.py#L31
    def getitem(k, v, default):
        # v is a dictionary.
        if isinstance(v, dict):
            return v[k]
        # v is probably a list.
        elif ']' in k:
            k = k[:-1].replace('n', '-1')  # Get the last with either [-1] or [n].
            # Work around for list indexes and slices.
            try:
                return v[int(k)]
            except IndexError:
                return default
            except ValueError:
                return v[slice(*map(
                    lambda x: int(x.strip()) if x.strip() else None,
                    k.split(':')
                ))]
        else:
            tmp = []
            for inner_v in v:
                try:
                    tmp.append(getitem(k, inner_v, default))
                except KeyError:
                    continue
            return tmp

    # Try regular Python first.
    try:
        key = int(key)
    except ValueError:
        pass
    try:
        return data[key]
    except (KeyError, TypeError):
        pass

    keys = SPLIT_KEY_PATTERN.split(key)
    value = data
    for k in keys:
        try:
            value = getitem(k, value, default)
        except KeyError:
            return default
        except TypeError:
            if k and value is None:
                # value is currently None and we are trying to get a key.
                return default
            raise
    return value

# TODO consider replace everything with JQ

def smartget_if(data, key, condition, default=None):
    unfiltered_result = smartget(data, key, default)
    if isinstance(unfiltered_result, list):
        return [_ for _ in unfiltered_result if condition(_)]

    return unfiltered_result if condition(unfiltered_result) else None


class SmartgetDictMixin(dict):
    def smartget(self, key, default=None):
        return smartget(self, key, default)

    def smartget_if(self, key, condition, default=None):
        return smartget_if(self, key, condition, default)
