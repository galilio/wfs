import re
import abc
from bayes.wfs.core.exceptions import OperateNotSupported, OMGException, InvalidFilter

class ValueRef(object):
    __slots__ = 'feature', 'name'
    def __init__(self, val):
        super().__init__()

        parts = re.split(r'/', val)
        while True:
            try:
                parts.remove('')
            except ValueError:
                break
        self.name = parts[-1]
        if len(parts) > 1:
            self.feature = parts[0]
        else:
            self.feature = None

    @classmethod
    def parse(cls, val):
        return ValueRef(val)

class Function(object):
    __slots__ = 'func', 'args'
    def __init__(self, func, args = []):
        super().__init__()

        self.func = func
        self.args = args

    @classmethod
    def parse(cls, obj):
        if 'name' not in obj:
            raise InvalidFilter('fes:Function', obj, 'Function need name property')

        func = obj['name']
        params_obj = obj.get('params', [])

        params = []
        for item in params_obj:
            params.append(parse_fes(item, params_obj[item]))

        return Function(func, params)

class Literal(object):
    def __init__(self, val):
        super().__init__()
        self.val = val

    @classmethod
    def parse(cls, val):
        return Literal(val)

class Operator(object):

    @classmethod
    @abc.abstractmethod
    def parse(cls, obj):
        raise OMGException()

class LogicalOperator(Operator):
    pass

class And(LogicalOperator):
    __slots__ = 'items'

    def __init__(self, items = []):
        super().__init__()
        self.items = items
    
    @classmethod
    def parse(cls, obj):
        retval = And()

        for key in obj:
            child = parse_fes(key, obj[key])
            if isinstance(child, (tuple, list)):
                retval.items += child
            else:
                retval.items.append(child)

        return retval

class Or(LogicalOperator):
    __slots__ = 'items'

    def __init__(self, items = []):
        super().__init__()
        self.items = items
    
    @classmethod
    def parse(cls, obj):
        retval = Or()

        if not isinstance(obj, (tuple, list)):
            raise InvalidFilter('fes:Or', obj, 'Child of fes:Or need to be list.')

        for item in obj:
            for key in item:
                retval.items.append(parse_fes(key, item[key]))
        return retval

class Not(LogicalOperator):
    __slots__ = 'item'
    def __init__(self, item):
        super().__init__()
        self.item = item

    @classmethod
    def parse(cls, obj):
        if len(obj) != 1:
            raise InvalidFilter('fes:Not', obj, 'Child of fes:Not need to be only one')


        item = parse_fes(*obj.popitem())
        return Not(item)

class BinaryOperator(Operator):
    __slots__ = 'val1', 'val2'
    def __init__(self, val1, val2):
        super().__init__()

        self.val1 = val1
        self.val2 = val2

    @classmethod
    def parse(cls, obj):
        retval = []
        cls_name = cls.__name__
        if not isinstance(obj, (tuple, list)):
            raise InvalidFilter(f'fes:PropertyIs{cls_name}', obj, f'Children of {cls_name} need to be list')
        for item in obj:
            keys = list(item.keys())
            if len(keys) != 2:
                raise InvalidFilter(f'fes:PropertyIs{cls_name}', item, 'Children of {cls_name} need to 2.')

            val1 = parse_fes(keys[0], item[keys[0]])
            val2 = parse_fes(keys[1], item[keys[1]])
            retval.append(cls(val1, val2))

        return retval if len(retval) > 1 else retval[-1]

class EqualTo(BinaryOperator):
    pass

class NotEqualTo(BinaryOperator):
    pass

class LessThan(BinaryOperator):
    pass

class GreaterThan(BinaryOperator):
    pass

class LessThanOrEqualTo(BinaryOperator):
    pass

class GreaterThanOrEqualTo(BinaryOperator):
    pass

class Like(BinaryOperator):
    pass

class Null(Operator):
    def __init__(self, item):
        super().__init__()
        self.item = item
    
    @classmethod
    def parse(cls, obj):
        if len(obj) != 1:
            raise InvalidFilter(f'fes:PropertyIsNull', obj, 'Child of Null need to be 1')
        if not isinstance(obj, dict):
            raise InvalidFilter(f'fes:PropertyIsNull', obj, 'Child of Null show to be dict')
        item = parse_fes(*obj.popitem())
        return Null(item)

