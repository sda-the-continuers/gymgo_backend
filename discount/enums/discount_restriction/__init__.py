OPERATOR_LT = 'lt'
OPERATOR_LE = 'le'
OPERATOR_GT = 'gt'
OPERATOR_GE = 'ge'
OPERATOR_EQ = 'eq'
OPERATOR_NE = 'ne'
OPERATOR_CONTAINS = 'contains'

EQUALITY_OPERATORS = (
    (OPERATOR_EQ, 'برابر'),
    (OPERATOR_NE, 'نابرابر'),
)

TEXT_OPERATORS = (
    (OPERATOR_CONTAINS, 'شامل'),
)

COMPARABLE_OPERATORS = (
    (OPERATOR_LT, 'کمتر از'),
    (OPERATOR_LE, 'کمتر از یا برابر'),
    (OPERATOR_GT, 'بزرگتر از'),
    (OPERATOR_GE, 'بزرگتر از یا برابر'),
)

from .typed_discount_restriction import *
