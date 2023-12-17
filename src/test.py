from typing import Optional


class B:
    ...


class A:
    def __init__(self, b, c, d: B = None):
        self.d = d or B()



def a(b, c, d: Optional[A] = None):
    ...