class Between(Operator):

    def __init__(self, item, lower, upper):
        super().__init__()
        self.item = item
        self.lower = lower
        self.upper = upper

    @classmethod
    def parse(cls, obj):
        lower = None
        upper = None
        item = None

        for key in obj:
            if key == 'fes:LowerBoundary':
                lower = parse_fes(*(obj[key].popitem()))
            elif key == 'fes:UpperBoundary':
                upper = parse_fes(*(obj[key].popitem()))
            else:
                item = parse_fes(key, obj[key])

        if not lower or not upper or not item:
            raise InvalidFilter('fes:PropertyIsBetween', obj, 'Need upper and lower boundary')
        return Between(item, lower, upper)

class SpatialOperator(Operator):
    __slots__ = 'geom1', 'geom2'
    def __init__(self, geom1, geom2):
        super().__init__()

        self.geom1 = geom1
        self.geom2 = geom2

    @classmethod
    def parse(cls, obj):
        cls_name = cls.__name__
        if not isinstance(obj, list) or len(obj) != 2:
            raise InvalidFilter(f'fes:PropertyIs{cls_name}', obj, f'Children of {cls_name} need to be list with length 2')

        geom1 = parse_fes(*(obj[0].popitem()))
        geom2 = parse_fes(*(obj[1].popitem()))

        return cls(geom1, geom2)


class ST_Equals(SpatialOperator):
    pass

class ST_Disjoint(SpatialOperator):
    pass

class ST_Touches(SpatialOperator):
    pass

class ST_Within(SpatialOperator):
    pass

class ST_Overlaps(SpatialOperator):
    pass

class ST_Crosses(SpatialOperator):
    pass

class ST_Intersects(SpatialOperator):
    pass

class ST_Contains(SpatialOperator):
    pass

class ST_DWithin(SpatialOperator):
    def __init__(self, geom1, geom2, distance):
        super().__init__(geom1, geom2)
        self.distance = distance
    
    @classmethod
    def parse(cls, obj):
        cls_name = cls.__name__
        if not isinstance(obj, dict):
            raise InvalidFilter(f'fes:{cls_name}', obj, f'Children of {cls_name} need to be dict')

        if not 'fes:Geoms' in obj:
            raise InvalidFilter(f'fes:{cls_name}', obj, f'Children of {cls_name} need fes:Geoms')
        if not 'fes:Distance' in obj:
            raise InvalidFilter(f'fes:{cls_name}', obj, f'Children of {cls_name} need fes:Geoms')

        geom1 = parse_fes(*(obj['fes:Geoms'][0].popitem()))
        geom2 = parse_fes(*(obj['fes:Geoms'][1].popitem()))
        distance = parse_fes(*(obj['fes:Distance'].popitem()))
        return ST_DWithin(geom1, geom2, distance)

class GeoJSON(object):
    def __init__(self, str):
        super().__init__()
        self.str = str

    @classmethod
    def parse(cls, obj):
        if not isinstance(obj, str):
            raise InvalidFilter('fes:GeoJSON', obj, 'GeoJSON should be str.')
        return GeoJSON(obj)

class Wkt(object):
    def __init__(self, wkt):
        super().__init__()
        self.wkt = wkt

    @classmethod
    def parse(cls, obj):
        if not isinstance(obj, str):
            raise InvalidFilter('fes:Wkt', obj, 'Wkt should be str.')
        return Wkt(obj)

_mapping = {
    'fes:PropertyIsEqualTo': EqualTo,
    'fes:PropertyIsNotEqualTo': NotEqualTo,
    'fes:PropertyIsLessThan': LessThan,
    'fes:PropertyIsGreaterThan': GreaterThan,
    'fes:PropertyIsLessThanOrEqualTo': LessThanOrEqualTo,
    'fes:PropertyIsGreaterThanOrEqualTo': GreaterThanOrEqualTo,
    'fes:PropertyIsLike': Like,
    'fes:PropertyIsNull': Null,
    'fes:PropertyIsBetween': Between,
    'fes:Equals': ST_Equals,
    'fes:Disjoint': ST_Disjoint,
    'fes:Touches': ST_Touches,
    'fes:Within': ST_Within,
    'fes:Overlaps': ST_Overlaps,
    'fes:Crosses': ST_Crosses,
    'fes:Intersects': ST_Intersects,
    'fes:Contains': ST_Contains,
    'fes:DWithin': ST_DWithin,
    'fes:And': And,
    'fes:Or': Or,
    'fes:Not': Not,
    'fes:ValueReference': ValueRef,
    'fes:Function': Function,
    'fes:Literal': Literal,
    'fes:GeoJSON': GeoJSON,
    'fes:Wkt': Wkt
}

def parse_fes(key, fes_filter):
    if key not in _mapping:
        raise OperateNotSupported(key)
    cls = _mapping[key]
    return cls.parse(fes_filter)
