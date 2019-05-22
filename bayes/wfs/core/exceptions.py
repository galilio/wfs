class VersionNegotiationFailed(Exception):
    def __init__(self, target):
        super().__init__(f'version {target} not supported.')
        self.target = target


class FormatNotSupportedException(Exception):
    def __init__(self, formats):
        formats_str = ','.join(formats)
        super().__init__(f'{formats_str} not supported.')
        self.formats = formats

class OMGException(Exception):
    def __init__(self):
        super().__init__('Shoud never reach here.')

class InvalidTypeName(Exception):
    def __init__(self, typename):
        super().__init__(f'invalid typename <{typename}>')
        self.typename = typename

class AliasesMissmatch(Exception):
    def __init__(self, typenames, aliases):
        super().__init__(f'alias {aliases} miss match with {typenames}')
        self.typenames = typenames
        self.aliases = aliases

class ProjectionFailed(Exception):
    def __init__(self, projections):
        super().__init__(f'projections failed {projections}')
        self.projections = projections

class NoSuchProperty(Exception):
    def __init__(self, table, props):
        super().__init__(f'table {table} no such property {props}')
        self.props = props

class OperateNotSupported(Exception):
    def __init__(self, which):
        super().__init__(f'Operate {which} not supported.')
        self.which = which

class InvalidFilter(Exception):
    def __init__(self, op, obj, msg):
        super().__init__(f'{op} Invalid Filter {obj}: <{msg}>')
        self.op = op
        self.obj = obj
        self.msg = msg