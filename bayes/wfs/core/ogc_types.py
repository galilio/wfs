import abc

class ServiceIdentification(metaclass = abc.ABCMeta):
    __slots__ = 'service_type', 'service_type_version', 'profile', 'description', 'fees', 'access_constraints'

    class Description(object):
        def __init__(self, title, abstract, keywords = []):
            super().__init__()

            self.title = title
            self.abstract = abstract
            self.keywords = keywords

    def __init__(self):
        self.service_type = 'WFS'
        self.service_type_version = '2.0.0'

class ServiceProvider(metaclass = abc.ABCMeta):
    __slots__ = 'provider_name', 'provider_site', 'service_contact'

    class Contact(object):
        def __init__(self, name, tel):
            super().__init__()
            self.name = name
            self.tel = tel

    def __init__(self):
        pass

class OperationsMetadata(metaclass = abc.ABCMeta):
    __slots__ = 'domains', 'operations'
    def __init__(self, domains):
        super().__init__()
        self.domains = domains
        self.operations = []
    
    class Operation(object):
        __slots__ = 'name', 'request_method', 'link', 'about', 'domains'

class ServiceMeta(metaclass = abc.ABCMeta):
    __slots__ = 'service_identification', 'version', 'update_sequence', 'service_provider', 'operations_metadata', 'contents'

    def __init__(self, version, update_sequence):
        super().__init__()

        self.version = version
        self.update_sequence = update_sequence

class FeatureType(metaclass = abc.ABCMeta):
    __slots__ = 'name', 'properties', 'abstract'
    def __init__(self, name, abstract = None, properties = []):
        super().__init__()
        self.name = name
        self.properties = properties
        self.abstract = abstract

    def __str__(self):
        return f'{self.name}-{self.properties}'

    class Property(metaclass = abc.ABCMeta):
        __slots__ = 'nullable', 'pk', 'dtype', 'max_length', 'min_length', 'name'

        def __init__(self, name, dtype, nullable = True, pk = False, max_length = 0, min_length = 0):
            super().__init__()
            self.name = name
            self.dtype = dtype
            self.nullable = nullable
            self.pk = pk
            self.max_length = max_length
            self.min_length = min_length

        def __str__(self):
            return '{} - {}'.format(self.name, self.dtype)