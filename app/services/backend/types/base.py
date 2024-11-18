from stollen import MutableStollenObject, StollenObject

from ..client import Backend


class SplitObject(StollenObject[Backend]):
    pass


class MutableSplitObject(MutableStollenObject[Backend]):
    pass
