class Bar:
    pass


def bar(*args, **kwargs):
    return Bar


class Foo:
    pass


class Foo1(
    object
):
    pass


class Foo2(
    object,
):
    pass


class Foo3(
    Bar
):
    pass


class Foo4(
    Bar,
):
    pass


class Foo5(
    bar
):
    pass


class Foo6(
    bar,
):
    pass


class Foo7(
    bar()
):
    pass


class Foo8(
    bar(),
):
    pass


class Foo9(Bar):
    pass


class Foo10(
    Bar):
    pass


class Foo11(
    lambda: None
):
    pass


class Foo12(
    bar('a', a='a')
):
    pass
