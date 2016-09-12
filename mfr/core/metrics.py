import copy


def _merge_dicts(a, b, path=None):
    """"merges b into a

    Taken from: http://stackoverflow.com/a/7205107
    """
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge_dicts(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]

    return a


class MetricsBase():
    """Lightweight wrapper around a dict to make keeping track of metrics a little easier.

    Current functionality is limited, but may be extended later.  To do:

    * update/override method to indicate expectations of existing key

        self.metrics.add_default('some.flag', True)
        <later>
        self.metrics.override('some.flag', False)  # dies if 'some.flag' doesn't already exist

    * optional type validation?

       self.metrics.add('some.flag', True, bool())
       -or-
       self.metrics.define('some.flag', bool())
       <later>
       self.metrics.add('some.flag', 'foobar')  # dies, 'foobar' isn't a bool
    """

    def __init__(self):
        self._metrics = {}

    def key(self):
        """ID string for this object"""
        raise NotImplementedError

    def add(self, key, value):
        """add() stores the given value under the given key.  Subkeys can be specified by placing
        a dot between the parent and child keys.  e.g. 'foo.bar' will be interpreted as
        ``self._metrics['foo']['bar']``

        :param str key: the key to store ``value`` under
        :param value: the value to store, type unrestricted
        """
        self._set_dotted_key(self._metrics, key, value)

    def merge(self, record):
        """Merges a dict into the current metrics.

        :param dict record: a dict to merge with the current metrics
        """
        _merge_dicts(self._metrics, record)

    def serialize(self):
        """Return a copy of the metrics"""
        return copy.deepcopy(self._metrics)

    def manifesto(self):
        """'This is who I am and this is what I stand for!'

        Returns a dict with one entry: our key pointing to our metrics
        """
        return {self.key: self.serialize()}

    def _set_dotted_key(self, store, key, value):
        """Naive method to set nested dict values via dot-separated keys. e.g
        ``_set_dotted_keys(self._metrics, 'foo.bar', 'moo')`` is equivalent to
        ``self._metrics['foo']['bar'] = 'moo'``.  This method is neither resilient nor intelligent
        and will react with bad grace if one of the keys already exists and is not a dict key.
        """
        parts = key.split('.')
        current = store
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}

            current = current[part]
        current[parts[-1]] = value


class MetricsRecord(MetricsBase):
    """An extension to MetricsBase that carries a category and list of submetrics.  When
    serialized, will include the serialized child metrics
    """

    def __init__(self, category):
        super().__init__()
        self.category = category
        self.subrecords = []

    @property
    def key(self):
        """ID string for this record: '{category}'"""
        return self.category

    def serialize(self):
        """Returns its metrics with the metrics for each of the subrecords included under their key.
        """
        metrics = super().serialize()
        for subrecord in self.subrecords:
            metrics[subrecord.key] = subrecord.serialize()

        return metrics

    def new_subrecord(self, name):
        """Create a new MetricsSubRecord object with our category and save it to the subrecords
        list."""
        subrecord = MetricsSubRecord(self.category, name)
        self.subrecords.append(subrecord)
        return subrecord


class MetricsSubRecord(MetricsRecord):
    """An extension to MetricsRecord that carries a name in addition to a category.  Will identify
    itself as {category}_{name}.  Can create its own subrecord whose category will be this
    subrecord's ``name``.
    """

    def __init__(self, category, name):
        super().__init__(category)
        self.name = name

    @property
    def key(self):
        """ID string for this subrecord: '{category}_{name}'"""
        return '{}_{}'.format(self.category, self.name)

    def new_subrecord(self, name):
        """Creates and saves a new subrecord.  The new subrecord will have its category set to the
        parent subrecord's ``name``.  ex::

            parent = MetricsRecord('foo')
            child = parent.new_subrecord('bar')
            grandchild = child.new_subrecord('baz')

            print(parent.key)      # foo
            print(child.key)       # foo_bar
            print(grandchild.key)  # bar_baz
        """
        subrecord = MetricsSubRecord(self.name, name)
        self.subrecords.append(subrecord)
        return subrecord
