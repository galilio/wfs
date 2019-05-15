class Predicate(object):
    pass

class ComparisonPredicate(Predicate):
    pass

class LogicalPredicate(Predicate):
    pass

class EqualTo(ComparisonPredicate):
    pass

class NotEqualTo(ComparisonPredicate):
    pass

class LessThan(ComparisonPredicate):
    pass

class LessThanOrEqual(ComparisonPredicate):
    pass

class GreaterThan(ComparisonPredicate):
    pass

class GreaterThanOrEqual(ComparisonPredicate):
    pass
