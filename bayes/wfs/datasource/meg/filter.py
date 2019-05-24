from sqlalchemy.sql import and_, or_, not_ # binary comp
import geoalchemy2
from sqlalchemy import func

from bayes.wfs.core.filter import *

class TableNotFound(Exception):
    def __init__(self, table):
        super().__init__(f'Table {table} Not Found')
        self.table = table

class FilterObjectNotSupported(Exception):
    def __init__(self, obj):
        super().__init__(f'Filter Object {obj} Not Supported')
        self.obj = obj

class TableMapper(object):
    '''
    Table Mapper: map feature name or aliases to table object of sqlalchemy
    '''
    def __init__(self, tables, typenames, aliases = None):
        self.tables = tables
        self.typenames = typenames
        self.aliases = aliases

    def get_table(self, name):
        '''
        get table from valref.
        '''
        if not name and len(self.tables) == 1:
            return self.tables[0]

        if name in self.typenames:
            return self.tables[self.typenames.index(name)]
        if self.aliases and name in self.aliases:
            return self.tables[self.aliases.index(name)]
        
        raise TableNotFound(name)

def value_ref(mapper, obj):
    table = mapper.get_table(obj.feature)
    return table.c[obj.name]

def literal(mapper, obj):
    return obj.val

def equal_to(mapper, obj):
    return filter(mapper, obj.val1) == filter(mapper, obj.val2)

def not_equal_to(mapper, obj):
    return filter(mapper, obj.val1) != filter(mapper, obj.val2)

def less_than(mapper, obj):
    return filter(mapper, obj.val1) < filter(mapper, obj.val2)

def less_than_or_equal(mapper, obj):
    return filter(mapper, obj.val1) <= filter(mapper, obj.val2)

def greater_than(mapper, obj):
    return filter(mapper, obj.val1) > filter(mapper, obj.val2)

def greater_than_or_equal(mapper, obj):
    return filter(mapper, obj.val1) >= filter(mapper, obj.val2)

def _like(mapper, obj):
    return filter(mapper, obj.val1).like(filter(mapper, obj.val2))

def _null(mapper, obj):
    return filter(mapper, obj.item).is_(None)

def _and(mapper, obj):
    inner = []
    for item in obj.items:
        inner.append(filter(mapper, item))
    return and_(*inner)

def _or(mapper, obj):
    inner = []
    for item in obj.items:
        inner.append(filter(mapper, item))
    return or_(*inner)

def _not(mapper, obj):
    return not_(filter(mapper, obj.item))

def st_equals(mapper, obj):
    return func.ST_Equals(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_disjoint(mapper, obj):
    return func.ST_Disjoint(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_within(mapper, obj):
    return func.ST_Within(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_touches(mapper, obj):
    return func.ST_Touches(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_overlaps(mapper, obj):
    return func.ST_Overlaps(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_crosses(mapper, obj):
    return func.ST_Crosses(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_intersects(mapper, obj):
    return func.ST_Intersects(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_contains(mapper, obj):
    return func.ST_Contains(filter(mapper, obj.geom1), filter(mapper, obj.geom2))

def st_dwithin(mapper, obj):
    return func.ST_DWithin(filter(mapper, obj.geom1), filter(mapper, obj.geom2), filter(mapper, obj.distance))

def wkt(mapper, obj):
    return obj.wkt

_mapping = {
    ValueRef: value_ref,
    Literal: literal,
    And: _and,
    Or: _or,
    Not: _not,
    EqualTo: equal_to,
    NotEqualTo: not_equal_to,
    LessThan: less_than,
    LessThanOrEqualTo: less_than_or_equal,
    GreaterThan: greater_than,
    GreaterThanOrEqualTo: greater_than_or_equal,
    Like: _like,
    Null: _null,
    ST_Equals: st_equals,
    ST_Disjoint: st_disjoint,
    ST_Touches: st_touches,
    ST_Within: st_within,
    ST_Overlaps: st_overlaps,
    ST_Crosses: st_crosses,
    ST_Intersects: st_intersects,
    ST_Contains: st_contains,
    ST_DWithin: st_dwithin,
    Wkt: wkt,
}

def filter(mapper, obj):
    print(f'filter {obj}')
    if obj.__class__ not in _mapping:
        raise FilterObjectNotSupported(obj)
    
    return _mapping[obj.__class__](mapper, obj)
