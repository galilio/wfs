from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import alias
from sqlalchemy.exc import ProgrammingError

from sqlalchemy.sql import and_, or_, not_ # logic
import geoalchemy2

from sqlalchemy import func
# related to ISO 19143 spatial operators
# func.ST_Disjoint
# func.ST_Touches
# func.ST_Within
# func.ST_Overlaps
# func.ST_Crosses
# func.ST_Intersects
# func.ST_Contains
# func.ST_DWithIn

from sqlalchemy.exc import OperationalError
from bayes.wfs.core import DataSource, ServiceIdentification, ServiceProvider
from bayes.wfs.core import OperationsMetadata
from bayes.wfs.core import FeatureType
from bayes.wfs.core import InvalidTypeName, AliasesMissmatch, ProjectionFailed, NoSuchProperty
from bayes.wfs.core.config import InvalidKeyException
from bayes.wfs.datasource.meg import filter as meg_filter
from bayes.wfs.datasource.meg import meg_feature

import logging

WFS_ENDPOINT = '/wfs'

class MissingConfigError(Exception):
    def __init__(self):
        super().__init__('When use MegDataSource, you should include MegDataSource.db section in config.yaml.')

class DatabaseConnectError(Exception):
    def __init__(self, conn_str):
        super().__init__(f'Database connect failed {conn_str}')

class PostgisNotFoundException(Exception):
    def __init__(self):
        super().__init__('use "CREATE EXTENSION postgis" on database first.')

class SQLError(Exception):
    def __init__(self, sql, error):
        super().__init__(f'{sql} ERROR: {error}')
        self.sql = sql
        self.error = error

class GeometryTable(object):
    class Column(object):
        def __init__(self, name, srid, dimension, type):
            self.name = name
            self.srid = srid
            self.dimension = dimension
            self.type = type

    def __init__(self, schema, name, columns = {}):
        self.schema = schema
        self.name = name
        self.columns = columns
        self.table = None

