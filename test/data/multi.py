class Bar:
    pass


def bar(*args, **kwargs):
    return Bar


class Foo:
    pass


class Foo1(
    Bar,
    Foo
):
    pass


class Foo2(
    Bar,
    Foo,
):
    pass


class Foo3(
    Bar(),
    Foo()
):
    pass


class Foo4(
    Bar(),
    Foo(),
):
    pass


class Foo5(
    Foo,
    Bar()
):
    pass


class Foo6(
    Foo,
    Bar(),
):
    pass


class Foo7(
    Foo,
    bar()
):
    pass


class Foo8(
    Foo,
    bar(),
):
    pass


class Foo9(Foo, Bar):
    pass


class Foo10(
    Foo,
    Bar):
    pass


class Foo11(
    Foo,
    lambda: None
):
    pass


class Foo12(
    Foo,
    bar('a', a='a')
):
    pass
