import abc
import yaml

from bayes.wfs.core.config import Configuration
from bayes.wfs.core.exceptions import *
from bayes.wfs.core.ogc_types import *

class DataSource(metaclass = abc.ABCMeta):

    def __init__(self, cfg = None):
        self.config = cfg

    @property
    @abc.abstractmethod
    def version(self):
        raise OMGException()

    @property
    @abc.abstractmethod
    def source_id(self):
        '''
        since there may be more than one source registered, each source should has id
        generated by uuid
        '''
        raise OMGException()

    @property
    @abc.abstractmethod
    def formats(self):
        '''
        formats which data source supported.
        '''
        raise OMGException()

    @property
    @abc.abstractmethod
    def update_sequence(self):
        '''
        update sequence of server.
        '''
        raise OMGException()

    @property
    @abc.abstractmethod
    def service_identification(self):
        raise OMGException()

    @property
    @abc.abstractmethod
    def service_provider(self):
        raise OMGException()

    @property
    @abc.abstractmethod
    def operations_metadata(self):
        raise OMGException()

    @abc.abstractmethod
    def get_contents(self):
        raise OMGException()

    def get_capabilities(self, accept_versions, sections, update_sequence, accept_formats):
        '''
        accept_versions: prioritized sequence of one or more specification versions accepted
            by client, with preferred versions list first.
        sections: Unordered list of zero or more names of requested sections in complete
            service metadata document.
        update_sequence: service metadata document version, value if 'increased' whenever
            any change is made in complete service metadata document.
        accept_formats: prioritized sequence of zero or more response formats desired by
            client, with the preferred formats listed first.
        '''
        if accept_versions and self.version not in accept_versions:
            '''
            if user specified accept versions, check is or just pass.
            '''
            raise VersionNegotiationFailed(','.join(accept_versions))

        if accept_formats:
            format_supported = False
            for format in self.formats:
                if format in accept_formats:
                    format_supported = True
        else:
            format_supported = True

        if not format_supported:
            raise FormatNotSupportedException(accept_formats)
        
        # TODO: update_sequence not supported.

        si = ServiceMeta(self.version, self.update_sequence)

        if ('ServiceIdentification' in sections) or ('ALL' in sections):
            si.service_identification = self.service_identification
        else:
            si.service_identification = None

        if ('ServiceProvider' in sections) or ('ALL' in sections):
            si.service_provider = self.service_provider
        else:
            si.service_provider = None

        if ('OperationsMetadata' in sections) or ('ALL' in sections):
            si.operations_metadata = self.operations_metadata
        else:
            si.operations_metadata = None

        if ('Contents' in sections) or ('ALL' in sections):
            si.contents = self.get_contents()
        else:
            si.contents = None

        return si

    def describe_feature_type(self, typenames):
        feature_describe = {}
        for typename in typenames:
            feature_describe[typename] = self.describe_one_feature_type(typename)
        return feature_describe

    @abc.abstractmethod
    def describe_one_feature_type(self, typename):
        raise OMGException()

    @abc.abstractmethod
    def get_feature(self, typenames, aliases = None, projection = None, filter = None, bbox = None, sort_by = None):
        print(typenames, aliases)
        if aliases is not None and len(aliases) != len(typenames):
            raise AliasesMissmatch(typenames, aliases)