class MegDataSource(DataSource):

    def __init__(self, cfg):
        super().__init__(cfg)
        try:
            self.config.get('MegDataSource.db')
        except InvalidKeyException:
            raise MissingConfigError()

        self.si = ServiceIdentification()
        self.si.description = ServiceIdentification.Description('BayesBA Meg GIS',
            '''
            City POI database powered by bayesba.
            ''', [
                'POI', 'City', 'Business Circle'
            ])
        self.si.service_type = 'WFS'
        self.si.service_type_version = '2.0.0'
        self.si.fees = 'Internal Only'
        self.si.access_constraints = 'Open But guard by service host.'

        self.sp = ServiceProvider()
        self.sp.provider_name = 'BayesBa'
        self.sp.provider_site = 'www.bayesba.com'
        self.sp.service_contact = ServiceProvider.Contact('xiaoyuming', 'yuming.xiao@bayesba.com')

        # TODO: read domain from configure
        self.om = OperationsMetadata(['xxxxxxx'])

        op = self.create_operation('GetCapabilities', 'Get service capabilities',
            WFS_ENDPOINT, 'Get', ['xxxxxxxx'])
        self.om.operations.append(op)
        print(self.config.get('MegDataSource.db'))
        self.engine = create_engine(self.config.get('MegDataSource.db'))
        try: # if connect failed, invalid config.
            conn = self.engine.connect()
        except OperationalError as e:
            raise DatabaseConnectError(self.config.get('MegDataSource.db'))

        try:
            self.ensure_database_has_geometry_table(conn)
        finally:
            conn.close()

        self.meta = MetaData()
        self.tables = {}
        self.inspect_geometry_tables()

    def ensure_database_has_geometry_table(self, conn):
        if not self.engine.dialect.has_table(conn, 'geometry_columns'):
            raise PostgisNotFoundException()

    def inspect_geometry_tables(self):
        conn = self.engine.connect()

        try:
            metatable = Table('geometry_columns', self.meta, autoload = True, autoload_with = self.engine, schema = 'public')
            result = conn.execute(select([metatable]))

            for r in result:
                key = '{}.{}'.format(r[metatable.c.f_table_schema], r[metatable.c.f_table_name])
                table = self.tables.get(key)
                if not table:
                    logging.info(f'Find new table {r[metatable.c.f_table_name]}')
                    table = GeometryTable(r[metatable.c.f_table_schema], r[metatable.c.f_table_name])
                    table.table = Table(r[metatable.c.f_table_name], self.meta, autoload = True, autoload_with = self.engine, schema = r[metatable.c.f_table_schema])

                    table.feature = self.create_feature_from_table(table.table)
                    self.tables[key] = table

                if r[metatable.c.f_geometry_column] in table.columns:
                    logging.warning(f'duplicated geometry column {key} {r}')
                    continue

                column = GeometryTable.Column(r[metatable.c.f_geometry_column],
                    r[metatable.c.coord_dimension], r[metatable.c.srid], r[metatable.c.type])
                table.columns[r[metatable.c.f_geometry_column]] = column

            for key in self.tables:
                print(key)
        finally:
            conn.close()

    def create_feature_from_table(self, table):
        title = '{}.{}'.format(table.schema, table.name)
        feature = FeatureType(title, abstract = table.comment)
        for column in table.columns:
            prop = FeatureType.Property(column.name, column.type, pk = column.primary_key, nullable = column.nullable)
            feature.properties.append(prop)

        return feature

    def create_operation(self, name, about, link, request_method, domains):
        op = OperationsMetadata.Operation()
        op.name = name
        op.about = about
        op.link = link
        op.request_method = request_method
        op.domains = domains
        return op

    @property
    def version(self):
        return '2.0.0'

    @property
    def formats(self):
        return ['application/json']

    @property
    def source_id(self):
        # generated by uuid.
        return '93644997-04a6-4263-a677-2cd6c6f0e716'

    @property
    def update_sequence(self):
        return None

    @property
    def service_identification(self):
        return self.si

    @property
    def service_provider(self):
        return self.sp

    @property
    def operations_metadata(self):
        return self.om

    def get_contents(self):
        retval = []
        for key in self.tables:
            table = self.tables[key]
            retval.append(table.feature)
        return retval

    def describe_one_feature_type(self, typename):
        if typename not in self.tables:
            raise InvalidTypeName(typename)
        return self.tables[typename].feature

    @staticmethod
    def is2dlist(a):
        if not a:
            return False
        return isinstance(a[0], (tuple, list))

    def _map_projection(self, tables, projection):
        if not projection:
            return tables

        if len(tables) > 1 and (not self.is2dlist(projection) or len(tables) != len(projection)):
            raise ProjectionFailed(projection)

        if len(tables) == 1 and self.is2dlist(projection):
            raise ProjectionFailed(projection)

        projected = []
        for i, table in enumerate(tables):
            table_projection = projection[i] if len(tables) > 1 else projection
            for ps in table_projection:
                try:
                    projected.append(table.c[ps])
                except KeyError:
                    raise NoSuchProperty(table.name, ps)

        return projected

    def debug(self, msg):
        if self.config.get('MegDataSource.debug', False):
            logging.info(msg)

    def get_feature(self, typenames, aliases = None, projection = None, filter = None, bbox = None, sort_by = None, fetch_data = True):
        super().get_feature(typenames, aliases, projection, filter, bbox, sort_by)

        tables = []
        for i, typename in enumerate(typenames):
            if typename not in self.tables:
                raise InvalidTypeName(typename)

            table = self.tables[typename].table
            if aliases is not None:
                table = table.alias(aliases[i])

            tables.append(table)
        table_mapper = meg_filter.TableMapper(tables, typenames, aliases)
        tables = self._map_projection(tables, projection)

        sql = select(tables)
        if filter:
            where = meg_filter.filter(table_mapper, filter)
            sql = sql.where(where)

        self.debug(sql)

        if not fetch_data:
            return sql

        try:
            return meg_feature.pack_result_proxy(table_mapper, self.engine.execute(sql))
        except ProgrammingError as e:
            raise SQLError(sql, str(e))


