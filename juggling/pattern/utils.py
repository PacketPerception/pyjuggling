class CacheProperties(object):
    """ Will automatically cache property attributes of itself. Can clear with self._clear_cache() """
    _cache_exclude = []

    def __init__(self, *args, **kwargs):  # noqa
        self._cache = {}
        super(CacheProperties, self).__init__()

    def _clear_cache(self):
        try:
            self._cache.clear()
        except AttributeError:
            pass  # means _cache hasn't been set yet

    def __setattr__(self, key, value):
        if key != '_cache' and key in self._cache:
            del self._cache[key]
        super(CacheProperties, self).__setattr__(key, value)

    def __getattribute__(self, name, *args, **kwargs):
        exclude_attrs = super(CacheProperties, self).__getattribute__('_cache_exclude')
        if (not name.startswith('__') and
                name not in ['_cache', '_cached_attrs', '_clear_cache'] + exclude_attrs and
                isinstance(getattr(self.__class__, name, None), property)):
            cache = super(CacheProperties, self).__getattribute__('_cache')
            if name not in cache:
                cache[name] = super(CacheProperties, self).__getattribute__(name)
            return cache[name]
        return super(CacheProperties, self).__getattribute__(name, *args, **kwargs)
